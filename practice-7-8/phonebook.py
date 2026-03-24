import sys
from typing import Any
from time import sleep
from pathlib import Path
from subprocess import run
from re import match, findall
from csv import DictReader, Error
from psycopg2 import DatabaseError
from connection import create_connection

PATH = Path(__file__).parent

COMMAND = "cls" if sys.platform == "win32" else "clear"

class PhoneBook:
    def __init__(self) -> None:
        self.clear_terminal()
        self.connection = create_connection()
        self.connection.autocommit = True
        self.pause_terminal(2)
        self.create_query("default", [])

    def main_page(self) -> None:
        try:
            self.clear_terminal()
            print("=== WELCOME TO THE \"PHONEBOOK\" ===")
            option = abs(int(input("\n\033[1;4mCHOOSE ONE OF THE GIVEN OPTIONS:\033[0m\n\n1 - CREATE\n2 - READ\n3 - UPDATE\n4 - DELETE\n5 - EXIT\n\n>> ").strip()))
            match option:
                case 1:
                    self.clear_terminal()
                    print("=== CREATE ===")
                    mode = abs(int(input("\n\033[1;4mCHOOSE ONE OF THE GIVEN OPTIONS:\033[0m\n\n1 - AUTOMATICALLY FROM '.CSV' FILE\n2 - MANUALLY VIA TERMINAL\n\n>> ").strip()))
                    match mode:
                        case 1:
                            self.create_query("create", self.parse_csv())
                        case 2:
                            self.create_query("create", self.parse_input("create"))
                        case _:
                            raise Exception
                case 2:
                    self.create_query("read", self.parse_input("read"))
                case 3:
                    self.create_query("update", self.parse_input("update"))
                case 4:
                    self.create_query("delete", self.parse_input("delete"))
                case 5:
                    sys.exit(1)
                case _:
                    raise Exception
            self.main_page()
        except (ValueError, Exception):
            self.handle_result("failure", "inapproriate input")
            self.main_page()

    def create_query(self, type: str, arguments: list[list[str]] | list[Any]) -> None:
        del self.connection.notices[:]
        match type:
            case "create":
                query = f"""
                        CALL create_contacts(ARRAY {arguments});
                        """
            case "read":
                query = f"""
                        SELECT read_contacts({arguments[0]}, '{arguments[1]}', '{arguments[2]}', {arguments[3]}, {arguments[4]}, {arguments[5]}, {arguments[6]});
                        """
            case "update":
                query = f"""
                        CALL update_contacts(ARRAY {arguments});
                        """
            case "delete":
                query = f"""
                        CALL delete_contacts(ARRAY {arguments});
                        """
            case "default":
                query = """
                        CREATE TABLE IF NOT EXISTS phonebook (
                            firstname VARCHAR(31) NOT NULL,
                            lastname VARCHAR(31) NOT NULL,
                            number VARCHAR(31) NOT NULL,
                            address VARCHAR(31) NOT NULL
                        );
                        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                if cursor.statusmessage == "CREATE TABLE":
                    self.handle_result("success", "initialized the table")
                elif type == "read":
                    self.clear_terminal()
                    result = cursor.fetchall()
                    if result:
                        print(f"{f" TOTAL NUMBER OF THE RECORDS: {len(result)} ":=^137}")
                        print("┌" + "─" * 33 + "┬" + "─" * 33 + "┬" + "─" * 33 + "┬" + "─" * 33 + "┐")
                        print("│" + f"{"\033[1mFirst Name\033[0m":^41}" + "│" + f"{"\033[1mLast Name\033[0m":^41}" + "│" + f"{"\033[1mNumber\033[0m":^41}" + "│" + f"{"\033[1mAddress\033[0m":^41}" + "│")
                        print("├" + "─" * 33 + "┼" + "─" * 33 + "┼" + "─" * 33 + "┼" + "─" * 33 + "┤")
                        for items in result:
                            item = items[0][1:(len(items[0])-1)].strip().replace('"', '').split(",")
                            print("│ " + f"{item[0]:<31}" + " │ " f"{item[1]:<31}" + " │ " + f"{item[2]:<31}" + " │ " f"{item[3]:<31}" + " │")
                            if result.index(items) != len(result) - 1:
                                print("├" + "─" * 33 + "┼" + "─" * 33 + "┼" + "─" * 33 + "┼" + "─" * 33 + "┤")
                            else:
                                print("└" + "─" * 33 + "┴" + "─" * 33 + "┴" + "─" * 33 + "┴" + "─" * 33 + "┘")
                    else:
                        self.handle_result("failure", "not found")
                    _ = input("\n=== PRESS [ENTER] TO CONTINUE ===\n\n>> ").strip()
                else:
                    for notice in self.connection.notices:
                        notice = notice.strip().replace("NOTICE:  ", "").replace("firstname", "first name").replace("lastname", "last name")
                        self.handle_result("success" if "success" in notice else "failure", notice)
        except DatabaseError as error:
            error = str(error).strip().replace(" FATAL: ", "")
            if match(r".+(?=\n[A-Z]+)", error):
                error = findall(r".+(?=\n[A-Z]+)", error)[0]
            self.handle_result("failure", error)
            sys.exit(1)

    def parse_csv(self) -> list[list[str]]:
        try:
            with open(file=f"{PATH}/contacts.csv", mode="r", newline="") as file:
                array = DictReader(file)
                data = []
                for element in array:
                    data.append([element["firstname"], element["lastname"], element["number"], element["address"]])
                return data
        except Error as error:
            self.handle_result("failure", str(error).strip())
            sys.exit(1)
        
    def parse_input(self, type: str) -> list[list[str]] | list[Any]:
        try:
            self.clear_terminal()
            count = abs(int(input("=== ENTER THE NUMBER OF RECORDS ===\n\n>> ").strip()))
            if count == 0:
                count += 1
            data = []
            fileds = {1: "first name", 2: "last name", 3: "number", 4: "address"}
            for index in range(count):
                self.clear_terminal()
                match type:
                    case "create":
                        information = input(f"=== ENTER THE #{index + 1} CONTACT'S INFORMATION ===\n\n>> ").strip().split(",")
                        if len(information) == 4:
                            data.append(information)
                        else:
                            continue
                    case "read":
                        search_column, search_pattern, page_number, page_size = "0", "0", "0", "0"
                        with_filter = bool(abs(int(input("=== ENTER 0 (WITHOUT FILTER) OR 1 (WITH FILTER) ===\n\n>> ").strip())))
                        if with_filter:
                            self.clear_terminal()
                            print("=== READ ===")
                            option = abs(int(input(f"\n\033[1;4mCHOOSE ONE OF THE GIVEN OPTIONS:\033[0m\n\n1 - FIRST NAME\n2 - LAST NAME\n3 - NUMBER\n4 - ADDRESS\n\n>> ").strip()))
                            if option > 0 and option < 5:
                                search_column = fileds[option].replace(" ", "")
                            self.clear_terminal()
                            search_pattern = input("=== ENTER PATTERN ===\n\n>> ").strip()
                        self.clear_terminal()
                        with_reverse = bool(abs(int(input("=== ENTER 0 (ASCENDING) OR 1 (DESCENDING) ===\n\n>> ").strip())))
                        self.clear_terminal()
                        with_pagination = bool(abs(int(input("=== ENTER 0 (WITHOUT PAGINATION) OR 1 (WITH PAGINATION) ===\n\n>> ").strip())))
                        if with_pagination:
                            self.clear_terminal()
                            page_number = input("=== ENTER NUMBER OF THE PAGE ===\n\n>> ").strip()
                            self.clear_terminal()
                            page_size = input("=== ENTER SIZE OF THE PAGE ===\n\n>> ").strip()
                        data = [with_filter, search_column, search_pattern, with_reverse, with_pagination, page_number, page_size]
                        break
                    case "update":
                        number = input(f"=== ENTER THE #{index + 1} CONTACT'S NUMBER ===\n\n>> ").strip()
                        self.clear_terminal()
                        print("=== UPDATE ===")
                        option = abs(int(input(f"\n\033[1;4mCHOOSE ONE OF THE GIVEN OPTIONS:\033[0m\n\n1 - FIRST NAME\n2 - LAST NAME\n3 - NUMBER\n4 - ADDRESS\n\n>> ").strip()))
                        if option > 0 and option < 5:
                            self.clear_terminal()
                            information = input(f"=== ENTER THE #{index + 1} CONTACT'S NEW {fileds[option].upper()} ===\n\n>> ").strip()
                            data.append([number, fileds[option].replace(" ", ""), information])
                        else:
                            continue
                    case "delete":
                        number = input(f"=== ENTER THE #{index + 1} CONTACT'S NUMBER ===\n\n>> ").strip()
                        if len(number) > 0:
                            data.append(number)
                        else:
                            continue
            if data:
                return data
            else:
                raise Exception
        except (ValueError, Exception):
            self.handle_result("failure", "inappropriate input")
            self.main_page()

    def handle_result(self, type: str, text: str) -> None:
        self.clear_terminal()
        match type:
            case "success":
                print(f"\033[92m[{text}]\033[0m\n")
            case "failure":
                print(f"\033[91m[{text}]\033[0m\n")
        self.pause_terminal(2)

    def clear_terminal(self) -> None:
        run(COMMAND)
        print("\n")
        run(COMMAND)

    def pause_terminal(self, seconds: int) -> None:
        sleep(seconds)

def execute_program() -> None:
    phone_book = PhoneBook()
    phone_book.main_page()

if __name__ == "__main__":
    execute_program()
