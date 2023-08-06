import shlex

from fire import parser


class CommandParser:
    """Parse command string into client operations and arguments."""

    def __init__(self, client):
        """Initialize parser based on the given client object."""
        self.client = client

    def parse(self, text):
        """Parse command string into operations and arguments."""
        attributes = []
        raw_arguments = []

        # Parse command elements based on the regular expression
        elements = shlex.split(text)

        # Separate elements into attributes and arguments
        for element in elements:
            if element.startswith("-"):
                raw_arguments.append(element)
            else:
                attributes.append(element)

        operation = self.get_operation(attributes=attributes)
        arguments = self.get_arguments_dict(raw_arguments=raw_arguments)

        return operation, arguments

    def get_operation(self, attributes):
        """Return the required operation based on the attribute list."""
        obj = self.client

        obj_operation_map = obj._operation_map
        len_attr = len(attributes)
        obj_meth_attr = None

        if len_attr == 1:
            obj_meth_attr = attributes[0]
            if obj_meth_attr not in obj_operation_map.keys():
                raise ValueError(
                    "Wrong <object/method> for PrivCloud API: <%s>" % obj_meth_attr
                )
            operation = obj._get_callable(obj_operation_map[obj_meth_attr].request)
        else:
            raise ValueError("Too many or none attributes <%r>" % attributes)

        return operation

    def get_arguments_dict(self, raw_arguments):
        arguments, data = {}, {}
        first_symb, last_symb = "[", "]"
        for raw_argument in raw_arguments:
            striped_argument = raw_argument.lstrip("-")
            is_req_body_arg = False

            if "body" in striped_argument:
                is_req_body_arg = True
                prefix = "body." if not striped_argument.startswith("body=") else "body"
                striped_argument = striped_argument.removeprefix(prefix)
            if "=" in striped_argument:
                full_path, value = striped_argument.split("=")
            else:
                full_path, value = striped_argument, "True"
            if first_symb and last_symb in value:
                value = [
                    x.strip()
                    for x in value.replace(first_symb, "")
                    .replace(last_symb, "")
                    .split(",")
                ]
            if is_req_body_arg:
                if isinstance(value, str) and value.isnumeric():
                    value = int(value)
                if not full_path:
                    data = value
                else:
                    data[full_path] = value
            else:
                self.set_nested(arguments, value, *full_path.split("."))
        arguments = {"parameters": arguments, "data": data}
        return arguments

    @staticmethod
    def set_nested(dictionary, value, *path):
        """Set the value in the given path to the given nested dictionary."""
        for level in path[:-1]:
            dictionary = dictionary.setdefault(level, {})

        # Use fire parser to convert raw argument into a value
        dictionary[path[-1]] = parser.DefaultParseValue(value)
