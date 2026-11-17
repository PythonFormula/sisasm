from typing import Generic, TypeVar, Sequence

T = TypeVar("T")


class PointerClass(Generic[T]):
    items: Sequence[T]
    pointer: int

    def __init__(self, items: Sequence[T]) -> None:
        self.items = items
        self.pointer = 0

    def peek(self, amount: int = 0) -> T | None:
        if self.pointer+amount > len(self.items)-1:
            return None
        return self.items[self.pointer+amount]

    def consume(self) -> T | None:
        if self.pointer == len(self.items):
            return None
        self.pointer += 1
        return self.items[self.pointer-1]
