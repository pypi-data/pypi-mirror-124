from typing import Any, Dict


def _dict_exclude_none(input: Dict[Any, Any]) -> Dict[Any, Any]:
    """Exclude items from a Dict where the value is None.

    This is used for OPML elements' `to_json` function so the output
    doesn't contain a bunch of null values."""

    return dict((k, v) for k, v in input.items() if v is not None)
