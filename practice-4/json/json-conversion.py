import json

# Some JSON
x = '{ "name":"John", "age":30, "city":"New York"}'

# Parse x
y = json.loads(x)

# The result is a Python object (dictionary)
print(y["age"])

# Python object (dictionary)
x = {"name": "John", "age": 30, "city": "New York"}

# Convert into JSON
y = json.dumps(x)

# The result is a JSON string
print(y)