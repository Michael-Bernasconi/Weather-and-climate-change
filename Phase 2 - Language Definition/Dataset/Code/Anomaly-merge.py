import pandas as pd
import os

# Path alla cartella
BASE_PATH = "/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset"

# Nome del file
INPUT_FILE = os.path.join(BASE_PATH, "WeatherReport.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "WeatherReport_ISO.csv")

# Carica il file CSV
df = pd.read_csv(INPUT_FILE)

# Converte il campo Date dal formato gg/mm/aaaa al formato ISO AAAA-MM-GG
df["Date_ISO"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")

# Crea un campo xsd:dateTime aggiungendo mezzanotte T00:00:00
df["DateTime_xsd"] = df["Date_ISO"] + "T00:00:00"

# (Opzionale) rimuovere la colonna originale Date
# df = df.drop(columns=["Date"])

# Salva il nuovo file CSV
df.to_csv(OUTPUT_FILE, index=False)

print("File creato:", OUTPUT_FILE)
