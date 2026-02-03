length = int(input())
numbers = [int(element) for element in input().split()]
count = int(input())
operations = []

for integer in range(0, count):
    operations.append(input())

for operation in operations:
    if operation == "abs":
        numbers = list(map(lambda element: abs(element), numbers))
        continue

    operation = operation.split()

    match operation[0]:
        case "add":
            numbers = list(map(lambda element: element + int(operation[1]), numbers))

        case "multiply":
            numbers = list(map(lambda element: element * int(operation[1]), numbers))

        case "power":
            numbers = list(map(lambda element: element ** int(operation[1]), numbers))

print(*numbers)