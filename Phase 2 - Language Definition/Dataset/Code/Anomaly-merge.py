import pandas as pd
import os

# Path alla cartella
BASE_PATH = "/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset"

# Nome del file
INPUT_FILE = os.path.join(BASE_PATH, "Anomaly.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "Anomaly2.csv")

# Carica il file CSV
df = pd.read_csv(INPUT_FILE)

# Converte DetectionDate nel formato ISO (AAAA-MM-GG)
df["DetectionDate"] = pd.to_datetime(df["DetectionDate"], format="%d/%m/%Y")

# Combina data + ora nel formato xsd:dateTime → AAAA-MM-GGTHH:MM:SS
df["DetectionDateTime"] = df["DetectionDate"].dt.strftime("%Y-%m-%d") + "T" + df["DetectionTime"]

# (Opzionale) Se vuoi rimuovere le due colonne originali:
# df = df.drop(columns=["DetectionDate", "DetectionTime"])

# Salva il nuovo file
df.to_csv(OUTPUT_FILE, index=False)

print("File creato:", OUTPUT_FILE)
