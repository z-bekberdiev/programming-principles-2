# I decided to import following modules due to the several reasons:
import os  # to use mkdir(), exists(), remove() functions
import time  # to use sleep() function
import shutil  # to implement copy() function
from pathlib import Path  # to get the relevant directory


class Copy_Delete_Files:
    def __init__(self, file_path: str, mode: str) -> None:
        self.file_path: str = file_path
        self.mode: str = mode

    def process_action(self) -> None:
        match self.mode:
            case "copy":
                self.new_file_path: str = self.file_path.replace("/text-file.txt", "/backup-storage")
                os.mkdir(self.new_file_path)
                shutil.copy(self.file_path, self.new_file_path)
                print("File was successfully copied!")
            case "delete":
                if os.path.exists(self.file_path):
                    os.remove(self.file_path)
                    print("File was successfully deleted!")
                else:
                    print("Oops! There is no such file. Try again!")
            case _:
                print("Wrong mode. Try again.")


def main() -> None:
    copy_file: Copy_Delete_Files = Copy_Delete_Files(f"{Path(__file__).parent}/text-file.txt", "copy")
    delete_file: Copy_Delete_Files = Copy_Delete_Files(f"{Path(__file__).parent}/text-file.txt", "delete")
    copy_file.process_action()
    time.sleep(5)
    delete_file.process_action()


if __name__ == "__main__":
    main()