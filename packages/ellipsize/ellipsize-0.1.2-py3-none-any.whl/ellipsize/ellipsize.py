"""Pretty reducing huge Python objects to visualise them nicely."""
from pprint import pformat, pprint
from typing import Any, Dict


class Dots(dict):  # type: ignore # inherit from dict to blend with expected type
    """Show dots inside Python objects repr."""

    def __repr__(self) -> str:
        """Show dots."""
        return ".."


def ellipsize(
    obj: Any,
    max_list_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> Any:
    """Reduce huge list/dict to show on screen.

    In lists (including dict items) show only 1st `max_list_items_to_show`
    and add ".." if there is more.
    Limit max dict/list length at max_item_length.
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
                    max_list_items_to_show=max_list_items_to_show,
                    max_item_length=max_item_length,
                )
                for val in obj[:max_list_items_to_show]
            ]
            if len(obj) > max_list_items_to_show:
                result_list.append(Dots())
            return result_list
        result = [
            ellipsize(
                item,
                max_list_items_to_show=max_list_items_to_show,
                max_item_length=max_item_length,
            )
            for item in obj[:max_list_items_to_show]
        ]
        if len(obj) > max_list_items_to_show:
            result.append(Dots())
        return result

    if isinstance(obj, dict):
        result_dict: Dict[str, Any] = {}
        for key, val in obj.items():
            result_dict[key] = ellipsize(
                val, max_list_items_to_show=max_list_items_to_show, max_item_length=max_item_length
            )
        return result_dict
    suffix = ".." if len(str(obj)) > max_item_length else ""
    return str(obj)[:max_item_length] + suffix


def ellipsize_format(
    obj: Any,
    max_list_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> str:
    """Use pprint.pformat for convert ellipsize result into string."""
    return pformat(
        ellipsize(
            obj, max_list_items_to_show=max_list_items_to_show, max_item_length=max_item_length
        )
    )


def ellipsize_print(
    obj: Any,
    max_list_items_to_show: int = 10,
    max_item_length: int = 1024,
) -> None:
    """Use pprint to print ellipsize result."""
    pprint(
        ellipsize(
            obj, max_list_items_to_show=max_list_items_to_show, max_item_length=max_item_length
        )
    )
