import pandas as pd
import glob
import os

# Directory che contiene i file CSV
INPUT_FOLDER = "/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset/Dataset_API"

all_rows = []

# Cerca tutti i file del tipo open-meteo-*.csv nella directory indicata
pattern = os.path.join(INPUT_FOLDER, "open-meteo-*.csv")

for filepath in glob.glob(pattern):

    # Estrae il nome della città dal file (es: open-meteo-Arco.csv → Arco)
    city = os.path.basename(filepath).replace("open-meteo-", "").replace(".csv", "")

    # Carica i dati saltando le prime 3 righe
    df = pd.read_csv(filepath, skiprows=3)

    # Crea il DataFrame finale con le colonne richieste
    df_out = pd.DataFrame({
        "City": city,
        "Date": df["time"],
        "WeatherCode": df["weather_code (wmo code)"],
        "MaxHumidity (Percentage)": df["relative_humidity_2m_max (%)"],
        "MinHumidity (Percentage)": df["relative_humidity_2m_min (%)"],
        "MeanHumidity (Percentage)": df["relative_humidity_2m_mean (%)"],
        "WindDirection (Degree)": df["winddirection_10m_dominant (°)"],
        "MaxTemperature (Celsius)": df["temperature_2m_max (°C)"],
        "MinTemperature (Celsius)": df["temperature_2m_min (°C)"],
        "Precipitation (mm)": df["precipitation_sum (mm)"],
        "PrecipitationHours (h)": df["precipitation_hours (h)"],
        "WindGusts (km/h)": df["wind_gusts_10m_mean (km/h)"],
        "WindSpeed (km/h)": df["wind_speed_10m_mean (km/h)"],
        "MeanTemperature (Celsius)": df["temperature_2m_mean (°C)"]
    })

    all_rows.append(df_out)

# Unisce tutti i file
final_df = pd.concat(all_rows, ignore_index=True)

# Salva il file finale nella stessa directory
OUTPUT_FILE = os.path.join(INPUT_FOLDER, "weather_output.csv")
final_df.to_csv(OUTPUT_FILE, index=False)

print("File creato:", OUTPUT_FILE)
