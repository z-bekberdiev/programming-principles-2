from os import system
from time import sleep


def task_1():

    def generate_squares_of_numbers(N):
        natural_number = 1
        while natural_number <= N:
            yield natural_number ** 2
            natural_number += 1

    N = int(input("Enter a number: "))

    print("\nOutput:", end=" ")

    for square_of_number in generate_squares_of_numbers(N):
        print(square_of_number, end= " ")

    print("\n")
    
    sleep(5)

    main()


def task_2():

    def generate_even_numbers(n):
        natural_number = 0
        while natural_number <= n:
            if natural_number % 2 == 0:
                yield natural_number
            natural_number += 1

    n = int(input("Enter a number: "))

    a = []

    print("\nOutput:", end=" ")

    for even_number in generate_even_numbers(n):
        a.append(even_number)

    print(*a, sep=", ")

    print()

    sleep(5)

    main()


def task_3():

    def generate_numbers_divisible_by_3_and_4(n):
        natural_number = 0
        while natural_number <= n:
            if natural_number % 3 == 0 and natural_number % 4 == 0:
                yield natural_number
            natural_number += 1

    n = int(input("Enter a number: "))

    print("\nOutput:", end=" ")

    for number_divisible_by_3_and_4 in generate_numbers_divisible_by_3_and_4(n):
        print(number_divisible_by_3_and_4, end= " ")

    print("\n")

    sleep(5)

    main()


def task_4():

    def generate_squares_from_a_to_b(a, b):
        while a <= b:
            yield a ** 2
            a += 1

    a, b = [int(i) for i in input("Enter two numbers using space between them: ").split()]

    print("\nOutput:", end=" ")

    for square_from_a_to_b in generate_squares_from_a_to_b(a, b):
        print(square_from_a_to_b, end=" ")

    print("\n")

    sleep(5)

    main()


def task_5():

    def generate_numbers_from_n_to_0(n):
        while n >= 0:
            yield n
            n -= 1

    n = int(input("Enter a number: "))

    print("\nOutput:", end=" ")

    for number_from_n_to_0 in generate_numbers_from_n_to_0(n):
        print(number_from_n_to_0, end=" ")

    print("\n")

    sleep(5)

    main()


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
                print("Task 1: Create a generator that generates the squares of numbers up to some number N.\n")
                task_1()
            case 2:
                clear()
                print("Task 2: Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.\n")
                task_2()
            case 3:
                clear()
                print("Task 3: Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.\n")
                task_3()
            case 4:
                clear()
                print("Task 4: Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a \"for\" loop and print each of the yielded values.\n")
                task_4()
            case 5:
                clear()
                print("Task 5: Implement a generator that returns all numbers from (n) down to 0.\n")
                task_5()
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