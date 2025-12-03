import pandas as pd
import os

# Path alla cartella
BASE_PATH = "/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset"

# File input/output
INPUT_FILE = os.path.join(BASE_PATH, "WeatherReport-minimum.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "WeatherReportMinimum2.csv")

# Carica il CSV
df = pd.read_csv(INPUT_FILE)
df["Date"] = pd.to_datetime(df["Date"])
# Filtra le righe con anno tra 2010 e 2025 (inclusi)
df_filtered = df[(df["Date"].dt.year >= 2010) & (df["Date"].dt.year <= 2025)]

# Salva il nuovo file
df_filtered.to_csv("dati_meteo_2010_2025.csv", index=False)

print("File generato: dati_meteo_2010_2025.csv")
