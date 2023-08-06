import json
import tabulate
from tabulate import _text_type, _binary_type, _strip_invisible

JSON = "json"
TABLE = "table"


def _format_ext(val, valtype, floatfmt, missingval="", has_invisible=True):
    """Format a value accoding to its type.

    Unicode is supported:

    >>> hrow = ['\u0431\u0443\u043a\u0432\u0430', '\u0446\u0438\u0444\u0440\u0430'] ; \
        tbl = [['\u0430\u0437', 2], ['\u0431\u0443\u043a\u0438', 4]] ; \
        good_result = '\\u0431\\u0443\\u043a\\u0432\\u0430      \\u0446\\u0438\\u0444\\u0440\\u0430\\n-------  -------\\n\\u0430\\u0437             2\\n\\u0431\\u0443\\u043a\\u0438           4' ; \
        tabulate(tbl, headers=hrow) == good_result
    True

    """
    if val is None:
        return missingval

    if valtype in [int, _text_type]:
        if type(val) == str:
            if len(val) > 30:
                val = "{0}..".format(val[0:30])
        elif isinstance(val, list):
            list_str = str(val)
            if len(list_str) > 30:
                return f"{list_str[:30]}...]"
        return "{0}".format(val)
    elif isinstance(val, list):
        return str(val)[:30] + "..."
    elif valtype is _binary_type:
        try:
            return _text_type(val, "ascii")
        except TypeError:
            return _text_type(val)
    elif valtype is float:
        is_a_colored_number = has_invisible and isinstance(
            val, (_text_type, _binary_type)
        )
        if is_a_colored_number:
            raw_val = _strip_invisible(val)
            formatted_val = format(float(raw_val), floatfmt)
            return val.replace(raw_val, formatted_val)
        else:
            return format(float(val), floatfmt)
    else:
        return "{0}".format(val)


tabulate._format = _format_ext


def to_table(response):
    """Convert raw response into table output."""
    if not response:
        return response

    # Tabulate dictionary responses
    if isinstance(response, dict):
        return tabulate.tabulate(
            [(key, value) for key, value in response.items()],
            headers={"Field": "Field", "Value": "Value"},
            tablefmt="grid",
        )

    # Tabulate list responses
    if isinstance(response, list):
        return tabulate.tabulate(
            response,
            headers={key: key.capitalize() for key in response[0].keys()},
            tablefmt="grid",
        )


def to_json(response):
    """Convert raw response into json output."""
    return json.dumps(response, indent=2)


FORMATTERS = {
    JSON: to_json,
    TABLE: to_table,
}


def format_response(response, output_format):
    return "\n{}\n".format(FORMATTERS[output_format](response))
