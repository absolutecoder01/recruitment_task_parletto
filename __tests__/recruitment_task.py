import csv
from io import StringIO
from functools import lru_cache

def parse_data(data):
    # Parse CSV data into list of dicts
    f = StringIO(data)
    reader = csv.DictReader(f)
    rows = list(reader)
    return reader.fieldnames, rows

@lru_cache(maxsize=128)
def cached_parse_data(data):
    return parse_data(data)

def task1(search, data):
    # Parse data with caching
    header, rows = cached_parse_data(data)
    
    # Check keys in search
    search_keys = set(search.keys())
    header_keys = set(header) - {'value'}
    if search_keys != header_keys:
        raise Exception("Key mismatch")
    
    for row in rows:
        # Check full match for all keys in search
        if all(row[k] == str(search[k]) for k in search_keys):
            return row['value']
    return '-1'

def task2(search_list, data):
    header, rows = cached_parse_data(data)
    header_keys = set(header) - {'value'}
    
    # Validate keys for each search dict
    for search in search_list:
        if set(search.keys()) != header_keys:
            raise Exception("Key mismatch")
    
    total_weighted_value = 0
    total_weight = 0
    
    for search in search_list:
        for row in rows:
            if all(row[k] == str(search[k]) for k in search.keys()):
                val = int(row['value'])
                weight = 20 if val % 2 == 0 else 10
                total_weighted_value += val * weight
                total_weight += weight
    
    if total_weight == 0:
        return '0.0'  # no matches
    
    avg = total_weighted_value / total_weight
    return f"{avg:.1f}"
