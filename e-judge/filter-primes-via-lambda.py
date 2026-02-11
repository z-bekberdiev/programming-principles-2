# Solution No. 1
def is_prime(number):
    for integer in range(2, number):
        if number % integer == 0:
            return False
    return True

array = [int(number) for number in input().split() if number != '1']
array = list(filter((lambda number: number if is_prime(number) else 0), array))
print(*array) if len(array) > 0 else print("No primes")

# Solution No. 2
print(*(lambda array: array if len(array) > 0 else ["No primes"])(list(filter(lambda number: number if not [False for integer in range(2, number) if number % integer == 0] else 0, [int(number) for number in input().split() if int(number) > 1]))))