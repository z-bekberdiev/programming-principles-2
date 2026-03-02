from pathlib import Path


class File_Reader:
    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path

    def __format__(self, format_spec: str) -> str:
        match format_spec:
            case "red":
                return f"\033[31m{self.content}\033[0m"
            case "yellow":
                return f"\033[33m{self.content}\033[0m"
            case "green":
                return f"\033[32m{self.content}\033[0m"
            case _:
                return "Wrong format specifier. Try again."

    def read_file(self) -> None:
        with open(self.file_path) as file:
            self.content: str = "".join(file.readlines())


def main() -> None:
    path_to_file: Path = Path(__file__).parent / "text-file.txt"
    file_reader: File_Reader = File_Reader(path_to_file)
    file_reader.read_file()
    print(f"{file_reader:red}")
    print()
    print(f"{file_reader:yellow}")
    print()
    print(f"{file_reader:green}")
    print()


if __name__ == "__main__":
    main()