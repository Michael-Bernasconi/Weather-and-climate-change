import os
import pandas as pd
import numpy as np

# Base directory
base_dir = os.path.expanduser("~/Scaricati/Telve")
output_file = os.path.join(base_dir, "Telve_2000_2025_clean.csv")

# Month mapping (for sorting)
months = {
    "Gennaio": 1, "Febbraio": 2, "Marzo": 3, "Aprile": 4,
    "Maggio": 5, "Giugno": 6, "Luglio": 7, "Agosto": 8,
    "Settembre": 9, "Ottobre": 10, "Novembre": 11, "Dicembre": 12
}

# Columns to keep and rename
columns_map = {
    "LOCALITA": "Location",
    "DATA": "Date",
    "TMEDIA °C": "MeanTemp",
    "TMIN °C": "MinTemperature",
    "TMAX °C": "MaxTemperature",
    "UMIDITA %": "MeanHumidity",
    "VENTOMEDIA km/h": "WindSpeed",
    "RAFFICA km/h": "WindGusts",
    "PIOGGIA mm": "Rainfall",
    "FENOMENI": "Phenomena"
}

# Common translation dictionary for Phenomena
phenomena_translation = {
    "pioggia": "rain",
    "pioggia temporale": "thunderstorm",
    "temporale": "thunderstorm",
    "neve": "snow",
    "nevischio": "sleet",
    "grandine": "hail",
    "foschia": "mist",
    "nebbia": "fog",
    "sereno": "clear",
    "nubi sparse": "partly cloudy",
    "coperto": "overcast"
}

# Funzione per tradurre fenomeni multipli
def translate_phenomena(text):
    if pd.isna(text):
        return np.nan
    parts = text.lower().strip().split()
    translated = []
    skip_next = False
    for i, part in enumerate(parts):
        if skip_next:
            skip_next = False
            continue
        # Gestione fenomeni composti come "pioggia temporale"
        if i < len(parts) - 1:
            combo = f"{part} {parts[i+1]}"
            if combo in phenomena_translation:
                translated.append(phenomena_translation[combo])
                skip_next = True
                continue
        # Singolo fenomeno
        translated.append(phenomena_translation.get(part, part))
    return " ".join(translated)

# Trova le cartelle annuali
years = sorted([
    d for d in os.listdir(base_dir)
    if d.isdigit() and 2000 <= int(d) <= 2025
])

all_data = []

for year in years:
    year_path = os.path.join(base_dir, year)
    for file in os.listdir(year_path):
        if file.startswith("Telve-") and file.endswith(".csv"):
            month_name = file.split("-")[2].replace(".csv", "").capitalize()
            month_num = months.get(month_name, 0)
            if month_num == 0:
                continue

            file_path = os.path.join(year_path, file)
            print(f"📂 Reading {file_path}")

            try:
                # Read CSV forcing correct separator
                df = pd.read_csv(file_path, sep=';', engine='python', dtype=str)

                # Fix number of columns if misaligned
                expected_cols = list(columns_map.keys())
                df = df.loc[:, df.columns.intersection(expected_cols)]

                # Ensure all expected columns exist (add missing as empty)
                for col in expected_cols:
                    if col not in df.columns:
                        df[col] = np.nan

                # Keep and rename
                df = df[expected_cols].rename(columns=columns_map)

                # Replace commas with dots for numeric columns
                numeric_cols = [
                    "MeanTemp", "MinTemperature", "MaxTemperature",
                    "MeanHumidity", "WindSpeed", "WindGusts", "Rainfall"
                ]
                for col in numeric_cols:
                    df[col] = df[col].astype(str).str.replace(",", ".").replace("nan", np.nan)

                # Traduci fenomeni multipli
                df["Phenomena"] = df["Phenomena"].apply(translate_phenomena)

                all_data.append(df)

            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")

# Merge e export
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(output_file, sep=';', index=False)
    print(f"\n✅ Clean dataset created: {output_file}")
else:
    print("❌ No valid files found.")
