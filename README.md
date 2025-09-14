# CSV Matcher - recruitment task

## Opis
Ten moduł zawiera funkcje do wyszukiwania wartości w plikach CSV (lub tekście CSV / file-like objects) oraz mechanizm prostego cache (LRU) dla przyspieszenia powtarzających się zapytań. Kod udostępnia dwie główne funkcje użytkowe:

- `task1(search_dict, data)` — znajdź **pierwszy** wiersz pasujący do `search_dict` i zwróć wartość z kolumny `value`.
- `task2(list_of_search_dicts, data)` — znajdź wiele wierszy odpowiadających listom zapytań i oblicz **ważoną średnią** z odnalezionych wartości.

Moduł obsługuje wejście jako:
- ścieżka do pliku CSV (string wskazujący istniejący plik),
- surowy tekst CSV (string z zawartością),
- obiekt file-like (np. otwarty plik lub `io.StringIO`).

## Główne cechy
- Prosty LRU cache (`OrderedDict`) ograniczony do 1024 wpisów.
- Obsługa różnych formatów wejścia (ścieżka, tekst, file-like).
- Walidacja nagłówka (wymagana kolumna `value` oraz zbiór oczekiwanych kluczy).
- `task2` liczy średnią ważoną, gdzie parzyste liczby mają wagę 20, nieparzyste 10.

---

## Instalacja
Ten moduł nie wymaga zewnętrznych zależności — używa tylko standardowej biblioteki Pythona (moduły: `os`, `csv`, `hashlib`, `collections`, `io`). Wystarczy skopiować plik `.py` do projektu.

---

## Szybkie przykłady użycia
### Przykład 1 — użycie `task1` z tekstem CSV
```py
from io import StringIO
# przykładowy CSV (nagłówek musi zawierać kolumnę "value")
csv_text = """id,name,value\n1,Alice,10\n2,Bob,15\n3,Charlie,20\n"""

result = task1({'id': '2', 'name': 'Bob'}, csv_text)
print(result)  # -> '15'
```

### Przykład 2 — użycie `task2` z listą zapytań
```py
csv_text = """id,name,value\n1,Alice,10\n2,Bob,15\n3,Charlie,20\n4,Bob,8\n"""
queries = [
    {'id': '2', 'name': 'Bob'},
    {'id': '4', 'name': 'Bob'}
]
# Znajdzie wiersze id=2,name=Bob (value=15) i id=4,name=Bob (value=8)
# Wagi: 15 (nieparzyste) -> 10, 8 (parzyste) -> 20
# Średnia ważona = (15*10 + 8*20) / (10 + 20) = (150 + 160) / 30 = 10.333... -> '10.3'
print(task2(queries, csv_text))  # -> '10.3'
```

---

## API — opis funkcji i zachowanie
> Wszystkie wartości pokazane niżej są zgodne z oryginalną implementacją modułu.

### `_push_cache(key, value)`
- Pomocnicza funkcja dodająca wpis do globalnego `_MATCH_CACHE` (LRU). Jeśli cache przekroczy rozmiar `_MATCH_CACHE_MAXSIZE`, usuwa najstarszy wpis.
- Parametry:
  - `key` — dowolny hashowalny klucz użyty do rozróżnienia zapytań.
  - `value` — wartość do zapisania w cache.

### `_make_data_identifier(data)`
- Tworzy identyfikator danych wejściowych używany w kluczu cache. Obsługuje trzy przypadki:
  1. `data` jest stringiem i istnieje plik o takiej ścieżce: zwraca `('file', absolutna_ścieżka, mtime, size)`.
  2. `data` jest stringiem (wartość CSV): zwraca `('content', sha256_prefix, length)`.
  3. W przeciwnym razie: `('fileobj', id(data))` lub `('unknown', id(data))`.
- Cel: wykrywanie zmian pliku i rozróżnianie różnych źródeł danych w cache.

### `_open_data_as_reader(data)`
- Przygotowuje `csv.reader` z przekazanego źródła.
- Zwraca krotkę `(fileobj, reader)` gdzie `fileobj` to uchwyt (otwarty plik lub `StringIO` lub oryginalny obiekt), a `reader` to `csv.reader(fileobj)`.
- Uwaga: funkcja nie zwraca informacji, czy `fileobj` został otwarty wewnątrz funkcji — dlatego _caller_ stara się bezpiecznie zamknąć tylko znane typy (`StringIO` lub ścieżka pliku).

### `_validate_header(header_row, expected_keys)`
- Waliduje, że w nagłówku:
  - jest kolumna `value`,
  - pozostałe kolumny (z nagłówka) odpowiadają dokładnie `expected_keys` (porównanie jako zbiory).
