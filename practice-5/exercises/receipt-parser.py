from os import system, path # type: ignore
from re import findall, search, Match # type: ignore


class Receipt_Parser:
    def __init__(self, raw_file_path: str) -> None:
        self.raw_file_path: str = raw_file_path

    def read_raw_file(self) -> None:
        with open(self.raw_file_path, "r") as raw_file:
            self.raw_file_content: str = "\n".join([raw_file_item.strip("\n").strip() for raw_file_item in raw_file.readlines()])
    
    def extract_product_prices(self) -> None:
        self.product_prices: list[str] = findall("(?<=Стоимость\\s)(\\d+?\\s?\\d+\\,\\d+)", self.raw_file_content)
        print(*self.product_prices, sep="\n")

    def find_product_names(self) -> None:
        self.product_names: list[str] = findall(r".+(?=\n\d{1}\,\d{3})", self.raw_file_content)
        print(*self.product_names, sep="\n")

    def calculate_total_amount(self) -> None:
        self.total_amount: float = sum([float(str(total_amount).replace(",", ".").replace(" ", "")) for total_amount in findall("\\d{1}\\,\\d{3}", self.raw_file_content)])
        print(f"{self.total_amount:.3f}".replace(".", ","))

    def extract_date_and_time(self) -> None:
        self.date_and_time: list[str] = [*findall("(\\d+\\.\\d+\\.\\d+)(\\s)(\\d+\\:\\d+\\:\\d+)", self.raw_file_content)[0]]
        del self.date_and_time[1]
        print(f"Дата: {self.date_and_time[0]}")
        print(f"Время: {self.date_and_time[1]}")

    def find_payment_method(self) -> None:
        self.payment_method: Match[str] | None = search(".+(?=\\n(\\d+?\\s?\\d+\\,\\d+)\\nИТОГО)", self.raw_file_content)
        if self.payment_method:
            print(self.payment_method.group()[:-1])


if __name__ == "__main__":
    system("clear") # type: ignore
    print("\n")
    system("clear") # type: ignore
    receipt_parser: Receipt_Parser = Receipt_Parser(f"{path.dirname(__file__)}/raw.txt")
    receipt_parser.read_raw_file()
    print("\033[1;4mAll product prices that are available in the receipt:\033[0m")
    receipt_parser.extract_product_prices()
    print()
    print("\033[1;4mAll product names that are available in the receipt:\033[0m")
    receipt_parser.find_product_names()
    print()
    print("\033[1;4mTotal amount of the purchased products:\033[0m")
    receipt_parser.calculate_total_amount()
    print()
    print("\033[1;4mDate and time information:\033[0m")
    receipt_parser.extract_date_and_time()
    print()
    print("\033[1;4mPayment method:\033[0m")
    receipt_parser.find_payment_method()
    print()


# The output of my program is provided below, by the way, my script is dynamic in terms of changes made inside the 'raw.txt' file
"""
All product prices that are available in the receipt:
308,00
51,00
32,00
120,00
310,00
461,00
381,00
386,00
381,00
414,00
841,00
841,00
1 200,00
1 152,00
1 152,00
168,00
163,00
1 526,00
792,00
7 330,00

All product names that are available in the receipt:
Натрия хлорид 0,9%, 200 мл, фл.
Борный спирт 3%, 20 мл, фл.
Шприц 2 мл, 3-комп. (Bioject)
Система для инфузии Vogt Medical
Шприц 5 мл, 3-комп.
AURA, ватные диски № 150
Чистая линия, скраб мягкий, 50 мл
Чистая линия, скраб очищающий «Абрикос», 50 мл
Чистая линия, скраб мягкий, 50 мл
Nivea, шампунь 3 в 1 мужской, 400 мл
Pro Series, шампунь «Яркий цвет», 500 мл
Pro Series, бальзам-ополаскиватель для длительного ухода за окрашенными волосами «Яркий цвет», 500 мл
Clear, шампунь «Актив Спорт» 2 в 1 мужской, 400 мл
Bio World (Hydro Therapy), мицеллярная вода 5 в 1, 445 мл
Bio World (Hydro Therapy), гель-мусс для умывания с гиалуроновой кислотой, 250 мл
[RX] Натрия хлорид 0,9%, 100 мл, фл.
[RX] Дисоль, р-р 400 мл, фл.
Тагансорбент с ионами серебра № 30, пор.
[RX] Церукал 2%, 2 мл, № 10, амп.
[RX] Андазол 200 мг, № 40, табл.

Total amount of the purchased products:
24,000

Date and time information:
Дата: 18.04.2019
Время: 11:13:58

Payment method:
Банковская карта
"""