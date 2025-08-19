from pathlib import Path

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
PROC_DIR = DATA_DIR / "processed"
FIG_DIR = Path("figures")

CITIES = {
    "Berlin":   {"lat": 52.5200, "lon": 13.4050},
    "Hamburg":  {"lat": 53.5511, "lon": 9.9937},
    "Munich":   {"lat": 48.1351, "lon": 11.5820},
    "Cologne":  {"lat": 50.9375, "lon": 6.9603},
}

START = "2010-01-01"
END = "2020-12-31"