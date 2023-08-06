from openapi3.components import Components
from openapi3.general import Reference
from openapi3.openapi import OpenAPI
from openapi3.paths import MediaType, Path, Operation, Parameter, RequestBody, Response
from openapi3.schemas import Schema, Model, TYPE_LOOKUP
from openapi3.errors import SpecError
from openapi3.object_base import ObjectBase
import requests

"""
TODO: contribute these changes to openapi3 library, cause this is an ugly override to support more openapi3 spec
"""


class OpenAPIExt(OpenAPI):
    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self._operation_map = {}

        self.components = self._get("components", ["ComponentsExt"])
        self.externalDocs = self._get("externalDocs", dict)
        self.info = self._get("info", "Info")
        self.openapi = self._get("openapi", str)
        self.paths = self._get("paths", ["PathExt"], is_map=True)
        self.security = self._get("security", ["SecurityRequirement"], is_list=True)
        self.servers = self._get("servers", ["Server"], is_list=True)
        self.tags = self._get("tags", ["Tag"], is_list=True)

        # now that we've parsed _all_ the data, resolve all references
        self._resolve_references()
        self._resolve_allOfs()


class PathExt(Path, ObjectBase):
    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        # TODO - handle possible $ref
        self.delete = self._get("delete", "OperationExt")
        self.description = self._get("description", str)
        self.get = self._get("get", "OperationExt")
        self.head = self._get("head", "OperationExt")
        self.options = self._get("options", "OperationExt")
        self.parameters = self._get(
            "parameters", ["ParameterExt", "Reference"], is_list=True
        )
        self.patch = self._get("patch", "OperationExt")
        self.post = self._get("post", "OperationExt")
        self.put = self._get("put", "OperationExt")
        self.servers = self._get("servers", ["Server"], is_list=True)
        self.summary = self._get("summary", str)
        self.trace = self._get("trace", "OperationExt")

        if self.parameters is None:
            # this will be iterated over later
            self.parameters = []


class ParameterExt(Parameter, ObjectBase):
    """
    A `Parameter Object`_ defines a single operation parameter.

    .. _Parameter Object: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#parameterObject
    """

    __slots__ = [
        "name",
        "in",
        "in_",
        "description",
        "required",
        "deprecated",
        "allowEmptyValue",
        "style",
        "explode",
        "allowReserved",
        "schema",
        "example",
        "examples",
    ]
    required_fields = ["name", "in"]

    def _parse_data(self):
        self.deprecated = self._get("deprecated", bool)
        self.description = self._get("description", str)
        self.example = self._get("example", str)
        self.examples = self._get("examples", dict)  # Map[str: ['Example','Reference']]
        self.explode = self._get("explode", bool)
        self.in_ = self._get(
            "in", str
        )  # TODO must be one of ["query","header","path","cookie"]
        self.name = self._get("name", str)
        self.required = self._get("required", bool)
        self.schema = self._get("schema", ["SchemaExt", "Reference"])
        self.style = self._get("style", str)

        # allow empty or reserved values in Parameter data
        self.allowEmptyValue = self._get("allowEmptyValue", bool)
        self.allowReserved = self._get("allowReserved", bool)

        # required is required and must be True if this parameter is in the path
        if self.in_ == "path" and self.required is not True:
            err_msg = "Parameter {} must be required since it is in the path"
            raise SpecError(err_msg.format(self.get_path()), path=self.path)


class RequestBodyExt(RequestBody, ObjectBase):
    """
    A `RequestBody`_ object describes a single request body.

    .. _RequestBody: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#requestBodyObject
    """

    __slots__ = ["description", "content", "required"]
    required_fields = ["content"]

    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self.description = self._get("description", str)
        self.content = self._get("content", ["MediaTypeExt"], is_map=True)
        raw_content = self._get("content", dict)
        self.required = self._get("required", bool)


class MediaTypeExt(MediaType, ObjectBase):
    """
    A `MediaType`_ object provides schema and examples for the media type identified
    by its key.  These are used in a RequestBody object.

    .. _MediaType: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#mediaTypeObject
    """

    __slots__ = ["schema", "example", "examples", "encoding"]
    required_fields = []

    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self.schema = self._get("schema", ["SchemaExt", "Reference"])
        self.example = self._get("example", str)  # 'any' type
        self.examples = self._get("examples", ["Example", "Reference"], is_map=True)
        self.encoding = self._get("encoding", dict)  # Map['Encoding']


