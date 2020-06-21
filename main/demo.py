numbers = [int(number) for number in input('enter numbers: ').split(' ')]
if len(numbers) < 3:
    print('please type at least 3 numbers')
    exit(0)
arr = [0, 0, 0]

def multiply(arr):
    return arr[0] * arr[1] * arr[2]

for number in numbers:
    if abs(number) > arr[0]:
        arr[2] = arr[1]
        arr[1] = arr[0]
        arr[0] = number

print(multiply(arr))

