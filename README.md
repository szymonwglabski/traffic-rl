# Sterowanie sygnalizacją świetlną za pomocą  uczenia ze wzmocnieniem
Projekt stara się sprostać zadaniu optymalizacji skrzyżowania w ruchu drogowym. Agent uczenia ze wzmocnieniem, napisany w Pytorchu, steruje sygnalizacją świetlną symulacji w środowisku SUMO tak, aby jak najbardziej ograniczyć czas i ilość pojazdów stojących przed skrzyżowaniem, dodatkowo rozpatrując różne natężenia ruchu 

## Wyniki 
Agent osiągał średnio lepsze wyniki niż stałe światła trwające 10 sekund. Testy zostałe wykoanne na trzech nowych, losowo wygenerowanych trasach, przez co można zauważyć, że trasa nr 2 była zdecydowanie trudniejsza od pozostałych. Jako miarę przyjąłem średnią liczbę aut stojących na wszystkich dojazdach skrzyżowania na końcu każdego kroku decyzyjnego agentu (który trwał 5 sekund bez zmiany kierunku lub 8 sekund podczas zmiany). Ilustruje to tabela poniżej:  
| | niski ruch | średni ruch | wysoki ruch |
|-|------------|-------------|-------------|
|baseline 10s|0.59|1.77|20.18|
|run1|0.86|1.45|11.49|
|run2|0.50|1.50|30.90|
|run3|0.40|1.11|16.15|
|run4|0.40|1.18|11.43|
|średnia z agenta|0.54|1.31|17.49|

Warto wziąć również pod uwagę, że światła trwające 10s miały najlepszy wynik spośród stałych czasów (np. przy 20s było to 1.09/3.10/26.29)  

Widzimy więc, że w małym ruchu run1 nie zdołał przebić baseline'u, a w wysokim nie udało się to drugiemu treningowi. Jednak w średnim ruchu, podobnie jak we wszystkich średnich wyniki te zostały przebite.

## Wizualizacja
Poniżej przedstawiam dwa screenshoty z dokładnie 70. sekundy przebiegu symulacji, pierwsza przy stałych światłach co 10 sekund, druga z modelu z run4. Naszym sterowanym skrzyżowaniem jest to znajdujące się w środku, oznaczone jako B1. Trasa to routes_high_4.rou.xml  

![Stałe światła 10s](img/sumo_70s_stale10s.png)

![Agent](img/sumo_70s_agent.png)