# Condition without elif
a = 200
b = 33
if b > a:
    print("b is greater than a")
else:
    print("b is not greater than a")

# Fallback with else
username = "Emil"
if len(username) > 0:
    print(f"Welcome, {username}!")
else:
    print("Error: Username cannot be empty")
 