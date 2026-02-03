def my_function(n):
    if isinstance(n, str):
        return "Hello, World!"
    elif isinstance(n, int):
        return 100
    elif isinstance(n, bool):
        return True
    elif isinstance(n, complex):
        return 10j
    elif isinstance(n, list):
        return [1, 2, 3]
    elif isinstance(n, tuple):
        return (1, 2, 3)
    elif isinstance(n, dict):
        return {"Name": "Zhantore", "Age": 18}
    else:
        return None


print(my_function("String"))
print(my_function(1))
print(my_function(False))
print(my_function(1j))
print(my_function([7, 8, 9]))
print(my_function((7, 8, 9)))
print(my_function({"Country": "Norway", "City": "Oslo"}))
print(
    my_function(1.0)
)  # Returns None because argument's data type is float which doesn't match with specified conditions