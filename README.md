# Sterowanie sygnalizacją świetlną za pomocą  uczenia ze wzmocnieniem
Projekt stara się sprostać zadaniu optymalizacji skrzyżowania w ruchu drogowym. Agent uczenia ze wzmocnieniem, napisany w Pytorchu, steruje sygnalizacją świetlną symulacji w środowisku SUMO tak, aby jak najbardziej ograniczyć czas i ilość pojazdów stojących przed skrzyżowaniem, dodatkowo rozpatrując różne natężenia ruchu.

## Wyniki 
Agent osiągał średnio lepsze wyniki niż stałe światła trwające 10 sekund. Testy zostałe wykonane na trzech nowych, losowo wygenerowanych trasach, przez co można zauważyć, że trasa nr 2 była zdecydowanie trudniejsza od pozostałych. Jako miarę przyjąłem średnią liczbę aut stojących na wszystkich dojazdach skrzyżowania na końcu każdego kroku decyzyjnego agenta (który trwał 5 sekund bez zmiany kierunku lub 8 sekund podczas zmiany). Ilustruje to tabela z dokładnymi wynikami oraz wykres poniżej:  
| | niski ruch | średni ruch | wysoki ruch |
|-|------------|-------------|-------------|
|baseline 10s|0.59|1.77|20.18|
|run1|0.86|1.45|11.49|
|run2|0.50|1.50|30.90|
|run3|0.40|1.11|16.15|
|run4|0.40|1.18|11.43|
|**średnia z agenta**|**0.54**|**1.31**|**17.49**|

![](img/charts.png)

Warto wziąć również pod uwagę, że światła trwające 10s miały najlepszy wynik spośród stałych czasów (np. przy 20s było to 1.09/3.10/26.29)  

Widzimy więc, że w małym ruchu run1 nie zdołał przebić baseline'u, a w wysokim nie udało się to drugiemu treningowi. Jednak w średnim ruchu, podobnie jak we wszystkich średnich wyniki te zostały przebite.

## Wizualizacja
Poniżej przedstawiam dwa screenshoty z dokładnie 70. sekundy przebiegu symulacji, pierwsza przy stałych światłach co 10 sekund, druga z modelu z run4. Naszym sterowanym skrzyżowaniem jest to znajdujące się w środku, oznaczone jako B1. Trasa to `routes_high_4.rou.xml`  

![Stałe światła 10s](img/sumo_70s_stale10s.png)

![Agent](img/sumo_70s_agent.png)

Na obrazku jeszcze lepiej widać, że nasz agent potrafi szybciej rozładować ruch, co również potwierdzają dana: na tej trasie średnia liczba stojących aut na skrzyżowaniu dla stałych świateł to 28.63, natomiast model zredukował to do 16.89.

Wizualizację można też uruchomić lokalnie, co jest opisane poniżej:

## Instalacja
Trening i testy zostały wykonane na Pythonie 3.13.1 i SUMO 1.28.0.  
### Jak zainstalować?
1. Zainstaluj SUMO i ustaw zmienną środowiskową `SUMO_HOME` na folder instalacji. Po zmianie zresetuj terminal.
2. Zainstaluj potrzebne biblioteki Pythona:

```
pip install -r requirements.txt
```
## Uruchamianie
Komendy wypisane poniżej należy uruchamiać z głównego folderu repozytorium.
```
# ocena wytrenowanego agenta w zależności od ruchu na trasach 4-6
python src/evaluate_agent.py run4

# baseline
python src/evaluate.py

# podgląd w SUMO: stałe światła, potem agent, na trasie high_4
python src/visualize.py run4

# wykres porównawczy (zapisuje img/charts.png)
python src/charts.py

# trening (500 epizodów), należy wpisać nazwę przebiegu
python src/train.py run5
```

Trening zapisuje model w `models/model_{nazwa}.pt` i przebieg treningu w `results/result_{nazwa}.csv`. Wytrenowane przeze mnie dotychczas modele również się tam znajdują.

