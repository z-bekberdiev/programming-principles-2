import datetime
from os import system
from time import sleep


def task_1():
    current_date = datetime.datetime.today()
    print(f"Current datetime: {current_date.strftime("%d-%m-%Y")}")
    print()
    print(f"Edited datetime: {(current_date - datetime.timedelta(days=5)).strftime("%d-%m-%Y")}")


def task_2():
    current_day = datetime.datetime.today()
    print(f"Yesterday: {(current_day - datetime.timedelta(days=1)).strftime("%d-%m-%Y")}")
    print()
    print(f"Today: {current_day.strftime("%d-%m-%Y")}")
    print()
    print(f"Tomorrow: {(current_day + datetime.timedelta(days=1)).strftime("%d-%m-%Y")}")


def task_3():
    current_date = datetime.datetime.now()
    print(f"Datetime with microseconds: {current_date.strftime("%d-%m-%Y %H:%M:%S.%f")}")
    print()
    print(f"Datetime without microseconds: {current_date.strftime("%d-%m-%Y %H:%M:%S")}")


def task_4():
    sample_date = "03-12-2007 14:00:00.000000"
    sample_date = datetime.datetime.strptime(sample_date, "%d-%m-%Y %H:%M:%S.%f")
    print(f"Sample datetime: {sample_date}.000000")
    print()
    current_date = datetime.datetime.now()
    print(f"Current datetime: {current_date}")
    print()
    print(f"Difference in seconds: {(current_date - sample_date).total_seconds()}")


def clear():
    system("clear")
    print("\n")
    system("clear")


def main():
    clear()
    try:
        n = int(input("Enter a number of the task (Enter [0] to exit): "))
        match n:
            case 0:
                clear()
                exit(0)
            case 1:
                clear()
                print("Task 1: Write a Python program to subtract five days from current date.\n")
                task_1()
            case 2:
                clear()
                print("Task 2: Write a Python program to print yesterday, today, tomorrow.\n")
                task_2()
            case 3:
                clear()
                print("Task 3: Write a Python program to drop microseconds from datetime.\n")
                task_3()
            case 4:
                clear()
                print("Task 4: Write a Python program to calculate two date difference in seconds.\n")
                task_4()
            case _:
                clear()
                print("Wrong input. Try again!\n")
                sleep(2)
                main()
    except ValueError:
        clear()
        print("Wrong input. Try again!\n")
        sleep(2)
        main()


if __name__ == "__main__":
    main()