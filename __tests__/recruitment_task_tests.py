"""
Pytest unit tests dla modułu zawierającego funkcje `task1` i `task2`.

Zapisz oryginalny kod w pliku `recruitment_task.py` w tym samym katalogu co ten plik testowy.
Uruchom testy poleceniem:

    pytest -q

"""

import pytest
from pathlib import Path

# helper: assumes module is saved as recruitment_task.py


def test_task1_string_csv_found():
    import recruitment_task
    error = False
    recruitment_task._MATCH_CACHE.clear()
    csv_text = "id,name,value\n1,Alice,10\n2,Bob,15\n"
    assert recruitment_task.task1({'id': '2', 'name': 'Bob'}, csv_text) == '15'
    if error != False:
        print("test_task1_string_csv_found: powodzenie")
    else:
        print("test_task1_string_csv_found: FATAL_ERROR")


def test_task1_file_path_found(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    p = tmp_path / "data.csv"
    p.write_text("id,name,value\n1,Alice,10\n2,Bob,15\n", encoding='utf-8')
    assert recruitment_task.task1({'id': '1', 'name': 'Alice'}, str(p)) == '10'


def test_task1_no_match_returns_minus1():
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    csv_text = "id,name,value\n1,Alice,10\n"
    assert recruitment_task.task1({'id': '2', 'name': 'Bob'}, csv_text) == '-1'


def test_task1_empty_file_returns_minus1(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    p = tmp_path / "empty.csv"
    p.write_text("", encoding='utf-8')
    assert recruitment_task.task1({'id': '1'}, str(p)) == '-1'


def test_task2_basic_weights(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    content = "id,name,value\n2,Bob,15\n4,Bob,8\n"
    p = tmp_path / "data.csv"
    p.write_text(content, encoding='utf-8')
    queries = [{'id': '2', 'name': 'Bob'}, {'id': '4', 'name': 'Bob'}]
    assert recruitment_task.task2(queries, str(p)) == '10.3'


def test_task2_non_numeric_values_ignored(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    content = "id,name,value\n1,Alice,notint\n"
    p = tmp_path / "data.csv"
    p.write_text(content, encoding='utf-8')
    queries = [{'id': '1', 'name': 'Alice'}]
    assert recruitment_task.task2(queries, str(p)) == '-1'


def test_task2_partial_numeric_and_non_numeric(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    content = "id,name,value\n1,A,5\n2,B,notint\n"
    p = tmp_path / "data.csv"
    p.write_text(content, encoding='utf-8')
    queries = [{'id': '1', 'name': 'A'}, {'id': '2', 'name': 'B'}]
    # tylko wartość 5 jest liczbowo poprawna -> waga 10 -> średnia 5.0
    assert recruitment_task.task2(queries, str(p)) == '5.0'


def test_key_mismatch_raises(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    p = tmp_path / "data.csv"
    p.write_text("id,value\n1,10\n", encoding='utf-8')
    with pytest.raises(Exception):
        recruitment_task.task1({'id': '1', 'name': 'Alice'}, str(p))


def test_task2_keys_must_match_between_queries():
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    queries = [{'id': '1', 'name': 'A'}, {'id': '2'}]
    with pytest.raises(Exception):
        recruitment_task.task2(queries, "")


def test_cache_behaviour(tmp_path):
    import recruitment_task
    recruitment_task._MATCH_CACHE.clear()
    p = tmp_path / "data.csv"
    p.write_text("id,name,value\n1,Alice,10\n", encoding='utf-8')
    res1 = recruitment_task.task1({'id': '1', 'name': 'Alice'}, str(p))
    res2 = recruitment_task.task1({'id': '1', 'name': 'Alice'}, str(p))
    assert res1 == res2 == '10'
