from pathlib import Path


class File_Writer:
    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path

    def write_file(self) -> None:
        with open(self.file_path, "w") as file:
            self.content: str = """Lorem ipsum dolor sit amet consectetur adipisicing elit. Aperiam accusantium eum quis libero porro. Fugiat ullam repellat impedit excepturi recusandae obcaecati nostrum! Vel odio ipsum tempore, consequatur culpa laborum excepturi ducimus praesentium distinctio voluptates ut enim quia libero exercitationem, commodi quaerat. In maxime sint ad illum cumque nostrum minus sapiente magnam, quidem tempore debitis commodi explicabo voluptas harum rerum sunt suscipit provident, enim, officia dolorum! Corrupti aspernatur eos beatae recusandae, saepe vel similique cum error laboriosam harum maxime eveniet repudiandae quibusdam debitis id neque deleniti consequatur tempore esse aperiam blanditiis praesentium, accusantium fugit? Facilis repellendus sapiente, voluptatibus dignissimos voluptates soluta."""
            file.write(self.content)

        with open(self.file_path, "a") as file:
            self.content: str = "Append a new sentence to text file content."
            file.write("\n" + self.content)


def main() -> None:
    path_to_file: Path = Path(__file__).parent / "text-file.txt"
    file_writer: File_Writer = File_Writer(path_to_file)
    file_writer.write_file()


if __name__ == "__main__":
    main()