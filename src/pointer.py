"""Ths module includes the PointerClass class.

PointerClass is a parent class for all classes that need to iterate over items 
using a pointer.
"""

from typing import Generic, TypeVar, Sequence

T = TypeVar("T")


class PointerClass(Generic[T]):
    """
    A parent class for all classes that need to iterate over items using a 
    pointer.

    Attributes:
        items(Sequence[T]): A sequence of the items to be iterated over.
        pointer(int): The pointer, that stores the index of the current item.

    """
    items: Sequence[T]
    pointer: int

    def __init__(self, items: Sequence[T]) -> None:
        """
        Initialize a PointerClass object.

        Parameters:
            items: A sequence of the items to be iterated over.
            pointer: The pointer, that stores the index of the current item.
        """
        self.items = items
        self.pointer = 0

    def peek(self, amount: int = 0) -> T | None:
        """
        Get any item relative to the pointer, the current by default.

        Parameters:
            amount: The offset from the pointer at which to get the item from.

        Returns:
            item(T | None): The item at the given location, None if the index is
              invalid.
        """
        if self.pointer+amount > len(self.items)-1:
            return None
        return self.items[self.pointer+amount]

    def consume(self) -> T | None:
        """
        Get the current item and move to the next.

        Returns the item the pointer is pointing to, and increments the pointer 
        by 1.

        Returns:
            item(T | None): The current item
        """
        # If the pointer is beyond the end of items, return None and don't
        # increment to keep the equals check working.
        if self.pointer == len(self.items):
            return None
        self.pointer += 1
        return self.items[self.pointer-1]
