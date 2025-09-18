from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def line_trend_monthly(df: pd.DataFrame, outdir: Path):
    # Monatsmittel pro Stadt
    outdir.mkdir(parents=True, exist_ok=True)
    d = df.copy().sort_values("date")
    d["year_month"] = d["date"].values.astype("datetime64[M]") 
    monthly = d.groupby(["city", "year_month"])["tavg"].mean().reset_index()

    plt.figure(figsize=(10, 5))
    for city, g in monthly.groupby("city"):
        plt.plot(g["year_month"], g["tavg"], label=city, linewidth=1.8)
    plt.legend(title="Stadt", frameon=True)
    plt.xlabel("Monat")
    plt.ylabel("Ø Tagesmitteltemperatur (°C)")
    plt.title("Monatsmittel der Tagesmitteltemperatur")
    plt.tight_layout()
    plt.savefig(outdir / "line_tavg_monthly.png", dpi=200)
    plt.close()


def line_small_multiples(df: pd.DataFrame, outdir: Path):
    # pro Stadt ein Panel, 30 Tage Gleitmittel
    outdir.mkdir(parents=True, exist_ok=True)
    d = df.copy().sort_values("date")
    d["tavg_roll30"] = d.groupby("city")["tavg"].transform(
        lambda s: s.rolling(30, min_periods=10).mean()
    )

    cities = list(d["city"].unique())
    n = len(cities)
    cols = 2
    rows = int(np.ceil(n / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(12, 6), sharex=True, sharey=True)
    axes = axes.flat if n > 1 else [axes]

    for ax, city in zip(axes, cities):
        g = d[d["city"] == city]
        ax.plot(g["date"], g["tavg_roll30"], linewidth=1.8)
        ax.set_title(city)
        ax.set_xlabel("Datum")
        ax.set_ylabel("Ø Temp (°C)")
        ax.grid(True, alpha=0.3)

    for ax in axes[n:]:
        ax.axis("off")

    fig.suptitle("30-Tage-Gleitmittel der Tagesmitteltemperatur (je Stadt)", y=0.98)
    fig.tight_layout()
    fig.savefig(outdir / "line_tavg_small_multiples.png", dpi=200)
    plt.close(fig)


def bar_climatology(df: pd.DataFrame, outdir: Path):
    
    # Balken: Ø je Monat über alle Jahre und Fehlerbalken (Std).
    outdir.mkdir(parents=True, exist_ok=True)
    d = df.copy()
    d["month"] = d["date"].dt.month
    clim = d.groupby(["city", "month"])["tavg"].agg(["mean", "std"]).reset_index()

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(data=clim, x="month", y="mean", hue="city", errorbar=None)
    # Fehlerbalken
    for _, row in clim.iterrows():
        ax.errorbar(
            x=row["month"] - 1,  # seaborn kategorische Positionen starten bei 0
            y=row["mean"],
            yerr=row["std"],
            fmt="none",
            ecolor="black",
            elinewidth=0.6,
            capsize=2,
            alpha=0.6,
        )
    ax.set_xlabel("Monat")
    ax.set_ylabel("Ø Temp (°C)")
    ax.set_title("Klimatologie: Monatsmittel (±1σ) über alle Jahre")
    leg = ax.legend(title="Stadt")
    if leg is not None:
        leg.set_title("Stadt")
    plt.tight_layout()
    plt.savefig(outdir / "bar_monthly_climatology.png", dpi=200)
    plt.close()


def scatter_min_max(df: pd.DataFrame, outdir: Path):
    # Scatter mit Farbe pro Stadt 
    outdir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 5))
    sample_n = min(len(df), 6000)
    s = df.sample(sample_n, random_state=42) if len(df) > sample_n else df
    ax = sns.scatterplot(
        data=s,
        x="tmin",
        y="tmax",
        hue="city",
        alpha=0.5,
        edgecolor=None,
        s=18,
    )
    ax.set_xlabel("Tagesminimum (°C)")
    ax.set_ylabel("Tagesmaximum (°C)")
    ax.set_title("Streudiagramm: tmin vs. tmax")
    leg = ax.legend(title="Stadt")
    if leg is not None:
        leg.set_title("Stadt")
    plt.tight_layout()
    plt.savefig(outdir / "scatter_min_max.png", dpi=200)
    plt.close()


def scatter_min_max_hexbin(df: pd.DataFrame, outdir: Path):
    # Hexbin-Diagramm: tmin vs. tmax mit Anzahl der Tage in Farbe
    outdir.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6.5, 5))
    hb = plt.hexbin(df["tmin"], df["tmax"], gridsize=50, mincnt=5, cmap="viridis")
    plt.colorbar(hb, label="Anzahl Tage")
    plt.xlabel("Tagesminimum (°C)")
    plt.ylabel("Tagesmaximum (°C)")
    plt.title("Dichtediagramm: tmin vs. tmax (alle Städte)")
    plt.tight_layout()
    plt.savefig(outdir / "hexbin_min_max.png", dpi=200)
    plt.close()


def hist_tavg_facets(df: pd.DataFrame, outdir: Path):

    # Histogramm je Stadt ein Panel.
    outdir.mkdir(parents=True, exist_ok=True)
    g = sns.FacetGrid(df, col="city", col_wrap=2, sharex=True, sharey=True, height=3.2)
    g.map_dataframe(sns.histplot, x="tavg", stat="density", bins=40, element="step")
    g.set_axis_labels("Tagesmittel (°C)", "Dichte")
    g.set_titles("Stadt = {col_name}")

    plt.subplots_adjust(top=0.9)
    plt.suptitle("Verteilung der Tagesmitteltemperaturen (pro Stadt)", y=0.98)

    # Speichern & schließen
    plt.savefig(outdir / "hist_tavg_facets.png", dpi=200)
    plt.close()
