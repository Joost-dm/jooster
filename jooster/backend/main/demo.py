entry_numbers = (1, 2, 3, 4, 5, 6, 7, 8, 9)
print(list(map(lambda i: entry_numbers[i] + entry_numbers[i+1], range(len(entry_numbers)-1)[::2])))

