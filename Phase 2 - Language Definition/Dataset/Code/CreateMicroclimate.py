import pandas as pd
import os
from datetime import datetime

# =======================================================
# 📝 1. PROJECT CONFIGURATION
# =======================================================
## 🏙️ Cities and Paths
CITIES = [
    'Trento', 'Povo', 'Rovereto', 'Tenno', 'Mezzana',
    'Predazzo', 'Lavarone', 'Telve', 'Cavalese', 'Arco'
]
BASE_PATH = '/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset/Dataset_API/'
FILE_PATTERN = 'open-meteo-{city}.csv'

## 💾 Output File
OUTPUT_MICROCLIMA = 'microclima.csv' # Kept original name for consistency

## 🏷️ Column Names (from CSV dataset)
TEMP_MEAN_COL = 'temperature_2m_mean (°C)'
HUM_MEAN_COL = 'relative_humidity_2m_mean (%)'
WIND_SPEED_COL = 'wind_speed_10m_mean (km/h)'
WIND_DIR_COL = 'winddirection_10m_dominant (°)'
PREC_COL = 'precipitation_sum (mm)' # Not used in final calculations, but kept for completeness

# =======================================================
# ⚙️ 2. MAIN ANALYSIS PROCESS
# =======================================================
microclima_rows = []

for city in CITIES:
    file_name = FILE_PATTERN.format(city=city)
    file_path = os.path.join(BASE_PATH, file_name)

    print(f"\n🔍 Processing: **{city}** (File: {file_name})")

    try:
        # 1. Reading the CSV: Skips the first 3 rows (metadata)
        df = pd.read_csv(file_path, skiprows=3, dayfirst=True)

        # 2. Checking for Essential Columns
        required_cols = [TEMP_MEAN_COL, HUM_MEAN_COL, WIND_SPEED_COL, WIND_DIR_COL]
        if not all(col in df.columns for col in required_cols):
            print(f"❌ ERROR in {file_name}: Missing columns. Required: {required_cols}")
            continue

        # 3. Converting 'time' Column to datetime format
        df['time'] = pd.to_datetime(df['time'], dayfirst=True)

        # -----------------------------------------------
        # 🛠️ METEOROLOGICAL CALCULATIONS
        # -----------------------------------------------

        ### Temperature Range
        min_temp = df[TEMP_MEAN_COL].min()
        max_temp = df[TEMP_MEAN_COL].max()
        temp_range_str = f"{min_temp:.1f}°C - {max_temp:.1f}°C"

        ### Humidity Range
        min_hum = df[HUM_MEAN_COL].min()
        max_hum = df[HUM_MEAN_COL].max()
        hum_range_str = f"{min_hum:.0f}% - {max_hum:.0f}%"

        ### Wind Analysis
        avg_wind_speed = df[WIND_SPEED_COL].mean()
        # Calculate dominant direction (mode), use 0 if empty
        dominant_wind_dir = df[WIND_DIR_COL].mode().iloc[0] if not df[WIND_DIR_COL].mode().empty else 0

        # Wind Strength Classification (Custom Scale)
        if avg_wind_speed < 5:
            wind_strength = "light winds"
        elif avg_wind_speed < 15:
            wind_strength = "moderate winds"
        elif avg_wind_speed < 30:
            wind_strength = "strong winds"
        else:
            wind_strength = "severe winds"

        wind_pattern_str = (
            f"{wind_strength}, avg {avg_wind_speed:.1f} km/h, dominant {dominant_wind_dir}°"
        )
        
        # -----------------------------------------------
        # 🌡️ MICROCLIMATE CLASSIFICATION (Based on Maximum Temperature)
        # -----------------------------------------------
        if max_temp < 12:
            microclimate = "alpine cold microclimate"
            type_micro = "cold"
        elif max_temp < 18:
            microclimate = "cool microclimate"
            type_micro = "mild"
        elif max_temp < 24:
            microclimate = "temperate microclimate"
            type_micro = "temperate"
        elif max_temp < 30:
            microclimate = "warm microclimate"
            type_micro = "warm"
        else:
            microclimate = "very warm microclimate"
            type_micro = "hot"

        # Analysis Period
        start_year = df['time'].dt.year.min()
        end_year = df['time'].dt.year.max()
        analysis_period = f"{start_year}-{end_year}"

        # -----------------------------------------------
        # 🏗️ CONSTRUCTING THE RESULT ROW
        # -----------------------------------------------
        microclima_row = {
            'City': city,
            'MicroClimate': f"{microclimate} ({analysis_period})",
            'TypeMicroCustom': type_micro,
            'TemperatureRange': temp_range_str,
            'HumidityRange': hum_range_str,
            'WindPattern': wind_pattern_str
        }

        microclima_rows.append(microclima_row)
        print(f"✅ Data extracted and classified: {microclimate} ({type_micro})")

    except FileNotFoundError:
        print(f"❌ ERROR: File not found for {city} at path {file_path}")
    except Exception as e:
        print(f"❌ Generic ERROR reading/processing {file_name}: {e}")

# =======================================================
# 📤 3. EXPORTING RESULTS
# =======================================================
print("\n" + "="*55)
if microclima_rows:
    # Converting the list of dictionaries to a DataFrame
    final_df = pd.DataFrame(microclima_rows)

    # Writing the DataFrame to a CSV file
    final_df.to_csv(OUTPUT_MICROCLIMA, index=False)
    
    # Printing the summary
    print(f"✅ SUCCESS! File '{OUTPUT_MICROCLIMA}' created.")
    print(f"   Total cities analyzed: **{len(final_df)}**")
    print("="*55)
    print("### Results Preview:")
    # Retaining the to_markdown() method as requested, assuming 'tabulate' is installed now.
    print(final_df.head().to_markdown(index=False)) 
    print("="*55)
else:
    print("❌ No data generated. Check directory, file names, and columns.")
    print("="*55)