# Solution No. 1
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

# Solution No. 2
numbers = [[int(element) for element in input().split()] for _ in range(int(input()) * 0, 1)]
for operation in [input().split() for _ in range(0, int(input()))]: numbers[0] = list(map(lambda element: abs(element) if operation[0] == "abs" else element + int(operation[1]) if operation[0] == "add" else element * int(operation[1]) if operation[0] == "multiply" else element ** int(operation[1]) if operation[0] == "power" else 0, numbers[0]))
print(*numbers[0])