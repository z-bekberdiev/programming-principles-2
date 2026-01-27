# Simple for loop
fruits = ["apple", "banana", "cherry"]
for x in fruits:
    print(x)

# The same loop but with else and for string
for x in "banana":
    print(x)
else:
    print("Finally finished!")

# Nested loops
details = ["red", "big", "tasty"]
fruits = ["apple", "banana", "cherry"]
for x in details:
    for y in fruits:
        print(x, y)
 