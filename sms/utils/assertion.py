"""Utility module for assertion."""

# official libraries
from typing import T


__all__ = (
        'is_dict',
        'is_instance',
        'is_int',
        'is_list',
        'is_str',
        'is_tuple',
        )


def is_dict(val: dict) -> dict:
    """Assertion for a dictionary type value.

    Args:
        val: check value (expect dict type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match a dict type.
    """
    assert isinstance(val, dict), f"Must be a Dioctonary type value!: {type(val)}"
    return val


def is_instance(val: T, a_type: T) -> T:
    """Assertion for any type value (e.g. Class instance, data class)

    Args:
        val: check value (expect object type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match the type.
    """
    assert isinstance(val, a_type), f"Must be a {a_type} value!: {type(val)}"
    return val


def is_int(val: int) -> int:
    """Assertion for an integer type value.

    Args:
        val: check value (expect int type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match an integer type.
    """
    assert isinstance(val, int), f"Must be a Integer type value!: {type(val)}"
    return val


def is_list(val: list) -> list:
    """Assertion for a list type value.

    Args:
        val: check value (expect list type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match a list type.
    """
    assert isinstance(val, list), f"Must be a List type value!: {type(val)}"
    return val


def is_str(val: str) -> str:
    """Assertion for a string type value.

    Args:
        val: check value (expect string type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match a string type.
    """
    assert isinstance(val, str), f"Must be a String type value!: {type(val)}"
    return val


def is_tuple(val: tuple) -> tuple:
    """Assertion for a tuple type value.

    Args:
        val: check value (expect tuple type)

    Returns:
        Same value to input.

    Raises:
        Assertion Error: if a value not match a tuple type.
    """
    assert isinstance(val, tuple), f"Must be a Tuple type value!: {type(val)}"
    return val
