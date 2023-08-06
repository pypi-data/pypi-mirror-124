from typing import Any, Optional, TypeVar

T = TypeVar("T")


class IllegalStateException(Exception):
    pass


class IllegalArgumentException(Exception):
    pass


def checkArgument(
    expression: bool, errorMessageTemplate: Optional[str] = None, *errorMessageArgs: Any
) -> None:
    "Ensures the truth of an expression involving one or more parameters to the calling method."

    if not expression:
        raise IllegalStateException(
            errorMessageTemplate.format(errorMessageArgs)
            if errorMessageTemplate
            else None
        )


def checkElementIndex(index: int, size: int, desc: str = None) -> int:
    "Ensures that index specifies a valid element in an array, list or string of size size."

    if index < 0 or index > (size - 1):
        raise IllegalStateException(desc)

    return index


def checkNotNull(
    reference: Optional[T], errorMessageTemplate: str, *errorMessageArgs: Any
) -> T:
    "Ensures that an object reference passed as a parameter to the calling method is not null."

    if not reference:
        raise IllegalArgumentException(
            errorMessageTemplate.format(errorMessageArgs)
            if errorMessageTemplate
            else None
        )

    return reference


def checkPositionIndex(index: int, size: int, desc: str = None) -> int:
    "Ensures that index specifies a valid position in an array, list or string of size size."

    return checkElementIndex(index, size, desc)


def checkPositionIndexes(start: int, end: int, size: int) -> None:
    "Ensures that start and end specify a valid positions in an array, list or string of size size, and are in order."

    if start < 0:
        raise IllegalStateException()
    elif start > end:
        raise IllegalStateException()
    else:
        checkElementIndex(end, size)


def checkState(
    expression: bool, errorMessageTemplate: str = None, *errorMessageArgs: Any
) -> None:
    "Ensures the truth of an expression involving the state of the calling instance, but not involving any parameters to the calling method."

    if not expression:
        raise IllegalStateException(
            errorMessageTemplate.format(errorMessageArgs)
            if errorMessageTemplate
            else None
        )
