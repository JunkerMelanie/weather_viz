from datetime import datetime
from meteostat import Point, Daily, Stations
import pandas as pd
from src.config import RAW_DIR, CITIES, START, END

def best_station(lat: float, lon: float, start_dt: datetime, end_dt: datetime):
    
    # Nimm die erste Station aus dem gefilterten Set in der Nähe der Koordinaten.
    
    stns = Stations().nearby(lat, lon).inventory('daily', (start_dt, end_dt))
    df_stn = stns.fetch()
    if df_stn.empty:
        return None
    return df_stn.index[0]  # station id

def fetch_city_daily(name: str, lat: float, lon: float, start: str, end: str) -> pd.DataFrame:
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    sid = best_station(lat, lon, start_dt, end_dt)
    if sid is not None:
        df = Daily(sid, start_dt, end_dt).fetch()
    else:
        # Fallback: direkt über die Koordinaten
        loc = Point(lat, lon)
        df = Daily(loc, start_dt, end_dt).fetch()

    df = df.reset_index().rename(columns={"time": "date"})
    df["city"] = name
    keep = ["date", "city", "tavg", "tmin", "tmax"]
    return df[keep]

def fetch_all() -> pd.DataFrame:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    frames = []
    for city, coords in CITIES.items():
        frames.append(fetch_city_daily(city, coords["lat"], coords["lon"], START, END))
    df = pd.concat(frames, ignore_index=True)
    df.to_parquet(RAW_DIR / "daily_all.parquet", index=False)
    return df