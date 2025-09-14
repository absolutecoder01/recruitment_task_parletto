import os
import csv
import hashlib
from collections import OrderedDict
from io import StringIO

# globalny orderedDict, sluzy jako pamiec podreczna
_MATCH_CACHE = OrderedDict()
# maksymalna liczba wpisow w cache 
_MATCH_CACHE_MAXSIZE = 1024


def _push_cache(key, value):
    '''
    dodaje/aktualizuje wpis w cache i realizuje last recently used
    * jesli klucz jest, przenosi na koniec (najswiezszy)
    * zapisuje aktualizuje _MATCH_CACHE
    * jesli dlugosc przekracza limit, usuwa najstarszy wpis
    '''
    if key in _MATCH_CACHE:
        _MATCH_CACHE.move_to_end(key)
    _MATCH_CACHE[key] = value
    if len(_MATCH_CACHE) > _MATCH_CACHE_MAXSIZE:
        _MATCH_CACHE.popitem(last=False)

def _make_data_identifier(data):
    """
    buduje identyfikator do uzycia w cache
    """
    if isinstance(data, str) and os.path.exists(data):
        stat = os.stat(data)
        return ("file", os.path.abspath(data), int(stat.st_mtime), stat.st_size)
    if isinstance(data, str):
        h = hashlib.sha256(data.encode("utf-8")).hexdigest()[:16]
        return ("content", h, len(data))
    try:
        return ("fileobj", id(data))
    except Exception:
        return ("unknown", id(data))

def _open_data_as_reader(data):
    """
    funkcja do otwierania/przygotowywania pliku CSV
    """
    if isinstance(data, str) and os.path.exists(data):
        f = open(data, "r", newline="", encoding="utf-8")
        reader = csv.reader(f)
        return f, reader
    if isinstance(data, str):
        f = StringIO(data)
        reader = csv.reader(f)
        return f, reader
    reader = csv.reader(data)
    return data, reader

def _validate_header(header_row, expected_keys):
    """
    funkcja sprawdza naglowek CSV
    """
    header = [h.strip() for h in header_row]
    if "value" not in header:
        raise Exception("Key mismatch")
    header_keys = [h for h in header if h != "value"]
    if set(header_keys) != set(expected_keys):
        raise Exception("Key mismatch")
    value_index = header.index("value")
    return header_keys, value_index, header

def task1(search_dict, data):
    """
    funkcja task1
    """
    if not isinstance(search_dict, dict):
        raise ValueError("search must be dict")

    data_id = _make_data_identifier(data)
    sorted_items = tuple(sorted((k, str(v)) for k, v in search_dict.items()))
    cache_key = (data_id, sorted_items)
    if cache_key in _MATCH_CACHE:
        _MATCH_CACHE.move_to_end(cache_key)
        return _MATCH_CACHE[cache_key]

    fileobj, reader = _open_data_as_reader(data)
    try:
        try:
            header_row = next(reader)
        except StopIteration:
            _push_cache(cache_key, "-1")
            return "-1"

        header_keys, value_index, header_full = _validate_header(header_row, search_dict.keys())
        key_to_index = {k: header_full.index(k) for k in header_keys}

        for row in reader:
            if len(row) < len(header_full):
                continue
            match = True
            for key, expected in sorted_items:
                idx = key_to_index[key]
                if row[idx].strip() != expected:
                    match = False
                    break
            if match:
                result_value = row[value_index].strip()
                _push_cache(cache_key, result_value)
                return result_value

        _push_cache(cache_key, "-1")
        return "-1"
    finally:
        if isinstance(fileobj, (StringIO,)) or (isinstance(data, str) and os.path.exists(data)):
            try:
                fileobj.close()
            except Exception:
                pass

def task2(list_of_search_dicts, data):
    """
    funkcja task2
    """
    if not isinstance(list_of_search_dicts, (list, tuple)):
        raise ValueError("first argument must be list of dicts")

    if len(list_of_search_dicts) == 0:
        return "-1"

    keys_set = set(list_of_search_dicts[0].keys())
    for d in list_of_search_dicts:
        if set(d.keys()) != keys_set:
            raise Exception("Key mismatch")

    fileobj, reader = _open_data_as_reader(data)
    try:
        try:
            header_row = next(reader)
        except StopIteration:
            return "-1"

        header_keys, value_index, header_full = _validate_header(header_row, keys_set)
        ordered_key_list = header_keys
        target_tuples = {}
        for idx, search in enumerate(list_of_search_dicts):
            t = tuple(str(search[k]) for k in ordered_key_list)
            target_tuples[t] = False

        found_values = {}

        remaining = len(target_tuples)
        indices_for_ordered_keys = [header_full.index(k) for k in ordered_key_list]

        for row in reader:
            if len(row) < len(header_full):
                continue
            key_tuple = tuple(row[idx].strip() for idx in indices_for_ordered_keys)
            if key_tuple in target_tuples and not target_tuples[key_tuple]:
                val = row[value_index].strip()
                found_values[key_tuple] = val
                target_tuples[key_tuple] = True
                remaining -= 1
                if remaining == 0:
                    break

        total_weighted_sum = 0
        total_weight = 0
        for key_tuple, val_str in found_values.items():
            try:
                value_int = int(val_str)
            except ValueError:
                continue
            weight = 20 if (value_int % 2 == 0) else 10
            total_weighted_sum += value_int * weight
            total_weight += weight

        if total_weight == 0:
            return "-1"
        average = total_weighted_sum / total_weight
        return "{:.1f}".format(round(average, 1))
    finally:
        if isinstance(fileobj, (StringIO,)) or (isinstance(data, str) and os.path.exists(data)):
            try:
                fileobj.close()
            except Exception:
                pass
