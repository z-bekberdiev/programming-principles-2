x = 300

def myfunc():
    print(x)

myfunc()

print(x)

# or

def myfunc():
    global x
    x = 300

myfunc()

print(x)