## Opis działania agenta
Działamy na sieci skrzyżowań 3x3 wygenerowanej przez `netgenerate`, przy czym nasz agent koncentruje się wyłącznie na optymalizacji środkowego skrzyżowania B1 (reszta działa domyślnie, ze stałymi światłami). Środowisko zostało opisane w `src/env.py` w klasie `TrafficEnv`. Określa ona:
- Stan: sześcioelementową listę zawierająca aktualną liczbę aut stojących na każdym z czterech pasów dojazdowych do skrzyżowania (na pierwszych czterech miejscach) oraz aktualną fazę (na ostatnich dwóch miejscach tej listy)
- Akcję: decyzję, która para przeciwległych świateł ma dostać zielone światło
- Krok: trwa on 5 sekund symulacji (przy zmianie doliczane są 3 sekundy żółtego światła) 
- Nagrodę: naszą miarę potrzebną do doskonalenia modelu, czyli minus sumę stojących aut na dojazdach
- Koniec epizodu: opuszczenie skrzyżowania przez wszystkie auta

### Algorytm (`src/dqn.py, src/train.py`)
Algorytm to napisany od zera, przy pomocy Pytorchowych sieci neuronowych, schemat uczenia ze wzmocnieniem. 

Niech `s` oznacza stan, natomiast `a` - akcję. Wtedy `Q(s, a)` oznacza oczekiwaną sumę przyszłych nagród, jeśli agent wykona `a`, a później będzie podejmować optymalne decyzje. Wartość Q przewiduje sieć neuronowa (`src/qnetwork.py`), pobierając `s`, czyli sześcioelementową listę, oraz zwracając dwuelementową, z czego pierwsza wartość odpowiada Q dla akcji 0, a druga dla akjci 1, z czego akcje oznaczają zmianę lub zostanie przy obecnym przebiegu świateł. Sieć korzysta z aktywacji ReLU, aby wprowadzić nieliniowość między warstwami. Na końcu, agent wybiera akcję o większej ocenie, w ten sposób się ucząc.

**Pętla treningowa** (`src/train.py`) - poniżej znajduje się opis, co dzieje się w jednym kroku decyzyjnym:
1. `select_action`: korzysta ze strategii $\varepsilon$-zachłannej ($\varepsilon$-greedy), która z prawdopodobieństwem $\varepsilon$ wybiera losową akcję oraz z prawdopodobieństwem $1 - \varepsilon$ wybiera tę o większym `Q`
2. Środowisko wykonuje akcje i dostarcza informajce o aktualnej nagrodzie, nowym stanie oraz o tym, czy epizod się skończył
3. Doświadczenie `state, action, reward, next_state, done` trafia do naszego bufora `src/replay_buffer.py`
4. Gdy w buforze zbierze się 1000 doświadczeń, `learn_step` (z `src/dqn.py`) robi jeden krok uczenia sieci
5. Co 200 kroków aktualne wagi ucznonej sieci `model` są kopiowane do do sieci docelowej `target_net`

*Na czym polega krok uczenia?*
Z bufora losujemy paczkę 64 doświadczeń. Następnie sieć uczona przewiduje oceny obu akcji, a funkcja `gather` wybiera z nich te, które faktycznie wykonał agent. Cel, oznaczony jako `goal`, liczony jest ze wzoru:
`goal = rewards + gamma * next_q * (1 - dones)`, gdzie
- `rewards`: nagrody z tej paczki i podzielone przez 10
- `gamma`: współczynnik, który definiuje jak bardzo bierzemy przyszłość pod uwagę (0.95)
- `next_q`: najlepsza z dwóch ocen w nowym stanie, policzona przez `target_net`
- `dones`: 0, gdy epizod jeszcze trwa oraz 1, gdy się skończył; `(1 - dones)` powoduje zerowanie się przyszłości, gdy aktualny epizod się skończył