class ResponseExt(Response, ObjectBase):
    """
    A `Response Object`_ describes a single response from an API Operation,
    including design-time, static links to operations based on the response.

    .. _Response Object: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#response-object
    """

    __slots__ = ["description", "headers", "content", "links"]
    required_fields = ["description"]

    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self.content = self._get("content", ["MediaTypeExt"], is_map=True)
        self.description = self._get("description", str)
        raw_content = self._get("content", dict)
        raw_headers = self._get("headers", dict)
        raw_links = self._get("links", dict)


class OperationExt(Operation, ObjectBase):
    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        raw_servers = self._get("servers", list)
        self.deprecated = self._get("deprecated", bool)
        self.description = self._get("description", str)
        self.externalDocs = self._get("externalDocs", "ExternalDocumentation")
        self.operationId = self._get("operationId", str)
        self.parameters = self._get(
            "parameters", ["ParameterExt", "Reference"], is_list=True
        )
        self.requestBody = self._get("requestBody", ["RequestBodyExt", "Reference"])
        self.responses = self._get(
            "responses", ["ResponseExt", "Reference"], is_map=True
        )
        self.security = self._get("security", ["SecurityRequirement"], is_list=True)
        self.servers = self._get("servers", ["Server"], is_list=True)
        self.summary = self._get("summary", str)
        self.tags = self._get("tags", list)
        raw_servers = self._get("servers", list)
        # self.callbacks  = self._get('callbacks', dict) TODO

        # default parameters to an empty list for processing later
        if self.parameters is None:
            self.parameters = []

        # gather all operations into the spec object
        if self.operationId is not None:
            # TODO - how to store without an operationId?
            formatted_operation_id = self.operationId.replace(" ", "_")
            self._root._register_operation(formatted_operation_id, self)

        # TODO - maybe make this generic
        if self.security is None:
            self.security = (
                self._root._get("security", ["SecurityRequirement"], is_list=True) or []
            )

        # Store session object
        self._session = requests.Session()

        # Store request object
        self._request = requests.Request()

    def _request_handle_secschemes(self, security_requirement, value):
        ss = self._root.components.securitySchemes[security_requirement.name]

        if ss.type == "http" and ss.scheme == "basic":
            self._request.auth = requests.auth.HTTPBasicAuth(*value)

        if ss.type == "http" and ss.scheme == "digest":
            self._request.auth = requests.auth.HTTPDigestAuth(*value)

        if ss.type == "http" and ss.scheme == "bearer":
            header = ss.bearerFormat or "Bearer {}"
            self._request.headers["Authorization"] = header.format(value)

        if ss.type == "mutualTLS":
            # TLS Client certificates (mutualTLS)
            self._request.cert = value

        if ss.type == "apiKey":
            if ss.in_ == "query":
                # apiKey in query parameter
                self._request.params[ss.name] = value

            if ss.in_ == "header":
                # apiKey in query header data
                self._request.headers[ss.name] = value

    def request(
        self,
        base_url,
        security={},
        data=None,
        parameters={},
        verify=True,
        session=None,
        raw_response=False,
    ):
        """
        Sends an HTTP request as described by this Path

        :param base_url: The URL to append this operation's path to when making
                         the call.
        :type base_url: str
        :param security: The security scheme to use, and the values it needs to
                         process successfully.
        :type security: dict{str: str}
        :param data: The request body to send.
        :type data: any, should match content/type
        :param parameters: The parameters used to create the path
        :type parameters: dict{str: str}
        :param verify: Should we do an ssl verification on the request or not,
                       In case str was provided, will use that as the CA.
        :type verify: bool/str
        :param session: a persistent request session
        :type session: None, requests.Session
        :param raw_response: If true, return the raw response instead of validating
                             and exterpolating it.
        :type raw_response: bool
        """
        # Set request method (e.g. 'GET')
        self._request = requests.Request(self.path[-1])

        # Set self._request.url to base_url w/ path
        self._request.url = base_url + self.path[-2]

        if security and self.security:
            security_requirement = None
            for scheme, value in security.items():
                security_requirement = None
                for r in self.security:
                    if r.name == scheme:
                        security_requirement = r
                        self._request_handle_secschemes(r, value)

            if security_requirement is None:
                err_msg = """No security requirement satisfied (accepts {}) \
                          """.format(
                    ", ".join(self.security.keys())
                )
                raise ValueError(err_msg)

        if self.requestBody:
            if self.requestBody.required and data is None:
                err_msg = "Request Body is required but none was provided."
                raise ValueError(err_msg)

            self._request_handle_body(data)

        self._request_handle_parameters(parameters)

        # send the prepared request
        result = self._session.send(self._request.prepare())

        # save request time in sec
        setattr(self._root, 'request_time_sec', result.elapsed.total_seconds())

        # spec enforces these are strings
        status_code = str(result.status_code)

        # find the response model in spec we received
        expected_response = None
        if status_code in self.responses:
            expected_response = self.responses[status_code]
        elif "default" in self.responses:
            expected_response = self.responses["default"]

        if expected_response is None:
            # TODO - custom exception class that has the response object in it
            err_msg = """Unexpected response {} from {} (expected one of {}, \
                         no default is defined"""
            err_var = (
                result.status_code,
                self.operationId,
                ",".join(self.responses.keys()),
            )

            raise RuntimeError(err_msg.format(*err_var))

        content_type = result.headers["Content-Type"]
        if not expected_response.content:
            response = ""
            try:
                response = result.json()
            except:
                response = result.text
            return response
        expected_media = expected_response.content.get(content_type, None)

        if expected_media is None and "/" in content_type:
            # accept media type ranges in the spec. the most specific matching
            # type should always be chosen, but if we do not have a match here
            # a generic range should be accepted if one if provided
            # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#response-object

            generic_type = content_type.split("/")[0] + "/*"
            expected_media = expected_response.content.get(generic_type, None)

        if expected_media is None:
            err_msg = """Unexpected Content-Type {} returned for operation {} \
                         (expected one of {})"""
            err_var = (
                result.headers["Content-Type"],
                self.operationId,
                ",".join(expected_response.content.keys()),
            )

            raise RuntimeError(err_msg.format(*err_var))

        response_data = None

        if content_type.lower() == "application/json":
            result_json = result.json()
            if isinstance(result_json, list):
                return [expected_media.schema.model(x) for x in result_json]
            return expected_media.schema.model(result_json)
        else:
            raise NotImplementedError()


