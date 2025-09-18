import pandas as pd
from src.config import RAW_DIR, PROC_DIR

# Load the raw parquet file into a DataFrame
def load_raw() -> pd.DataFrame:
    return pd.read_parquet(RAW_DIR / "daily_all.parquet")

# Sort data by date and set 'date' as index and interpolate missing values
def _interp_city(g: pd.DataFrame, max_gap_days: int) -> pd.DataFrame:
    g = g.sort_values("date").set_index("date")
    for col in ["tavg", "tmin", "tmax"]:
        g[col] = g[col].interpolate(limit=max_gap_days, limit_direction="both")
    return g.reset_index()

# Clean and filter the DataFrame, removing rows with NaN in specified columns
def clean_and_filter(df: pd.DataFrame, max_gap_days: int = 3) -> pd.DataFrame:
    df = df.sort_values(["city", "date"]).copy()
    parts = []
    for city, g in df.groupby("city", sort=False):
        parts.append(_interp_city(g, max_gap_days))
    df = pd.concat(parts, ignore_index=True)
    df = df.dropna(subset=["tavg", "tmin", "tmax"])
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROC_DIR / "daily_clean.parquet", index=False)
    return df
