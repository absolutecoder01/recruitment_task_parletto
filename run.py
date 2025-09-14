from recruitment_task import task1, task2

data = 'side,currency,value\nIN,PLN,1\nIN,EUR,2\nOUT,ANY,3'

print(task1({'side': 'IN', 'currency': 'PLN'}, data))  # '1'
print(task1({'side': 'IN', 'currency': 'GBP'}, data))  # '-1'

keys = [
  {'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120},
  {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}
]

result = task2(keys, 'find_match_average_v2.dat')
print("Wynik task2:", result) # 666172.0