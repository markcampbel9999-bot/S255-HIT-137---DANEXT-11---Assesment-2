# Group Name: DAN/EXT 11
# Team Members
# Jarrah Brain - S392191
# Mark Campbell - S385026
# Craig Shaw - S396655
# Dan Williams - S391056

"""
Program: Temperature Data Analysis
Description: Analyses multi-year Australian weather station temperature data
stored in multiple CSV files. Calculates seasonal averages,
largest temperature range, and temperature stability.
"""

import csv
import os
import math

# Folder containing all temperature CSV files, located relative to the
# program file. Ensures portability.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPERATURE_FOLDER = os.path.join(BASE_DIR, "temperatures")

# Australian seasons as related to the month columns
SEASONS = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"]
}

# Data storage
seasonal_temps = {season: [] for season in SEASONS}
station_temps = {}

# --------------------------------------------------
# Read and process all CSV files
# --------------------------------------------------
for filename in os.listdir(TEMPERATURE_FOLDER):
    if filename.lower().endswith(".csv"):
        file_path = os.path.join(TEMPERATURE_FOLDER, filename)

        with open(file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            # Process each weather station entry in the file
            for row in reader:
                station_key = f"{row['STATION_NAME']} ({row['STN_ID']})"

                if station_key not in station_temps:
                    station_temps[station_key] = []

                # Process each month
                for season, months in SEASONS.items():
                    for month in months:
                        try:
                            temp = float(row[month])
                            # ignore missing values (NaN)
                            if not math.isnan(temp):
                                seasonal_temps[season].append(temp)
                                station_temps[station_key].append(temp)
                        # missing columns
                        except (ValueError, KeyError):
                            pass

# --------------------------------------------------
# 1. Seasonal Average Temperatures
# --------------------------------------------------

# Write the average temperature for each season as a txt file
with open("average_temp.txt", "w") as file:
    for season, temps in seasonal_temps.items():
        # calculate average temp
        average = sum(temps) / len(temps)
        file.write(f"{season}: {average:.1f}°C\n")

# --------------------------------------------------
# 2. Largest Temperature Range
# --------------------------------------------------

# Find the largest temp range and the corresponding station
largest_range = -1
largest_range_stations = []

for station, temps in station_temps.items():
    max_temp = max(temps)
    min_temp = min(temps)
    temp_range = max_temp - min_temp

# The program iteratively compares each station’s temperature
# range to the largest range found so far, updating the result
# when a larger value is encountered.
    if temp_range > largest_range:
        largest_range = temp_range
        largest_range_stations = [(station, max_temp, min_temp)]

    # include stations that tie for the largest range
    elif math.isclose(temp_range, largest_range):
        largest_range_stations.append((station, max_temp, min_temp))

# Write results to txt file
with open("largest_temp_range_station.txt", "w") as file:
    for station, max_temp, min_temp in largest_range_stations:
        file.write(
            f"{station}: Range {max_temp - min_temp:.1f}°C "
            f"(Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n"
        )

# --------------------------------------------------
# 3. Temperature Stability (Standard Deviation)
# --------------------------------------------------
standard_deviations = {}

for station, temps in station_temps.items():
    mean = sum(temps) / len(temps)
    variance = sum((t - mean) ** 2 for t in temps) / len(temps)
    standard_deviations[station] = math.sqrt(variance)

# determine smallest and largest standard deviations
min_std = min(standard_deviations.values())
max_std = max(standard_deviations.values())

# identify stations with the most stable temperatures
most_stable = [
    station for station, std in standard_deviations.items()
    if math.isclose(std, min_std)
]

# Identify stations with the most variable temperatures
most_variable = [
    station for station, std in standard_deviations.items()
    if math.isclose(std, max_std)
]

# Write results to a text file
with open("temperature_stability_stations.txt", "w") as file:
    for station in most_stable:
        file.write(
            f"Most Stable: {station}: StdDev {standard_deviations[station]:.1f}°C\n"
        )
    for station in most_variable:
        file.write(
            f"Most Variable: {station}: StdDev {standard_deviations[station]:.1f}°C\n"
        )

input("\nProcessing complete. Press Enter to exit...")
