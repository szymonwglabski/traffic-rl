import matplotlib.pyplot as  plt
import seaborn as sns
import pandas as pd

data = [
    {"Kategoria": "Low", "Próba": "baseline", "wartosc": 0.59},
    {"Kategoria": "Low", "Próba": "run1", "wartosc": 0.86},
    {"Kategoria": "Low", "Próba": "run2", "wartosc": 0.50},
    {"Kategoria": "Low", "Próba": "run3", "wartosc": 0.40},
    {"Kategoria": "Low", "Próba": "run4", "wartosc": 0.40},

    {"Kategoria": "Mid", "Próba": "baseline", "wartosc": 1.77},
    {"Kategoria": "Mid", "Próba": "run1", "wartosc": 1.45},
    {"Kategoria": "Mid", "Próba": "run2", "wartosc": 1.50},
    {"Kategoria": "Mid", "Próba": "run3", "wartosc": 1.11},
    {"Kategoria": "Mid", "Próba": "run4", "wartosc": 1.18},

    {"Kategoria": "High", "Próba": "baseline", "wartosc": 20.18},
    {"Kategoria": "High", "Próba": "run1", "wartosc": 11.49},
    {"Kategoria": "High", "Próba": "run2", "wartosc": 30.90},
    {"Kategoria": "High", "Próba": "run3", "wartosc": 16.15},
    {"Kategoria": "High", "Próba": "run4", "wartosc": 11.43},
]

df = pd.DataFrame(data)

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(1, 3, figsize=(14, 6))
categories = ["Low", "Mid", "High"]

for i, cat in enumerate(categories):
    ax = axes[i]
    sub_df = df[df["Kategoria"] == cat]
    
    sns.barplot(
    data=sub_df,
    x="Próba",
    y="wartosc",
    hue="Próba",
    palette="viridis",
    ax=ax,
    errorbar=None,
    legend=False
    )


    ax.set_xlabel(f"Natężenie ruchu: {cat}", fontsize=12)

    if i == 0:
        ax.set_ylabel("Średnia liczba stojących aut", fontsize=12)
    else:
        ax.set_ylabel("")

    ax.tick_params(axis="x", rotation=15)

fig.suptitle("Wykresy średniej liczby aut na jeden krok symulacji w zależności od natężenia ruchu",
           fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts.png", dpi=150)
plt.show()