import sys
import pathlib
import subprocess
import re
import csv
import json
import psycopg2
from psycopg2.extras import Json


class PhoneBook:
    def __init__(self) -> None:
        self.COMMAND = "cls" if sys.platform == "win32" else "clear"
        self.PATH = pathlib.Path(__file__).parent / "assets"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
        self.UNDERLINED = "\033[4m"
        self.RED = "\033[91m"
        self.GREEN = "\033[92m"
        self.YELLOW = "\033[93m"

    def clear_terminal(self) -> None:
        subprocess.run(self.COMMAND)
        print("\n")
        subprocess.run(self.COMMAND)

    def handle_output(self, type: str, text: str) -> None:
        self.clear_terminal()
        print((self.RED if type == "failure" else self.GREEN if type == "success" else self.YELLOW) + f"[{text}]" + self.RESET, end="\n\n")
        _ = input(f"Press {self.BOLD}[Enter]{self.RESET} to continue...")

    def execute_query(self, query: str, arguments: list[bool | str]) -> None | list[tuple[str]]:
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, arguments)
                if "SELECT" in query:
                    output = cursor.fetchall()
                    if not output:
                        raise Exception
                    return output
        except (psycopg2.Error, Exception):
            self.handle_output("failure", "FAILURE: Could not execute query")
            self.start_application()

    def validate_email(self, email: str) -> bool:
        if not bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)):
            self.handle_output("failure", f"FAILURE: Invalid email address ({email})")
            return False
        return True
    
    def validate_birthday(self, birthday: str) -> bool:
        if not bool(re.match(r"^[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$", birthday)):
            self.handle_output("failure", f"FAILURE: Invalid birthday date ({birthday})")
            return False
        return True
    
    def validate_phone(self, phones: list[dict[str, str]]) -> bool:
        for phone in phones:
            if not bool(re.match(r"^\+[0-9]{7,15}$", phone["phone_number"])):
                self.handle_output("failure", f"FAILURE: Invalid phone number ({phone["phone_number"]})")
                return False
            if phone["phone_type"] not in ["Home", "Work", "Mobile"]:
                self.handle_output("failure", f"FAILURE: Invalid phone type ({phone["phone_type"]})")
                return False
        return True

    def enter_using_terminal(self) -> None:
        try:
            self.clear_terminal()
            print(self.BOLD + "===== PhoneBook - Create Contact =====" + self.RESET, end="\n\n")
            data = input("Enter contact's data (name, email, birthday, phone type, phone number, group name) separating by commas: ").strip().split(",")
            data[0] = data[0].strip().title()
            data[1] = data[1].strip().lower()
            data[2] = data[2].strip()
            data[5] = data[5].strip().title()
            if len(data) != 6:
                raise Exception
            data[3:5] = [[{"phone_type": data[3].strip().title(), "phone_number": data[4].strip()}]]
            credentials = [dict(zip(("contact_name", "contact_email", "contact_birthday", "contact_phones", "group_name"), data))]
            if self.validate_email(credentials[0]["contact_email"]) and self.validate_birthday(credentials[0]["contact_birthday"]) and self.validate_phone(credentials[0]["contact_phones"]):
                self.execute_query("CALL create_contact(%s)", [Json(credentials)])
        except Exception:
            self.handle_output("failure", "FAILURE: Invalid data")
            self.start_application()

    def import_from_csv(self) -> list[dict[str, str | list[dict[str, str]]]]:
        try:
            with open(self.PATH / "contacts.csv", "r", newline="") as file:
                self.handle_output("success", "SUCCESS: Imported from CSV")
                result = list(csv.DictReader(file))
                data = [{"contact_name": record["contact_name"], "contact_email": record["contact_email"], "contact_birthday": record["contact_birthday"], "contact_phones": [{"phone_type": record.pop("phone_type"), "phone_number": record.pop("phone_number")}], "group_name": record["group_name"]} for record in result if self.validate_email(record["contact_email"]) and self.validate_birthday(record["contact_birthday"]) and self.validate_phone([{"phone_type": record["phone_type"], "phone_number": record["phone_number"]}])]
                return data
        except (csv.Error, FileNotFoundError):
            self.handle_output("failure", "FAILURE: Could not import from CSV")
            self.start_application()

    def import_from_json(self) -> list[dict[str, str | list[dict[str, str]]]]:
        try:
            with open(self.PATH / "contacts.json", "r", encoding="utf-8") as file:
                self.handle_output("success", "SUCCESS: Imported from JSON")
                result = json.load(file)
                data = [record for record in result if self.validate_email(record["contact_email"]) and self.validate_birthday(record["contact_birthday"]) and self.validate_phone(record["contact_phones"])]
                return data
        except (json.JSONDecodeError, FileNotFoundError):
            self.handle_output("failure", "FAILURE: Could not import from JSON")
            self.start_application()

    def export_to_json(self, data: list[dict[str, str | list[dict[str, str]]]]) -> None:
        try:
            with open(self.PATH / "contacts.json", "w", encoding="utf-8") as file:
                self.handle_output("success", "SUCCESS: Exported to JSON")
                json.dump(data, file, indent=4)
        except (TypeError, KeyError):
            self.handle_output("failure", "FAILURE: Could not export to JSON")
            self.start_application()

    def create_contact(self) -> None:
        try:
            self.clear_terminal()
            print(self.BOLD + "===== PhoneBook - Create Contact =====" + self.RESET, end="\n\n")
            print(self.BOLD + self.UNDERLINED + "Select one of the following options:" + self.RESET, end="\n\n")
            print("1. Enter using terminal")
            print("2. Import from CSV")
            print("3. Import from JSON")
            print("4. Export to JSON")
            print("0. Go back", end="\n\n")
            option = int(input(">> "))
            if not (option > -1 and option < 5):
                raise Exception
            match option:
                case 0:
                    self.start_application()
                case 1:
                    self.enter_using_terminal()
                case 2:
                    self.execute_query("CALL create_contact(%s);", [Json(self.import_from_csv())])
                case 3:
                    self.execute_query("CALL create_contact(%s);", [Json(self.import_from_json())])
                case 4:
                    result = self.execute_query("SELECT * FROM read_contact(%s, %s, %s, %s, %s);", [False, "contact_name", False, "contact_name", "contact_name"])
                    data = [dict(zip(("contact_name", "contact_email", "contact_birthday", "contact_phones", "group_name"), record[1:])) for record in result]
                    self.export_to_json(data)
        except (ValueError, Exception):
            self.handle_output("failure", "FAILURE: Invalid option")
            self.create_contact()

    def update_contact(self) -> None:
        try:
            self.clear_terminal()
            print(self.BOLD + "===== PhoneBook - Update Contact =====" + self.RESET, end="\n\n")
            data = input("Enter contact's data (id, name, email, birthday, phone type, phone number, group name) separating by commas: ").strip().split(",")
            if len(data) != 7:
                raise Exception
            data[1] = data[1].strip().title()
            data[2] = data[2].strip().lower()
            data[3] = data[3].strip()
            data[6] = data[6].strip().title()
            data[4:6] = [[{"phone_type": data[4].strip().title(), "phone_number": data[5].strip()}]]
            credentials = dict(zip(("contact_id", "contact_name", "contact_email", "contact_birthday", "contact_phones", "group_name"), data))
            if self.validate_email(credentials["contact_email"]) and self.validate_birthday(credentials["contact_birthday"]) and self.validate_phone(credentials["contact_phones"]):
                self.execute_query("CALL update_contact(%s)", [Json(credentials)])
        except Exception:
            self.handle_output("failure", "FAILURE: Invalid data")
            self.start_application()

    def draw_table(self, data: list[dict[str, str | list[dict[str, str]]]], page_size: int = 15) -> None:
        total_records = len(data)
        total_pages = (total_records + page_size - 1) // page_size
        page = 0
        while True:
            self.clear_terminal()
            print(self.BOLD + "===== PhoneBook - Table =====" + self.RESET, end="\n\n")
            start = page * page_size
            end = min(start + page_size, total_records)
            page_data = data[start:end]
            column_widths = [36, 32, 32, 16, 32, 16]
            print(f"{f' TOTAL RECORDS: {total_records} | PAGE: {page+1}/{total_pages} ':=^{sum(column_widths) + 7}}")
            print("┌" + "┬".join("─" * w for w in column_widths) + "┐")
            headers = ["ID", "Name", "Email", "Birthday", "Phones", "Group"]
            print("│" + "│".join(f"{h:^{w}}" for h, w in zip(headers, column_widths)) + "│")
            print("├" + "┼".join("─" * w for w in column_widths) + "┤")
            for i, contact in enumerate(page_data):
                phone_lines = [f"{phone['phone_type']}: {phone['phone_number']}" for phone in contact[4]]
                if not phone_lines:
                    phone_lines = [""]
                row_height = max(1, len(phone_lines))
                for line_index in range(row_height):
                    row = [
                        f"{contact[0]:<{column_widths[0]}}" if line_index == 0 else " " * column_widths[0],
                        f"{contact[1]:<{column_widths[1]}}" if line_index == 0 else " " * column_widths[1],
                        f"{contact[2]:<{column_widths[2]}}" if line_index == 0 else " " * column_widths[2],
                        f"{contact[3]:<{column_widths[3]}}" if line_index == 0 else " " * column_widths[3],
                        f"{phone_lines[line_index]:<{column_widths[4]}}" if line_index < len(phone_lines) else " " * column_widths[4],
                        f"{contact[5]:<{column_widths[5]}}" if line_index == 0 else " " * column_widths[5],
                    ]
                    print("│" + "│".join(row) + "│")
                if i != len(page_data) - 1:
                    print("├" + "┼".join("─" * w for w in column_widths) + "┤")
                else:
                    print("└" + "┴".join("─" * w for w in column_widths) + "┘")
            print(f"\nNavigate: {self.BOLD}[n]{self.RESET} - next, {self.BOLD}[p]{self.RESET} - previous, {self.BOLD}[q]{self.RESET} - quit")
            key = input("\n>> ").strip().lower()
            if key == "n" and page < total_pages - 1:
                page += 1
            elif key == "p" and page > 0:
                page -= 1
            elif key == "q":
                break
        self.start_application()

    def establish_connection(self) -> None:
        try:
            with psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="123123") as connection:
                self.handle_output("success", "SUCCESS: Connected to database")
                self.connection = connection
                self.connection.autocommit = True
        except psycopg2.Error:
            self.handle_output("failure", "FAILURE: Could not connect to database")
            sys.exit(1)

    def start_application(self) -> None:
        try:
            del self.connection.notices[:]
            self.clear_terminal()
            print(self.BOLD + "===== PhoneBook =====" + self.RESET, end="\n\n")
            print(self.BOLD + self.UNDERLINED + "Select one of the following options:" + self.RESET, end="\n\n")
            print("1. Create contact")
            print("2. Read contact")
            print("3. Update contact")
            print("4. Delete contact")
            print("5. Search contact")
            print("6. Add phone to contact")
            print("7. Move contact to group")
            print("0. Exit", end="\n\n")
            option = int(input(">> "))
            if not (option > -1 and option < 8):
                raise Exception
            match option:
                case 0:
                    self.clear_terminal()
                    sys.exit(0)
                case 1:
                    self.create_contact()
                case 2:
                    result = self.execute_query("SELECT * FROM read_contact(%s, %s, %s, %s, %s);", [False, "contact_name", False, "contact_name", "contact_name"])
                    self.draw_table(result)
                case 3:
                    self.update_contact()
                case 4:
                    self.clear_terminal()
                    print(self.BOLD + "===== PhoneBook - Delete Contact =====" + self.RESET, end="\n\n")
                    contact_uuid = input("Enter contact's UUID: ").strip().lower()
                    self.execute_query("CALL delete_contact(%s);", [contact_uuid])
                case 5:
                    self.clear_terminal()
                    print(self.BOLD + "===== PhoneBook - Search Contact =====" + self.RESET, end="\n\n")
                    search_column = input("Enter column's label (id, name, email, birthday, phone type, phone number, group name): ").strip().lower()
                    search_column = ("contact_" + search_column if search_column in ("id", "name", "email", "birthday") else search_column.replace(" ", "_"))
                    print("")
                    search_pattern = input("Enter pattern: ").strip().lower()
                    result = self.execute_query("SELECT * FROM search_contact(%s, %s);", [search_column, search_pattern])
                    self.draw_table(result)
                case 6:
                    self.clear_terminal()
                    print(self.BOLD + "===== PhoneBook - Add Phone to Contact =====" + self.RESET, end="\n\n")
                    contact_id = input("Enter contact's ID: ").strip().lower()
                    print("")
                    phone_number = input("Enter contact's phone number: ").strip()
                    print("")
                    phone_type = input("Enter contact's phone type: ").strip().title()
                    if self.validate_phone([{"phone_number": phone_number, "phone_type": phone_type}]):
                        self.execute_query("CALL add_phone_to_contact(%s, %s, %s);", [contact_id, phone_number, phone_type])
                case 7:
                    self.clear_terminal()
                    print(self.BOLD + "===== PhoneBook - Move Contact to Group =====" + self.RESET, end="\n\n")
                    contact_id = input("Enter contact's ID: ").strip().lower()
                    print("")
                    group_name = input("Enter contact's group name: ").strip().title()
                    self.execute_query("CALL move_contact_to_group(%s, %s);", [contact_id, group_name])
            for notice in self.connection.notices:
                notice = notice.strip("NOTICE:  ").strip()
                self.handle_output("success" if "SUCCESS" in notice else "failure", notice)
            self.start_application()
        except (ValueError, Exception):
            self.handle_output("failure", "FAILURE: Invalid option")
            self.start_application()


if __name__ == "__main__":
    phone_book = PhoneBook()
    phone_book.establish_connection()
    phone_book.start_application()