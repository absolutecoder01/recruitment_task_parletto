# CSV Data Search & Weighted Average

Ten projekt zawiera implementację w Pythonie, która umożliwia:

1. **Parsowanie danych CSV** do listy słowników.  
2. **Wyszukiwanie wartości w danych** na podstawie pełnego dopasowania kluczy.  
3. **Obliczanie średniej ważonej** wartości liczbowych przy różnych wagach zależnych od parzystości liczby.  
4. **Cache’owanie wyników parsowania** w celu optymalizacji wydajności.  

---

## Funkcjonalności

### `parse_data(data: str)`
- Przyjmuje dane w formacie CSV (string).  
- Zwraca nagłówki oraz listę wierszy w formie słowników (`dict`).  

### `cached_parse_data(data: str)`
- Jak `parse_data`, ale z **cache’owaniem** (do 128 różnych wejść).  
- Przy kolejnych wywołaniach na tych samych danych CSV zwraca wynik z pamięci podręcznej, zamiast parsować ponownie.  

### `task1(search: dict, data: str)`
- Szuka dokładnego dopasowania wiersza w danych CSV.  
- `search` musi zawierać wszystkie kolumny oprócz `value`.  
- Zwraca wartość z kolumny `value`, jeśli znaleziono dopasowanie.  
- W przeciwnym wypadku zwraca `-1`.  

**Przykład:**  
```python
csv_data = """name,age,value
Alice,30,100
Bob,25,200
"""

print(task1({"name": "Alice", "age": "30"}, csv_data))  
# Wynik: 100
```

### `task2(search_list: list[dict], data: str)`
- Przyjmuje listę zapytań (`search_list`).  
- Dla każdego dopasowanego wiersza oblicza **średnią ważoną** z kolumny `value`:  
  - waga = `20` dla liczb parzystych  
  - waga = `10` dla liczb nieparzystych  
- Zwraca wynik w formacie stringa z dokładnością do 1 miejsca po przecinku.  
- Jeśli brak dopasowań → zwraca `"0.0"`.  

**Przykład:**  
```python
csv_data = """name,age,value
Alice,30,100
Bob,25,201
Charlie,25,202
"""

searches = [
    {"name": "Alice", "age": "30"},
    {"name": "Charlie", "age": "25"}
]

print(task2(searches, csv_data))
# Wynik: 151.1
```

---

## Wymagania

- Python **3.8+**  
- Standardowa biblioteka (`csv`, `functools`, `io`) – brak dodatkowych zależności.  

---

## Uruchamianie

1. Sklonuj repozytorium:  
   ```bash
   git clone https://github.com/absolutecoder01/csv-search
   cd csv-search
   ```
2. Uruchom w Pythonie (np. w trybie interaktywnym):  
   ```bash
   python3
   >>> from main import task1, task2
   ```

---

## Możliwe zastosowania

- Przechowywanie i szybkie wyszukiwanie danych w formacie CSV.  
- Analiza wartości z prostym systemem wag.  
- Rozszerzalny fundament pod system rekomendacji lub rankingów.  

## Twórca

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