Zatem błąd to różnica między przewidywaniami naszego agenta oraz celem. W celu zmiejszenia tych błędów korzystamy z optymalizatora *Adam*, który poprawia wagi modelu. Sam cel liczony jest bez śledzenia gradientu, więc poprawki w wagach nie będą przesuwać nam celu.

*Dlaczego tak?*
 - Kolejne kroki symulacji są do siebie bardzo podobne, natomiast branie paczki losowych doświadczeń z naszego bufora zmniejsza korelacje i tworzy doświadczenia, które można wykorzystać wielokrotnie, dzięki czemu model zapamiętuje też rzadsze sytuacje.
 - Odświeżanie co 200 kroków zapewnia stały cel pomiędzy doświadczeniami, do których dąży nasz model
 - Algorytm $\varepsilon$-greedy sprawia, że na początku wybieramy często niekorzystne akcje, by sprawdzić wszystkie sceniariusze - $\varepsilon$ maleje liniowo od 1 do 0.05, dzięki czemu na początku sprawdza często losowe sytuacje, natomiast później coraz częsciej wybiera te z lepszymi Q.
 - Skalowanie (podzielenie `rewards` przez 10) powoduje, że wyjścia i wejścia mają rząd wielkości około jedności, przez co sieć lepiej się uczy.

 ### Wszystkie wykorzystane stałe:

|Hiperparametr|	Wartość|
|-------------|--------|
|learning rate (optymalizator	Adam)| 1e-3|
|gamma|	0,95|
|rozmiar paczki|	64|
|pojemność bufora|	20 000|
|start uczenia po|	1 000 doświadczeniach|
|odświeżanie sieci docelowej|	co 200 kroków uczenia|
|epizody|	500|
|$\varepsilon$|	liniowo od 1,0 do 0,05 w pierwszych 70% treningu|

### Trasy ruchu
Zostały one wygenerowane skryptem `randomTrips.py`, który jest dołączony do SUMO (nie ma go tutaj w repozytorium). Gotowe pliki tras znajdują się w folderze `sumo/routes`, z czego 1-3 służa wyłącznie do treningu, a 4-6 - do testowania.

## Ewaluacja
- Baselline: stały program świateł (10, 20 lub 40 sekund)
- Metryka: liczba aut stojących na dojazdach do skrzyżowania podzielona przez liczbę kroków oraz uśredniona po trasach dla każdego poziomu ruchu
- Agent gra zachłannie ($\varepsilon = 0$) na nieznanych dla niego trasach
- Agent losowy na końcu podany jest wyłącznie dla porównania wyników (co gdyby wybierać całkowicie losowe czasy zmiany świateł)

## Ograniczenia 
- **Przede wszystkim, tylko jedno skrzyżowanie**: Opytmalizujemy tylko jedno, środkowe skrzyżowanie, a reszta działa domyślnym programem. Rozszerzenie np. na całą siatkę 9 skrzyżowań byłoby czasochłonne, gdyż wymagałoby chociażby zmiany sposobu zapisywania stanu i podejmowania akcji, gdyż mają one różną liczbę ulic dojazdowych.
- Wysoki rozrzut wyników między treningami i trasami: Dla wysokiego ruchu rozciągają się one od 11.4 do 30.9 sekund, a jedne trasy są wyraźnie trudniejsze od innych. Doddatkowo, trening został wykonany tylko czterokrotnie, co prawdopodobnie jest zbyt małą próbą, by faktycznie ocenić wyniki i odrzucić wartości skrajne.
- To tylko prosta symulacja: wyniki dotyczą losowego ruchu na nierealistycznie regularnej siatce, a światła na pozostałych skrzyżowaniach nie reagują na żadne czujniki lub nie zmieniają czasu trwania w zależności od pory dnia - trwają tyle samo czasu przez cały okres symulacji. Nie wspominając też o zdarzeniach losowych, z którymi mamy do czynienia w prawdziwym życiu, takimi jak wypadki, a także np. o tramwaju wykolejającym się z torów na jezdni, jak to często bywa we Wrocławiu.

