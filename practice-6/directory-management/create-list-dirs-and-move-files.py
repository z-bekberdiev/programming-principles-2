import os
import shutil
from pathlib import Path


class Directory_Manager:
    def __init__(self, parent_directory: str) -> None:
        self.parent_directory: str = parent_directory

    def create_nested_directories(self) -> None:
        self.path_1: str = self.parent_directory + "/outer-folder"
        os.mkdir(self.path_1)
        file_1 = open(self.path_1 + "/file-1.txt", "x")
        self.path_2: str = self.parent_directory + "/outer-folder" + "/inner-folder"
        os.mkdir(self.path_2)
        file_2 = open(self.path_2 + "/file-2.txt", "x")

    def list_files_and_folders(self) -> None:
        print()
        print(*os.listdir(self.parent_directory), sep="\n")

    def move_copy_between_directories(self) -> None:
        shutil.move(self.path_1 + "/file-1.txt", self.path_2)
        shutil.copy(self.path_2 + "/file-2.txt", self.path_1)

    def find_files_by_extensions(self) -> None:
        self.files: list[str] = []
        for file in os.listdir(self.path_2):
            if file.endswith(".txt"):
                if os.path.isfile(os.path.join(self.path_2, file)):
                    self.files.append(file)

        print()
        print(*self.files, sep=", ")
        print()


def main() -> None:
    directory_manager: Directory_Manager = Directory_Manager(f"{Path(__file__).parent}")
    directory_manager.create_nested_directories()
    directory_manager.list_files_and_folders()
    directory_manager.move_copy_between_directories()
    directory_manager.find_files_by_extensions()


if __name__ == "__main__":
    main()