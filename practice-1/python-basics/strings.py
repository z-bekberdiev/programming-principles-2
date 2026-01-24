# Single or double quotes
print("Hello")
print('Hello')

# Quotes inside quotes
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

a = "Hello"
print(a)

a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

a = "Hello, World!"
print(a[1])
print(len(a))

for x in "banana":
    print(x)

txt = "The best things in life are free!"
print("free" in txt)
if "free" in txt:
    print("Yes, 'free' is present.")
print("expensive" not in txt)
if "expensive" not in txt:
    print("No, 'expensive' is NOT present.")

b = "Hello, World!"
print(b[2:5])
print(b[:5])
print(b[2:])
print(b[-5:-2])
print(b.upper())
print(b.lower())

a = " Hello, World! "
print(a.strip())            # Returns "Hello, World!"
print(a.replace("H", "J"))  # Returns "Jello, World!"
print(a.split(","))         # Returns ['Jello', ' World!']

a = "Hello"
b = "World"
c = a + b
print(c)

a = "Hello"
b = "World"
c = a + " " + b
print(c)

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price} dollars"
print(txt)
txt = f"The price is {price:.2f} dollars"
print(txt)
txt = f"The price is {20 * price} dollars"
print(txt)

txt = "We are the so-called \"Vikings\" from the north." # Backslash character to use similar quotes several times
print(txt)
