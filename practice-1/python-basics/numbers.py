x = 1    # int
y = 2.8  # float
z = 1j   # complex

print(type(x))
print(type(y))
print(type(z))

# int
x = 1
y = 35656222554887711
z = -3255522

print(type(x))
print(type(y))
print(type(z))

# float
x = 1.10
y = 1.0
z = -35.59

print(type(x))
print(type(y))
print(type(z))

# n times ten in power of m
x = 35e3
y = 12E4
z = -87.7e100

print(type(x))
print(type(y))
print(type(z))

# complex
x = 3+5j
y = 5j
z = -5j

print(type(x))
print(type(y))
print(type(z))

# Type conversion
x = 1    # int
y = 2.8  # float
z = 1j   # complex

# Convert from int to float
a = float(x)

# Convert from float to int
b = int(y)

# Convert from int to complex
c = complex(x)

print(a)
print(b)
print(c)

print(type(a))
print(type(b))
print(type(c))

# Random number
import random

print(random.randrange(1, 10)) # Generates pseudo-random integer number in a range from 1 to 10 (exclusive)
