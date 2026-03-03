import re
import subprocess


class Regex_Exercises:
    def __init__(self) -> None:
        subprocess.run("clear")
        print("\n")
        subprocess.run("clear")
        print("\033[1;4mMy solutions to the given exercises are provided below:\033[0m")
        print()

    def task_1(self, string: str) -> None:
        if re.match(r"[a-zA-Z]*ab*[a-zA-Z]*", string):
            print("String satisfies the condition.")
        else:
            print("Inappropriate string usage.")
        print()

    def task_2(self, string: str) -> None:
        if re.match(r"[a-zA-Z]*ab{2,3}[a-zA-Z]*", string):
            print("String satisfies the condition.")
        else:
            print("Inappropriate string usage.")
        print()

    def task_3(self, string: str) -> None:
        print("The sequences of lower case letters joined with an underscore: ", end="")
        print(*re.findall(r"[a-z]+_[a-z]+", string), sep=", ")
        print()

    def task_4(self, string: str) -> None:
        print("The sequences of an upper case letter followed by lower case letters: ", end="")
        print(*re.findall(r"[A-Z][a-z]+", string), sep=", ")
        print()

    def task_5(self, string: str) -> None:
        if re.match(r".*a.*b$", string):
            print("String satisfies the condition.")
        else:
            print("Inappropriate string usage.")
        print()

    def task_6(self, string: str) -> None:
        print(re.sub(r"\ |\,|\;|\.", ":", string))
        print()

    def task_7(self, string: str) -> None:
        print("".join([word.capitalize() for word in re.split(r"_", string)]))
        print()

    def task_8(self, string: str) -> None:
        print(*re.split(r"[A-Z]+", string), sep=" ")
        print()

    def task_9(self, string: str) -> None:
        print(*re.findall(r"[A-Z][a-z]*|[a-z]+", string), sep=" ")
        print()
    
    def task_10(self, string: str) -> None:
        print("_".join([word.lower() for word in re.findall(r"[A-Z]*[a-z]+", string)]))
        print()


def main() -> None:
    regex_exercises: Regex_Exercises = Regex_Exercises()
    regex_exercises.task_1(input("Enter the string for task #1: ").strip())
    regex_exercises.task_2(input("Enter the string for task #2: ").strip())
    regex_exercises.task_3(input("Enter the string for task #3: ").strip())
    regex_exercises.task_4(input("Enter the string for task #4: ").strip())
    regex_exercises.task_5(input("Enter the string for task #5: ").strip())
    regex_exercises.task_6(input("Enter the string for task #6: ").strip())
    regex_exercises.task_7(input("Enter the string for task #7: ").strip())
    regex_exercises.task_8(input("Enter the string for task #8: ").strip())
    regex_exercises.task_9(input("Enter the string for task #9: ").strip())
    regex_exercises.task_10(input("Enter the string for task #10: ").strip())


if __name__ == "__main__":
    main()


# 1. Write a Python program that matches a string that has an 'a' followed by zero or more 'b'

# 2. Write a Python program that matches a string that has an 'a' followed by two to three 'b'

# 3. Write a Python program to find the sequences of lower case letters joined with an underscore

# 4. Write a Python program to find the sequences of an upper case letter followed by lower case letters

# 5. Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'

# 6. Write a Python program to replace all occurrences of space, comma, semicolon, or dot with a colon

# 7. Write a Python program to convert snake case string to camel case string

# 8. Write a Python program to split a string at uppercase letters

# 9. Write a Python program to insert spaces between words starting with capital letters

# 10. Write a Python program to convert camel case string to snake case string