- Zwraca `(header_keys, value_index, header)` gdzie `header_keys` to lista kolumn z nagłówka bez `value` (w kolejności z pliku), `value_index` to indeks kolumny `value`, a `header` to pełny, przycięty nagłówek.
- Jeśli walidacja nie przejdzie, rzuca `Exception("Key mismatch")`.

### `task1(search_dict, data)`
- Argumenty:
  - `search_dict` — słownik {kolumna: wartość} opisujący wymagane wartości (wszystkie porównania są wykonywane jako stringy po `strip()`).
  - `data` — ścieżka do pliku CSV, tekst CSV lub obiekt file-like.
- Działanie:
  1. Waliduje typ `search_dict`.
  2. Buduje klucz cache bazując na identyfikatorze danych i posortowanych parametrach zapytania.
  3. Jeśli wynik jest w cache — zwraca go natychmiast.
  4. Otwiera reader CSV i czyta nagłówek; waliduje obecność `value` i zgodność kluczy.
  5. Iteruje po wierszach, porównując wartości kolumn (stripowane) z oczekiwaniami — po pierwszym dopasowaniu zwraca zawartość kolumny `value` (string) i zapisuje w cache.
  6. Jeśli nic nie znaleziono — zapisuje w cache `"-1"` i zwraca `"-1"`.
- Uwaga: funkcja zwraca string — wartość kolumny `value` lub specjalny string `"-1"` przy braku wyniku.

### `task2(list_of_search_dicts, data)`
- Argumenty:
  - `list_of_search_dicts` — lista słowników (wszystkie muszą mieć identyczny zestaw kluczy).
  - `data` — jak wyżej.
- Działanie:
  1. Waliduje wejście i klucze zapytań.
  2. Tworzy zbiór docelowych krotek wartości (w kolejności kolumn z pliku).
  3. Iteruje plik, wyszukuje wszystkie żądane wiersze (przerywa wcześniej, jeśli wszystkie znalezione).
  4. Dla znalezionych wartości `value` parsuje je na `int` (ignoruje wartości nie konwertowalne) i sumuje ważoną sumę: waga 20 dla liczb parzystych, 10 dla nieparzystych.
  5. Zwraca średnią ważoną sformatowaną jako string z jedną cyfrą po przecinku (np. `'10.3'`) lub `"-1"` jeśli nie ma wartości liczbowych.

---

## Przykłady błędów / wyjątki
- `ValueError` zostanie rzucony, jeśli `search_dict` w `task1` nie jest słownikiem lub jeśli `list_of_search_dicts` w `task2` nie jest listą/krotką.
- `Exception("Key mismatch")` jest rzucane, gdy nagłówek pliku CSV nie zawiera kolumn wymaganych przez zapytania lub brakuje kolumny `value`.
- `task1` i `task2` zwracają string `"-1"` w różnych przypadkach braku wyniku (pusty plik, brak zgodnych wierszy, brak numerycznych wartości w `task2`).

---

## Ograniczenia i uwagi praktyczne
- Sentinel `"-1"` jako string może kolidować z rzeczywistą wartością `value` w CSV — rozważ zmianę na `None` lub wyjątki.
- `_open_data_as_reader` nie informuje callerów, czy obiekt `fileobj` został otwarty wewnątrz funkcji (co utrudnia deterministyczne zamykanie). Można to poprawić, zwracając dodatkowy flag `should_close`.
- Walidacja nagłówka używa porównania jako zbiorów (`set(...)`) — oznacza to, że **kolejność kolumn** w pliku może być dowolna, ale `task2` wykorzystuje kolejność nagłówka do budowy krotek — warto zachować konsekwencję.
- Format CSV: kod używa domyślnych ustawień `csv.reader` (separator `,`), nie obsługuje innych dialektów bez modyfikacji.
- Brak obsługi wielowątkowości — jeśli kod będzie używany współbieżnie, warto dodać blokady przy dostępie do `_MATCH_CACHE`.

---

## Testy jednostkowe

- Uruchom testy jednostkowe poleceniem:

```bash

pytest -q tests.py

```

---

## Twórca projektu


<table align="center">
  <tr>
    <td align="center">
      <a href="https://github.com/absolutecoder01">
        <img src="https://avatars.githubusercontent.com/u/56998201?v=4" width="100px;" alt="Zdjęcie użytkownika absolutecoder01"/><br />
        <sub><b>absolutecoder01</b></sub>
      </a>
      <br />
      🎨 📖 💻 🐛  
    </td>
  </tr>
</table>





