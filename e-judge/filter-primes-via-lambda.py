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
print(*list(filter(lambda i: i if not [False for j in range(2, i) if i % j == 0] else 0, [int(i) for i in input().split() if int(i) != 1])))