# Warcaby

Projekt powstał na przedmiot PSZT.

![](assets/screen1.png)

![](assets/screen2.png)

## Opis zadania

```
Warcaby w wariancie rosyjskim, może być interfejs konsolowy.
Gra z komputerem, przydatne algorytmy: minimax z przycinaniem alpha-beta.
Przed rozpoczęciem realizacji projektu proszę zapoznać się z zawartością strony.
```

Zasady gry wzięliśmy z tej [strony](https://www.kurnik.pl/warcabyrosyjskie/zasady.phtml).
Uznaliśmy możliwość bicia w przód jak i tył, ale ruch może być tylko w przód.
Każdy pion, który znajdzie się na przeciwnym końcu planszy awansuje na damkę.
Bicie jest obowiązkowe, ale wybór z wielu możliwości bić jest dowolny.
Nie ma dodatkowych zasad typu zasad określających remis, gdy zostanie dokonana pewna ilość ruchów damkami.

## Dokumentacja

### Opis programu z poziomu użytkownika

Użytkownik zaczyna gre jako biały na dole planszy.
Przyjęliśmy, że białe pinki to te wypełnione, natomiast czarne to puste, nie jest to trywialne, z uwagi, na możliwość występowania różnych stylów terminala.
Użytkownik może wybrać ruch z pośród N możliwych, wybór następuje przed podanie indeksu ruchu.
Przestrzeń terminala jest podzielona na trzy sekcje: plansza gry, możliwe ruchy i historia rozgrywki.
Punkty na planszy są oznaczane jako dwie liczby, numer wiersza(pion) i numer kolumny(poziom) oddzielone przecinkiem.
Po dokonaniu wyboru, który trzeba zatwierdzić enterem, następuje ruch komputera.
W celu lepszych doznań użytkownika, komputer myśli minimum 3 sekundy.
Następnie gracz z komputerem wykonują ruchy na przemiennie.

### Podział klas w programie

Postanowiliśmy rozdzielić zasady gry od algorytmu przeszukiwania.

#### Stan gry i ruchy

Gra w warcaby opiera się na ruchach turowych, ale nie naprzemiennych.
Podzieliliśmy program na 3 klasy z danymi i 1 pomocniczą:
 - `CheckersState` w pliku `src/game/state.py`, reprezentującą stan planszy
 - `CheckerMove` w pliku `src/game/move.py`, reprezentującą ruch jednego pionka (jedno posunięcie)
 - `CheckerMoveComplex` w pliku `src/game/moveComlex.py`, reprezentującą ruch jednego pionka (wiele posunięć)
 - `CheckerType` w pliku `src/game/type.py`, do określania typów pionków i ich drużyn

#### Algorytm min-max



### Wnioski

## Autorzy

Adam Jędrzejowski <adam@jedrzejowski.pl>

Dawid Mackiewicz <dawidmyk@wp.pl>