class ComponentsExt(Components, ObjectBase):
    """
    A `Components Object`_ holds a reusable set of different aspects of the OAS
    spec.

    .. _Components Object: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.1.md#componentsObject
    """

    __slots__ = [
        "schemas",
        "responses",
        "parameters",
        "examples",
        "headers",
        "requestBodies",
        "securitySchemes",
        "links",
        "callback",
    ]

    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self.examples = self._get("examples", ["Example", "Reference"], is_map=True)
        self.parameters = self._get(
            "parameters", ["ParameterExt", "Reference"], is_map=True
        )
        self.requestBodies = self._get(
            "requestBody", ["RequestBodyExt", "Reference"], is_map=True
        )
        self.responses = self._get(
            "responses", ["ResponseExt", "Reference"], is_map=True
        )
        self.schemas = self._get("schemas", ["SchemaExt", "Reference"], is_map=True)
        self.securitySchemes = self._get(
            "securitySchemes", ["SecurityScheme", "Reference"], is_map=True
        )


class SchemaExt(Schema, ObjectBase):
    def _parse_data(self):
        """
        Implementation of :any:`ObjectBase._parse_data`
        """
        self.title = self._get("title", str)
        self.maximum = self._get("maximum", [int, float])
        self.minimum = self._get("minimum", [int, float])
        self.maxLength = self._get("maxLength", int)
        self.minLength = self._get("minLength", int)
        self.pattern = self._get("pattern", str)
        self.maxItems = self._get("maxItems", int)
        self.minItems = self._get("minItmes", int)
        self.required = self._get("required", list)
        self.enum = self._get("enum", list)
        self.type = self._get("type", str)
        self.allOf = self._get("allOf", ["SchemaExt", "Reference"], is_list=True)
        self.oneOf = self._get("oneOf", list)
        self.anyOf = self._get("anyOf", list)
        self.items = self._get("items", ["SchemaExt", "Reference"])
        self.properties = self._get(
            "properties", ["SchemaExt", "Reference"], is_map=True
        )
        self.additionalProperties = self._get(
            "additionalProperties", [bool, "Reference", dict]
        )
        self.description = self._get("description", str)
        self.format = self._get("format", str)
        self.default = self._get(
            "default", TYPE_LOOKUP.get(self.type, str)
        )  # TODO - str as a default?
        self.nullable = self._get("nullable", bool)
        self.discriminator = self._get("discriminator", dict)  # 'Discriminator'
        self.readOnly = self._get("readOnly", bool)
        self.writeOnly = self._get("writeOnly", bool)
        self.xml = self._get("xml", dict)  # 'XML'
        self.externalDocs = self._get("externalDocs", dict)  # 'ExternalDocs'
        self.deprecated = self._get("deprecated", bool)
        self.example = self._get("example", "*")

        # TODO - Implement the following properties:
        # self.multipleOf
        # self.not
        # self.uniqueItems
        # self.maxProperties
        # self.minProperties
        # self.exclusiveMinimum
        # self.exclusiveMaximum

        self._resolved_allOfs = False

        if self.type == "array" and self.items is None:
            raise SpecError(
                '{}: items is required when type is "array"'.format(self.get_path())
            )

    def get_type(self):
        """
        Returns the Type that this schema represents.  This Type is created once
        per Schema and cached so that all instances of the same schema are the
        same Type.  For example::

           object1 = example_schema.model({"some":"json"})
           object2 = example_schema.model({"other":"json"})

           isinstance(object1, example._schema.get_type()) # true
           type(object1) == type(object2) # true
        """
        # this is defined in ObjectBase.__init__ as all slots are
        if self._model_type is None:  # pylint: disable=access-member-before-definition
            type_name = self.title or self.path[-1]
            slots = []
            if self.properties:
                slots = self.properties.keys()
            elif self.items:
                slots = self.items.properties.keys()
            elif self.additionalProperties:
                if isinstance(self.additionalProperties, bool):
                    slots = []
                else:
                    slots = self.additionalProperties.properties.keys()
            self._model_type = type(
                type_name,
                (ModelExt,),
                {"__slots__": slots},  # pylint: disable=attribute-defined-outside-init
            )

        return self._model_type

    def get_request_type(self):
        """
        Similar to :any:`get_type`, but the resulting type does not accept readOnly
        fields
        """
        # this is defined in ObjectBase.__init__ as all slots are
        if (
            self._request_model_type is None
        ):  # pylint: disable=access-member-before-definition
            type_name = self.title or self.path[-1]
            self._request_model_type = type(
                type_name + "Request",
                (ModelExt,),
                {  # pylint: disable=attribute-defined-outside-init
                    "__slots__": [
                        k for k, v in self.properties.items() if not v.readOnly
                    ]
                },
            )

        return self._request_model_type


