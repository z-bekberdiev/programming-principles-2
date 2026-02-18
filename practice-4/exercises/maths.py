import math
from os import system
from time import sleep


def task_1():
    input_degree = float(input("Input degree: "))
    print()
    output_radian = math.radians(input_degree)
    print(f"Output radian: {output_radian:.6f}")
    print()
    sleep(5)
    main()


def task_2():
    height = float(input("Height: "))
    print()
    first_base = float(input("Base, first value: "))
    print()
    second_base = float(input("Base, second value: "))
    print()
    expected_output = (first_base + second_base) / 2 * height
    print(f"Expected output: {expected_output}")
    print()
    sleep(5)
    main()


def task_3():
    input_number_of_sides = int(input("Input number of sides: "))
    print()
    input_the_length_of_a_side = float(input("Input the length of a side: "))
    print()
    the_area_of_the_polygon_is = (1 / 4) * input_number_of_sides * (input_the_length_of_a_side ** 2) * (1 / math.tan(math.pi / input_number_of_sides))
    print(f"The area of the polygon is: {the_area_of_the_polygon_is:.0f}")
    print()
    sleep(5)
    main()


def task_4():
    length_of_base = float(input("Length of base: "))
    print()
    height_of_parallelogram = float(input("Height of parallelogram: "))
    print()
    expected_output = length_of_base * height_of_parallelogram
    print(f"Expected output: {expected_output}")
    print()
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
                print("Task 1: Write a Python program to convert degree to radian.\n")
                task_1()
            case 2:
                clear()
                print("Task 2: Write a Python program to calculate the area of a trapezoid.\n")
                task_2()
            case 3:
                clear()
                print("Task 3: Write a Python program to calculate the area of regular polygon.\n")
                task_3()
            case 4:
                clear()
                print("Task 4: Write a Python program to calculate the area of a parallelogram.\n")
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