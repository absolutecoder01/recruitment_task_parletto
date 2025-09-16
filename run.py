import lz4.frame
from recruitment_task import task1,task2

search_list = [
  {'a': 862984, 'b': 29105, 'c': 605280, 'd': 678194, 'e': 302120},
  {'a': 20226, 'b': 781899, 'c': 186952, 'd': 506894, 'e': 325696}
]

def read_lz4_file(filename):
    with lz4.frame.open(filename, 'rt') as f:
        return f.read()

filename = 'find_match_average_v2.dat.lz4'
data = read_lz4_file(filename)

result = task2(search_list, data)
print(result) # 608384.2 / CORRECT!


data = 'side,currency,value\nIN,PLN,1\nIN,EUR,2\nOUT,ANY,3'

print(task1({'side': 'IN', 'currency': 'PLN'}, data))  # '1'
print(task1({'side': 'IN', 'currency': 'GBP'}, data))  # '-1'
