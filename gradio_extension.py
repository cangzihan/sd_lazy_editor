from enum import Enum


class _Keywords(Enum):
    NO_VALUE = "NO_VALUE"  # Used as a sentinel to determine if nothing is provided as a argument for `value` in `Component.update()`
    FINISHED_ITERATING = "FINISHED_ITERATING"  # Used to skip processing of a component's value (needed for generators + state)


# 新版本的gradio没有gr.Dropdown.update方法，用以下函数代替
def gr_Dropdown_update(
    value=_Keywords.NO_VALUE,
    choices=None,
    label=None,
    show_label=None,
    interactive=None,
    placeholder=None,
    visible=None,
):
    return {
        "choices": choices,
        "label": label,
        "show_label": show_label,
        "visible": visible,
        "value": value,
        "interactive": interactive,
        "placeholder": placeholder,
        "__type__": "update",
    }


def gr_Slider_update(minimum=None, maximum=None, value=None):
    return {
        "minimum": minimum,
        "maximum": maximum,
        "value": value if value is not None else maximum,
        "__type__": "update",
    }