class ModelExt(Model):
    def __init__(self, data, schema):
        """
        Creates a new Model from data.  This should never be called directly,
        but instead should be called through :any:`Schema.model` to generate a
        Model from a defined Schema.

        :param data: The data to create this Model with
        :type data: dict
        """
        self._raw_data = data
        self._schema = schema

        for s in self.__slots__:
            # initialize all slots to None
            setattr(self, s, None)

        # collect the data into this model
        additional_props = False
        model_available = True
        properties = {}
        if schema.properties:
            properties = schema.properties
        elif schema.items:
            properties = schema.items.properties
        elif schema.additionalProperties:
            if isinstance(schema.additionalProperties, bool):
                properties = {}
                model_available = False
            else:
                properties = schema.additionalProperties.properties
            additional_props = True
        for k, v in data.items():
            if additional_props:
                if model_available:
                    setattr(self, k, schema.additionalProperties.model(v))
                else:
                    setattr(self, k, v)
                continue
            prop = properties[k]

            if prop.type == "array":
                # handle arrays
                if isinstance(prop.items, Reference):
                    prop._resolve_references()
                item_schema = prop.items
                setattr(self, k, [item_schema.model(c) for c in v])
            elif prop.type == "object":
                # handle nested objects
                object_schema = prop
                setattr(self, k, object_schema.model(v))
            else:
                setattr(self, k, v)
