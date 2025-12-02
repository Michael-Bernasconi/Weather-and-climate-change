import pandas as pd
import os

# Path alla cartella
BASE_PATH = "/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset"

# File input/output
INPUT_FILE = os.path.join(BASE_PATH, "WeatherReport.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "WeatherReport_ISO.csv")

# Carica il CSV
df = pd.read_csv(INPUT_FILE)

# Mapping città → codici
city_codes = {
    "Lavarone": "T0032",
    "Trento": "T0356",
    "Povo": "T0142",
    "Mezzana": "T0071",
    "Arco": "T0322",
    "Tenno": "T0200",
    "Cavalese": "T0367",
    "Telve": "T0392",
    "Predazzo": "T0389",
    "Rovereto":"T0147"
}

# Aggiunge la colonna CityCode
df["CityCode"] = df["City"].map(city_codes)

# Controllo: eventuali città non presenti nel mapping
missing_codes = df[df["CityCode"].isna()]["City"].unique()
if len(missing_codes) > 0:
    print("Attenzione! Le seguenti città non hanno codice assegnato:", missing_codes)

# Salva il nuovo file CSV
df.to_csv(OUTPUT_FILE, index=False)

print("File creato:", OUTPUT_FILE)
