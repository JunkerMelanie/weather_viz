from src.data.meteostat_loader import fetch_all
from src.processing.transform import load_raw, clean_and_filter
from src.analysis.stats import city_stats
from src.viz.plots import (
    line_trend_monthly,
    line_small_multiples,
    bar_climatology,
    scatter_min_max,          # neu hinzugefügt (deutsche Legende)
    scatter_min_max_hexbin,   # bleibt
    hist_tavg_facets,         # Facetten mit "Stadt = ..."
)
from src.config import FIG_DIR, PROC_DIR

def run_pipeline():
    print("Fetching Meteostat data ...")
    fetch_all()

    print("Cleaning & interpolating ...")
    df_raw = load_raw()
    df = clean_and_filter(df_raw)

    print("Computing city stats ...")
    stats = city_stats(df)
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    stats_path = PROC_DIR / "city_stats.csv"
    stats.to_csv(stats_path, index=False)
    print(f"Saved stats to {stats_path}")

    print("Creating figures ...")
    line_trend_monthly(df, FIG_DIR)
    line_small_multiples(df, FIG_DIR)
    bar_climatology(df, FIG_DIR)
    scatter_min_max(df, FIG_DIR)
    scatter_min_max_hexbin(df, FIG_DIR)
    hist_tavg_facets(df, FIG_DIR)
    print("Done. See figures/.")

if __name__ == "__main__":
    run_pipeline()
