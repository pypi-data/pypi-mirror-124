import shlex

from prompt_toolkit.completion import Completer, Completion

IN_USE_SCHEMA_ATTR = ["allOf", "oneOf", "items", "properties"]


class CommandCompleter(Completer):
    """Manage completion suggestions to the CLI."""

    def __init__(self, client):
        """Create a CLI commands completer based on the client object."""
        self.client = client
        self.definitions = client._operation_map

    def get_completions(self, document, complete_event):
        """Yields CLI completion based on the input text and the client object."""
        for completion, position in self._text_to_completions(document.text):
            yield Completion(completion, start_position=-position)

    def _text_to_completions(self, text):
        """Convert raw text into completion suggestions."""
        try:
            words = shlex.split(text)
        except ValueError:
            words = text.split(" ")

        operation, remaining_text, param_req_body_flag = self._extract_operation(
            words=words
        )

        if param_req_body_flag:
            return self._get_operation_attr_completions(
                original_text=text,
                remaining_text=remaining_text,
                operation=operation,
            )
        return self._get_completion(
            original_text=text, remaining_text=remaining_text, options=operation
        )

    def _extract_operation(self, words):
        """Get the required client operation and separate it from the remaining text."""
        operation = self.client
        operation_map = operation._operation_map
        oper_ids = [o for o in operation_map]
        words_len = len(words)

        if not words_len:
            return oper_ids, "", False

        word = words[0]
        attr = word if word in oper_ids else None
        if attr is None:
            if words_len == 1:
                return oper_ids, word, False
            elif words_len > 1:
                return [], words[-1], False
        else:
            operation = operation_map.get(word)
            word = words[-1]
            (
                operation,
                rem_text,
                param_req_body_flag,
            ) = self._get_distributed_attr_for_completion(operation, word)
            return operation, rem_text, param_req_body_flag

    def _get_distributed_attr_for_completion(self, operation, word):
        param, req_body = [], []
        op_param, op_req_body = operation.parameters, operation.requestBody
        result = []
        rem_text = ""
        param_req_body_flag = True
        if op_param:
            param = [p.name for p in operation.parameters]
        if op_req_body:
            prop = operation.requestBody.content.get("application/json")
            if prop:
                prop_attr = [
                    attr
                    for attr in dir(prop.schema)
                    if attr in IN_USE_SCHEMA_ATTR and getattr(prop.schema, attr)
                ]
                if not prop_attr:
                    return [], "", False
                else:
                    prop_attr = prop_attr[0]
                    allof_attr = IN_USE_SCHEMA_ATTR[0]
                    oneof_attr = IN_USE_SCHEMA_ATTR[1]
                    items_attr = IN_USE_SCHEMA_ATTR[2]
                    properties_attr = IN_USE_SCHEMA_ATTR[3]
                    if prop_attr == allof_attr:
                        prop = prop.schema.allOf[-1].properties
                    elif prop_attr == oneof_attr:
                        prop_list = []
                        for p in prop.schema.oneOf:
                            prop_list.extend([k for k in p["properties"]])
                        prop = prop_list
                    elif prop_attr == items_attr:
                        prop = prop.schema.items
                        # What should we do with this? at the moment we don't have any proper fields
                        # prop = []
                        if prop.properties:
                            prop = prop.properties
                    elif prop_attr == properties_attr:
                        prop = prop.schema.properties
                    else:
                        raise NotImplementedError()
            else:
                prop = operation.requestBody.content[
                    "multipart/form-data"
                ].schema.properties
            if isinstance(prop, list) or isinstance(prop, dict):
                req_body = [
                    p for p in prop
                ]  # all or only required and also without id ??
        if op_param and not op_req_body:
            rem_text = word if bool([p for p in param if p.startswith(word)]) else ""
            result = dict(param=param)
        elif not op_param and op_req_body:
            rem_text = word if bool([p for p in req_body if p.startswith(word)]) else ""
            result = dict(req_body=req_body)
        elif op_param and op_req_body:
            rem_text = (
                word
                if bool([p for p in param + req_body if p.startswith(word)])
                else ""
            )
            result = dict(param=param, req_body=req_body)
        elif not op_param and not op_req_body:
            param_req_body_flag = False
        return result, rem_text, param_req_body_flag

    def _get_operation_attr_completions(self, original_text, remaining_text, operation):
        """Get suggestions based on operation and remaining text."""
        completion_offset = 0
        param_add_str, req_body_add_str = "--", "--body"

        # Strip argument prefix
        if remaining_text.startswith(param_add_str):

            if len(remaining_text.split("=")) == 2:
                # Already a valid param
                remaining_text = ""

            else:
                remaining_text = remaining_text[2:]
                completion_offset = 2

        if self.should_hide_completions(
            original_text=original_text,
            remaining_text=remaining_text,
            allowed_suffixes=(" ", "-"),
        ):
            return []

        result = []
        for k in operation:
            l = []
            if k == "param":
                s = param_add_str
                l = [
                    (s + attribute, len(remaining_text) + completion_offset)
                    for attribute in operation[k]
                    if attribute.startswith(remaining_text)
                    and not attribute.startswith("_")
                ]
            elif k == "req_body":
                s = req_body_add_str
                l = [
                    (s + "." + attribute, len(remaining_text) + completion_offset)
                    for attribute in operation[k]
                    if attribute.startswith(remaining_text)
                    and not attribute.startswith("_")
                ]
                if not l:
                    l = [(s, len(remaining_text) + completion_offset)]
            result.extend(l)

        return result

    def _get_completion(self, original_text, remaining_text, options):
        """Get completion properties based on text and possible options."""
        if self.should_hide_completions(
            original_text=original_text,
            remaining_text=remaining_text,
            allowed_suffixes=(" ", "."),
        ):
            return []

        return [
            (option, len(remaining_text))
            for option in options
            if option.startswith(remaining_text) and not option.startswith("_")
        ]

    @staticmethod
    def should_hide_completions(original_text, remaining_text, allowed_suffixes):
        return (
            original_text
            and not remaining_text
            and original_text[-1] not in allowed_suffixes
        )
