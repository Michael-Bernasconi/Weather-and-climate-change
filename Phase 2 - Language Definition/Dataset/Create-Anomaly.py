import pandas as pd
import numpy as np
import random
from datetime import timedelta, datetime
import os

# --- 1. CONFIGURATION AND DEFINITIONS ---

# The 10 cities for which we must generate anomalies
CITIES = [
    'Trento', 'Povo', 'Rovereto', 'Tenno', 'Mezzana',
    'Predazzo', 'Lavarone', 'Telve', 'Cavalese', 'Arco'
]

# Base dataset path
BASE_PATH = '/home/michael/Weather-and-climate-change/Phase 2 - Language Definition/Dataset/Dataset_API/'
# File name pattern (where {city} gets replaced)
FILE_PATTERN = 'open-meteo-{city}.csv'

# Date interval requested as reference/fallback
START_DATE_REQ = pd.to_datetime('01/01/1990', dayfirst=True)
END_DATE_REQ = pd.to_datetime('31/10/2025', dayfirst=True)

# Anomaly and TypeAnomaly definitions
ANOMALY_DEFINITIONS = {
    "Extreme Heat Wave": "Too Hot Temperature",
    "Intense Cold Peak": "Too Cold Temperature",
    "Torrential Rainfall": "Excessive Precipitation",
    "Severe Drought": "Prolonged Low Precipitation",
    "Record Wind": "Excessive Wind",
    "Sudden Hail": "Solid Precipitation",
    "Dense Fog": "Reduced Visibility"
}

# Severity levels
SEVERITIES = ['Critical', 'High', 'Medium', 'Low']


# --- 2. LOAD FILES AND COLLECT DATES ---

all_dates = set()
files_info = []   # << new: store file name + full path
files_read_successfully = 0

print("Starting date aggregation from the 10 local files...\n")

for city in CITIES:
    file_name = FILE_PATTERN.format(city=city)
    file_path = os.path.join(BASE_PATH, file_name)

    try:
        df = pd.read_csv(
            file_path,
            skiprows=4,
            usecols=['time'],
            parse_dates=['time'],
            dayfirst=True
        )

        all_dates.update(df['time'].dt.normalize().unique())
        files_read_successfully += 1

        files_info.append({
            "City": city,
            "FileName": file_name,
            "FilePath": file_path,
            "Loaded": True
        })

    except Exception as e:
        print(f"⚠️ ERROR reading '{file_name}': {e}")
        files_info.append({
            "City": city,
            "FileName": file_name,
            "FilePath": file_path,
            "Loaded": False
        })


# --- 3. FINALIZE DATE SET ---

if files_read_successfully > 0:
    dates_to_process = pd.to_datetime(list(all_dates))
    dates_to_process = dates_to_process[
        (dates_to_process >= START_DATE_REQ) & (dates_to_process <= END_DATE_REQ)
    ]
    dates_to_process = sorted(dates_to_process)

    print(f"✅ Dates successfully loaded from {files_read_successfully} files. Total unique days: {len(dates_to_process)}")
else:
    dates_to_process = pd.date_range(start=START_DATE_REQ, end=END_DATE_REQ, freq='D')
    print("🚨 No files readable. Using full date range fallback.")


# --- 4. GENERATE ANOMALIES ---

print("\nGenerating simulated anomaly events...\n")

anomaly_data = []

for date in dates_to_process:
    num_anomalies_for_day = random.randint(0, 3)

    for _ in range(num_anomalies_for_day):
        anomaly_name, type_anomaly = random.choice(list(ANOMALY_DEFINITIONS.items()))
        severity = random.choice(SEVERITIES)
        city = random.choice(CITIES)

        detection_time = timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        detection_datetime = pd.to_datetime(date) + detection_time

        anomaly_data.append({
            'TypeAnomaly': type_anomaly,
            'Severity': severity,
            'DetectionDate': detection_datetime.strftime('%d/%m/%Y'),
            'DetectionTime': detection_datetime.strftime('%H:%M:%S'),
            'Anomaly': anomaly_name,
            'City': city
        })


# --- 5. EXPORT anomaly.csv ---

df_anomaly = pd.DataFrame(anomaly_data)
df_anomaly = df_anomaly[['TypeAnomaly', 'Severity', 'DetectionDate', 'DetectionTime', 'Anomaly', 'City']]

anomaly_output = 'anomaly.csv'
df_anomaly.to_csv(anomaly_output, index=False)

print("=======================================================")
print(f"✅ SUCCESS! File '{anomaly_output}' has been created.")
print(f"   Total Generated Records: {len(df_anomaly)}")
print(f"   Covered Period: {df_anomaly['DetectionDate'].min()} → {df_anomaly['DetectionDate'].max()}")
print("=======================================================\n")

print("First 5 rows:")
print(df_anomaly.head())


# --- 6. EXPORT file paths summary (NEW) ---

df_files = pd.DataFrame(files_info)
files_output = 'loaded_files.csv'
df_files.to_csv(files_output, index=False)

print(f"\n📁 A second CSV '{files_output}' has been created with:")
print("- City")
print("- File name")
print("- Full path")
print("- Whether the file was loaded successfully")
