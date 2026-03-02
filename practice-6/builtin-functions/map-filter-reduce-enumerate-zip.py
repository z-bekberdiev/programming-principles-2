from functools import reduce
from typing import Any


class Builtin_Functions:
    def __init__(self, array: list[str]) -> None:
        self.array: list[str] = array

    def map_and_filter(self) -> None:
        self.array: list[int] = list(map(int, self.array))
        print(f"Sum of the array: {sum(self.array)}")
        print()
        self.array: list[int] = list(filter(lambda number: number if number % 3 == 0 else 0, self.array))
        print("The filtered array (all numbers that are divisible by 3): ", end="")
        print(*self.array, sep=", ")
        print()

    def functools_reduce(self) -> None:
        self.total_sum: int = reduce(lambda x, y: x + y, self.array)
        print(f"Total sum of the filtered array: {self.total_sum}")
        print()

    def enumerate_and_zip(self) -> None:
        self.string: str = "Hello World I'm gonna sleep Goodbye".split()
        self.array: list[str] = ["Friend", "Championship", "Genius", "study", "so long", "Python"]
        for word in enumerate(self.string):
            print("Index " + str(word[0]) + ": " + word[1])
        print()
        print(*[element[0] + " " + element[1] for element in list(zip(self.string, self.array))], sep=", ")
        print()

    def type_checking_and_converion(self) -> None:
        self.variable: int = 10
        print("This is an integer!" if isinstance(self.variable, int) else "This is something else...")
        self.item: list[Any] = []
        print()
        print("This is an integer!" if isinstance(self.item, int) else "This is something else...")
        print()
        print(f"Int to Str: {type(str(self.variable))}")
        print()


def main() -> None:
    builtin_functions: Builtin_Functions = Builtin_Functions(input().strip().split())
    builtin_functions.map_and_filter()
    builtin_functions.functools_reduce()  # Algorithm: ((3 + 6) + 9) = 18, not just 3 + 6 + 9 = 18
    builtin_functions.enumerate_and_zip()
    builtin_functions.type_checking_and_converion()


if __name__ == "__main__":
    main()