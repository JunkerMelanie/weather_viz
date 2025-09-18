# Weather Data Visualization (Meteostat) — Example Project

This project demonstrates the complete process of **analyzing and visualizing historical weather data** for four major German cities: **Berlin**, **Hamburg**, **Munich**, and **Cologne**.  
It uses the [Meteostat Python library](https://dev.meteostat.net/python/) to fetch weather data, clean and process it, compute statistical metrics, and visualize the results using different chart types.

## Cities & Time Period

- Berlin (52.5200, 13.4050)
- Hamburg (53.5511, 9.9937)
- Munich (48.1351, 11.5820)
- Cologne (50.9375, 6.9603)

Default time range: **2010-01-01** to **2020-12-31**  
(Changeable in `src/config.py`.)

## Project Goals

- Automatically retrieve historical weather data via the Meteostat library
- Clean and interpolate missing values
- Calculate statistical indicators (average, min, max, standard deviation)
- Visualize the data using **line, bar, scatter, and histogram plots**
- Compare the suitability of different visualization types for various analytical tasks

## Installation & Usage

```bash
# Clone repository
git clone <REPO-URL>
cd weather-viz

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run pipeline
python main.py

# Data Source & Attribution
Data is retrieved via the Meteostat Python library and originates from official meteorological archives.
Please review and comply with the Meteostat terms of use and the respective original data providers.

# Notes
No API key is required for the Meteostat Python library.
Raw data files are not committed to the repository; they are generated locally during the first run.
The project is modular and can easily be extended with more cities, different time ranges, or additional chart types.