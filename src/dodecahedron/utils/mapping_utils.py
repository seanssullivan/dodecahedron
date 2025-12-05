# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
from typing import Any
from typing import Hashable
from typing import List
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Sequence
from typing import Union

__all__ = [
    "deep_get",
    "deep_set",
]


def deep_get(
    __m: Union[Mapping[Hashable, Any], Sequence[Any]],
    /,
    key: Union[str, Sequence[str]],
    default: Optional[object] = None,
) -> Any:
    """Get value from nested mapping object.

    Args:
        __d: Mapping object.
        key: Key(s) seperated by periods or in a sequence.
        default (optional): Default when value not found. Default ``None``.

    Returns:
        Value of key in nested mapping object.

    Raises:
        TypeError: when argument is not a mapping.

    """

    def _get_item(o: Any, k: str) -> Any:
        """Get item from object.

        Args:
            o: Object.
            key: Key for which to get value.

        Returns:
            Value.

        """
        try:
            result = o[k] if not k.isdigit() else o[int(k)]

        except (IndexError, KeyError):
            return o[_standardize_key(k)]

        return result

    def _get(o: Any, k: str) -> Any:
        """Get value of key from object.

        Args:
            o: Object.
            k: Key for which to get value.

        Returns:
            Value.

        """
        try:
            result = _get_item(o, k)

        except (IndexError, KeyError, TypeError):
            return default

        return result

    if not isinstance(__m, (Mapping, Sequence)):  # type: ignore
        message = f"expected mapping or sequence, got {type(__m)} instead"
        raise TypeError(message)

    if not isinstance(key, (str, Sequence)):  # type: ignore
        message = f"expected type 'str', got {type(key)} instead"
        raise TypeError(message)

    keys: List[str] = key.split(".") if isinstance(key, str) else list(key)
    result = functools.reduce(_get, keys, __m)
    return result


def deep_set(
    __m: Union[MutableMapping[Hashable, Any], Sequence[Any]],
    /,
    key: Union[str, Sequence[str]],
    value: Any,
) -> Union[MutableMapping[Hashable, Any], Sequence[Any]]:
    """Sets key to value in nested mapping object.

    Args:
        __m: Mapping.
        key: Key(s) seperated by periods or a sequence of keys.
        value: Value to set for key.

    Returns:
        Updated mutable mapping object.

    Raises:
        TypeError: when argument is not mutable mapping.

    """

    def _set_item(o: Any, k: str, v: Any) -> None:
        """Set value of key on object.

        Args:
            o: Object.
            k: Key.
            v: Value.

        """
        if isinstance(o, dict):
            o[k] = v

        if isinstance(o, list) and k.isdigit():
            o[int(k)] = v

        if isinstance(o, list) and not k.isdigit():
            raise KeyError(k)

        if not isinstance(o, (dict, list)):
            raise KeyError(k)

    if not isinstance(__m, (MutableMapping, Sequence)):  # type: ignore
        expected = "expected mutable mapping or sequence"
        actual = f"got {type(__m)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)

    keys: List[str] = key.split(".") if isinstance(key, str) else list(key)

    try:
        k, remaining = keys[0], keys[1:]
        v = (
            deep_set(deep_get(__m, k) or {}, remaining, value)
            if len(remaining) >= 1
            else value
        )
        _set_item(__m, k, v)

    except KeyError as error:
        raise KeyError(f"{k}.{error.args[0]}") from error  # type: ignore

    except (IndexError, TypeError) as error:
        raise KeyError(keys[0]) from error

    return __m


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def _standardize_key(__k: str, /) -> str:
    """Standardize key.

    Args:
        k: Key.

    Returns:
        Key.

    """
    if __k.startswith("'") and __k.endswith("'"):
        return __k.strip("'")

    if __k.startswith('"') and __k.endswith('"'):
        return __k.strip('"')

    if __k.startswith("[") and __k.endswith("]"):
        return __k.strip("[").strip("]")

    if __k.startswith("(") and __k.endswith(")"):
        return __k.strip("(").strip(")")

    if __k.startswith("<") and __k.endswith(">"):
        return __k.strip("<").strip(">")

    return __k
