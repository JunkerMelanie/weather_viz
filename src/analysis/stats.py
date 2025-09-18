import pandas as pd

# Group by city and calculate statistics
def city_stats(df: pd.DataFrame) -> pd.DataFrame:
    agg = (
        df.groupby("city")
          .agg(
              avg_temp=("tavg","mean"), # average temperature
              min_temp=("tmin","min"), # minimum temperature
              max_temp=("tmax","max"), # maximum temperature
              std_temp=("tavg","std"), # standard deviation of average temperature
          )
          .reset_index()
    )
    return agg.round({"avg_temp":2, "min_temp":1, "max_temp":1, "std_temp":2})