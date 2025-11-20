import pandas as pd
import os
import numpy as np
from scipy.stats import linregress
# This script assumes 'scipy' is installed: pip install scipy

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
OUTPUT_CLIMATE_TREND = 'climate_trend_analysis.csv' # Renamed to reflect the analysis

## 🏷️ Column Names (from CSV dataset)
TEMP_MEAN_COL = 'temperature_2m_mean (°C)'
HUM_MEAN_COL = 'relative_humidity_2m_mean (%)'
WIND_SPEED_COL = 'wind_speed_10m_mean (km/h)'
WIND_DIR_COL = 'winddirection_10m_dominant (°)'
PREC_COL = 'precipitation_sum (mm)'

# -----------------------------------------------
# 📈 FUNCTION TO CALCULATE THE TREND (Linear Regression)
# -----------------------------------------------
def calculate_climate_trend(df, temp_col):
    """Calculates the annual trend using linear regression."""
    
    # 1. Convert time to "decimal years"
    # The origin (0) is the minimum year in the dataset
    min_date = df['time'].min()
    
    # Calculate time in days from the start of the period, then convert to years
    time_in_years = (df['time'] - min_date).dt.days / 365.25 
    
    # 2. Perform Linear Regression (OLS)
    # y = Temperature, x = Time (in years)
    slope, intercept, r_value, p_value, std_err = linregress(time_in_years, df[temp_col])
    
    # slope is the Rate of change: °C per year
    
    # 3. Determine the Total Variation (°C)
    start_year = df['time'].dt.year.min()
    end_year = df['time'].dt.year.max()
    years_diff = end_year - start_year
    total_variation = slope * years_diff
    
    # 4. Determine the Trend Description
    if abs(slope) < 0.05: # Threshold for near-zero variation
        trend_description = "Stable (Minimal Change)"
    elif slope > 0:
        trend_description = "Warming (Increase)"
    else:
        trend_description = "Cooling (Decrease)"
        
    return {
        'trend_description': trend_description,
        'rate': slope,
        'variation': total_variation,
        'years_diff': years_diff
    }

# =======================================================
# ⚙️ 2. MAIN ANALYSIS PROCESS
# =======================================================
microclima_rows = []

for city in CITIES:
    file_name = FILE_PATTERN.format(city=city)
    file_path = os.path.join(BASE_PATH, file_name)

    print(f"\n🔍 Processing: **{city}** (File: {file_name})")

    try:
        # 1. Read and Check Columns
        df = pd.read_csv(file_path, skiprows=3, dayfirst=True)
        required_cols = [TEMP_MEAN_COL] # Only temperature is needed for the trend
        if not all(col in df.columns for col in required_cols):
            print(f"❌ ERROR in {file_name}: Missing temperature column.")
            continue

        # 2. Converting 'time' Column
        df['time'] = pd.to_datetime(df['time'], dayfirst=True)

        # -----------------------------------------------
        # 🛠️ CLIMATE TREND CALCULATION
        # -----------------------------------------------
        trend_data = calculate_climate_trend(df, TEMP_MEAN_COL)
        
        start_year = df['time'].dt.year.min()
        end_year = df['time'].dt.year.max()

        # -----------------------------------------------
        # 🏗️ CONSTRUCTING THE RESULT ROW (Simplified Column Names)
        # -----------------------------------------------
        microclima_row = {
            'City': city,
            'ClimateTrendCustom': trend_data['trend_description'], # The long-term pattern
            'ParameterMeasuredCustom': TEMP_MEAN_COL,             # The variable measured
            'TimeWindowCustom': f"{start_year}-{end_year} ({trend_data['years_diff']:.1f} years)", # The period observed
            'VariationCustom': f"{trend_data['variation']:.2f}°C (total change)", # The change over time
            'RateCustom': f"{trend_data['rate']:.4f}°C/year",                     # The speed of change
        }

        microclima_rows.append(microclima_row)
        print(f"✅ Data extracted and classified: Trend = {trend_data['trend_description']}")

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
    final_df.to_csv(OUTPUT_CLIMATE_TREND, index=False)
    
    # Printing the summary
    print(f"✅ SUCCESS! File '{OUTPUT_CLIMATE_TREND}' created.")
    print(f"   Total cities analyzed: **{len(final_df)}**")
    print("="*55)
    print("### Results Preview:")
    # Uses to_markdown, which requires 'tabulate' to be installed
    print(final_df.head().to_markdown(index=False)) 
    print("="*55)
else:
    print("❌ No data generated. Check directory, file names, and columns.")
    print("="*55)