import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIGURATION ---

CITIES = [
    'Trento', 'Povo', 'Rovereto', 'Tenno', 'Mezzana',
    'Predazzo', 'Lavarone', 'Telve', 'Cavalese', 'Arco'
]

BASE_PATH = '/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset/Dataset_API/'
FILE_PATTERN = 'open-meteo-{city}.csv'

OUTPUT_SEASON = 'season.csv'


# --- 2. FUNCTION TO MAP DATE TO SEASON (ITALIAN ASTRONOMICAL DATES) ---

def date_to_season(date):
    month = date.month
    day = date.day

    if (month == 12 and day >= 21) or (month in [1, 2]) or (month == 3 and day <= 19):
        return "Winter"
    elif (month == 3 and day >= 20) or (month in [4, 5]) or (month == 6 and day <= 20):
        return "Spring"
    elif (month == 6 and day >= 21) or (month in [7, 8]) or (month == 9 and day <= 22):
        return "Summer"
    else:
        return "Autumn"


# --- 3. PROCESS ALL CITIES ---

season_rows = []

for city in CITIES:
    file_name = FILE_PATTERN.format(city=city)
    file_path = os.path.join(BASE_PATH, file_name)

    try:
        df = pd.read_csv(
            file_path,
            skiprows=3,        # Corretto: salta 3 righe per l'intestazione
            dayfirst=True
        )

        # Check required columns
        if 'time' not in df:
            print(f"❌ ERROR in {file_name}: column 'time' not found after skiprows.")
            continue

        temp_col = 'temperature_2m_mean (°C)'
        prec_col = 'precipitation_sum (mm)'
        
        if temp_col not in df or prec_col not in df:
            print(f"❌ ERROR in {file_name}: required columns missing.")
            continue

        # Convert time column to datetime
        df['time'] = pd.to_datetime(df['time'], dayfirst=True)
        
        # 🌟 NUOVA AGGIUNTA: Estrai l'anno dalla colonna 'time'
        df['Year'] = df['time'].dt.year 

        # Assign season
        df['Season'] = df['time'].apply(date_to_season)

        # 🌟 MODIFICA CHIAVE: Raggruppa per 'Year' E 'Season'
        grouped = df.groupby(['Year', 'Season']).agg(
            AverageTemperature=(temp_col, 'mean'),
            AveragePrecipitation=(prec_col, 'mean')
        ).reset_index()

        grouped['City'] = city
        
        # Filtra i dati solo per l'intervallo 1990-2025 (anche se la groupby li avrebbe inclusi, questo è un controllo)
        grouped = grouped[(grouped['Year'] >= 1990) & (grouped['Year'] <= 2025)]


        season_rows.append(grouped)

    except Exception as e:
        print(f"❌ ERROR reading {file_name}: {e}")


# --- 4. EXPORT RESULT ---

if season_rows:
    final_df = pd.concat(season_rows, ignore_index=True)
    
    # Arrotonda i risultati come richiesto
    final_df['AverageTemperature'] = final_df['AverageTemperature'].round(1)
    final_df['AveragePrecipitation'] = final_df['AveragePrecipitation'].round(1)
    
    # Riorganizza le colonne per una migliore leggibilità
    final_df = final_df[['City', 'Year', 'Season', 'AverageTemperature', 'AveragePrecipitation']]
    
    final_df.to_csv(OUTPUT_SEASON, index=False)

    print("\n============================================")
    print(f"✅ SUCCESSO! '{OUTPUT_SEASON}' è stato creato.")
    print(f"   Totale righe: {len(final_df)} (4 stagioni * 10 città * anni totali)")
    print("============================================\n")

    print(final_df.head(8)) # Mostra di più per far vedere anni e città

else:
    print("❌ Nessun dato stagionale calcolato. Verifica percorsi e intestazioni.")