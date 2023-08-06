"""Pretty reducing huge Python objects to visualise them nicely."""
from pprint import pformat
from typing import Any, Dict


class Dots(dict):  # type: ignore # inherit from dict to blend with expected type
    """Show dots inside Python objects repr."""

    def __repr__(self) -> str:
        """Show dots."""
        return ".."


def ellipsize(
    obj: Any,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> Any:
    """Reduce huge list/dict to show on screen.

    In lists (including dict items) show only 1st `max_list_items_to_show`
    and add ".." if there is more.
    Limit max dict/list length at max_item_length.

    Args:
        obj: Python object to ellipsize
        max_items_to_show: if List or Dict in obj (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and his string representation longer than show ".." instead of the rest of it
    """
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, list):
        if len(obj) == 0:
            return obj
        if isinstance(obj[0], dict):  # Heuristic to pretty show list of dicts with huge items
            result_list = [
                ellipsize(
                    val,
                    max_items_to_show=max_items_to_show,
                    max_item_length=max_item_length,
                )
                for val in obj[:max_items_to_show]
            ]
            if len(obj) > max_items_to_show:
                result_list.append(Dots())
            return result_list
        result = [
            ellipsize(
                item,
                max_items_to_show=max_items_to_show,
                max_item_length=max_item_length,
            )
            for item in obj[:max_items_to_show]
        ]
        if len(obj) > max_items_to_show:
            result.append(Dots())
        return result

    if isinstance(obj, dict):
        result_dict: Dict[str, Any] = {}
        for key, val in obj.items():
            result_dict[key] = ellipsize(
                val, max_items_to_show=max_items_to_show, max_item_length=max_item_length
            )
        return result_dict
    suffix = ".." if len(str(obj)) > max_item_length else ""
    return str(obj)[:max_item_length] + suffix


def format_ellipsized(
    obj: Any,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> str:
    """Pformat ellipsized `obj`.

    Use [pprint.pformat](https://docs.python.org/3/library/pprint.html)
    to convert ellipsize result into string

    Args:
        obj: Python object to ellipsize
        max_items_to_show: if List or Dict in obj (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and his string representation longer than show ".." instead of the rest of it
    """
    return pformat(
        ellipsize(obj, max_items_to_show=max_items_to_show, max_item_length=max_item_length)
    )


def print_ellipsized(
    *objs: Any,
    max_items_to_show: int = 10,
    max_item_length: int = 1024,
    **kwargs: Any,
) -> None:
    """Print ellipsized `obj` with [pprint](https://docs.python.org/3/library/pprint.html).

    Can print many objects, like general print.
    Pass args to print like [end](https://realpython.com/lessons/sep-end-and-flush/).

    Args:
        objs: Python objects to ellipsize
        max_items_to_show: if List or Dict in objs (including nested) has more items,
            then show ".." instead of the rest items
        max_item_length: if List's or Dict's item are not another List/Dict
            and his string representation longer than show ".." instead of the rest of it
    """
    print(
        *[
            pformat(
                ellipsize(
                    obj,
                    max_items_to_show=max_items_to_show,
                    max_item_length=max_item_length,
                )
            )
            for obj in objs
        ],
        **kwargs,
    )
