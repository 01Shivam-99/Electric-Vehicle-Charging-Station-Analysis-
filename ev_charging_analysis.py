"""
Project 26: Electric Vehicle Charging Station Analysis
Student: Shivam Mishra | ABES Engineering College, Ghaziabad (B.Tech, ELCE)
Admission No: 2026B022310161 
git hub repo: https://github.com/01Shivam-99/Electric-Vehicle-Charging-Station-Analysis-.git

This script performs complete data cleaning, exploratory analysis, statistical
summaries (NumPy + Pandas), core Python data structures & OOP demonstration,
and produces five evidence-based operational recommendations.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ============================================================
# 1. LOAD AND INSPECT RAW DATA (FR1)
# ============================================================
print("=" * 70)
print("1. LOADING AND INSPECTING RAW DATASET")
print("=" * 70)

df_raw = pd.read_csv("26_ev_charging_sessions.csv")
print(f"Shape (rows, columns): {df_raw.shape}")
print(f"\nColumn names:\n{list(df_raw.columns)}")
print(f"\nData types:\n{df_raw.dtypes}")
print(f"\nFirst 5 rows:\n{df_raw.head()}")
print(f"\nBasic info:")
df_raw.info()

# ============================================================
# 2. DATA QUALITY CHECKS – MISSING VALUES & DUPLICATES (FR2)
# ============================================================
print("\n" + "=" * 70)
print("2. DATA QUALITY CHECKS")
print("=" * 70)

print("\nMissing values per column:")
missing = df_raw.isnull().sum()
missing_pct = (df_raw.isnull().sum() / len(df_raw) * 100).round(2)
quality_df = pd.DataFrame({"Missing_Count": missing, "Missing_%": missing_pct})
print(quality_df)

print(f"\nTotal missing Energy_kWh: {df_raw['Energy_kWh'].isnull().sum()} "
      f"({missing_pct['Energy_kWh']}%)")
print(f"Total missing Charging_Duration_Mins: {df_raw['Charging_Duration_Mins'].isnull().sum()} "
      f"({missing_pct['Charging_Duration_Mins']}%)")

# Check if missing values occur in the same rows
both_missing = df_raw[df_raw['Energy_kWh'].isnull() & df_raw['Charging_Duration_Mins'].isnull()]
print(f"Rows with BOTH Energy_kWh and Duration missing: {len(both_missing)}")

# Duplicate Session_IDs
dup_session_ids = df_raw[df_raw.duplicated(subset=['Session_ID'], keep=False)]
n_dup_ids = df_raw['Session_ID'].duplicated().sum()
print(f"\nDuplicate Session_ID records (extra copies): {n_dup_ids}")
print(f"Total rows with duplicated Session_ID (including originals): {len(dup_session_ids)}")
print(f"Unique Session_IDs: {df_raw['Session_ID'].nunique()}")
print(f"Total rows: {len(df_raw)}")

# Exact duplicate rows
exact_dups = df_raw.duplicated().sum()
print(f"Exact duplicate rows: {exact_dups}")

# ============================================================
# 3. CLEANING – DEDUPLICATION & IMPUTATION (FR3)
# ============================================================
print("\n" + "=" * 70)
print("3. DATA CLEANING")
print("=" * 70)

# Keep first occurrence of each Session_ID
df = df_raw.drop_duplicates(subset=['Session_ID'], keep='first').copy()
print(f"Rows after removing duplicate Session_IDs: {len(df)} "
      f"(removed {len(df_raw) - len(df)} duplicates)")

# Imputation strategy (justified):
# Missing Energy_kWh and Charging_Duration_Mins are imputed with the
# median of the same Charger_Type. Median is robust to extreme values
# (some sessions last >300 mins) and preserves the central tendency
# of each charger technology.
print("\nImputation method: Median of each Charger_Type group")
print("Justification: Median resists distortion from extreme long sessions.")

for col in ['Energy_kWh', 'Charging_Duration_Mins']:
    medians = df.groupby('Charger_Type')[col].transform('median')
    before = df[col].isnull().sum()
    df[col] = df[col].fillna(medians)
    after = df[col].isnull().sum()
    print(f"  {col}: imputed {before} values → remaining missing = {after}")

# Final verification
print(f"\nMissing values after cleaning:\n{df.isnull().sum()}")
assert df.isnull().sum().sum() == 0, "Still have missing values!"
print("✓ Zero missing values remaining.")

# ============================================================
# 4. FEATURE ENGINEERING – DATETIME EXTRACTION (FR4)
# ============================================================
print("\n" + "=" * 70)
print("4. FEATURE ENGINEERING")
print("=" * 70)

df['Charging_Start_Time'] = pd.to_datetime(df['Charging_Start_Time'])
df['Hour'] = df['Charging_Start_Time'].dt.hour
df['Weekday'] = df['Charging_Start_Time'].dt.day_name()
df['Month'] = df['Charging_Start_Time'].dt.month_name()
df['Year'] = df['Charging_Start_Time'].dt.year

print("Derived columns added: Hour, Weekday, Month, Year")
print(f"Date range: {df['Charging_Start_Time'].min()} → {df['Charging_Start_Time'].max()}")
print(f"Years present: {sorted(df['Year'].unique())}")

# ============================================================
# 5. HEADLINE OPERATIONAL METRICS (FR5, FR6)
# ============================================================
print("\n" + "=" * 70)
print("5. HEADLINE OPERATIONAL METRICS")
print("=" * 70)

total_sessions = len(df)
total_energy = df['Energy_kWh'].sum()
avg_duration = df['Charging_Duration_Mins'].mean()
avg_energy = df['Energy_kWh'].mean()

print(f"Total charging sessions      : {total_sessions}")
print(f"Total energy delivered (kWh) : {total_energy:,.2f}")
print(f"Average charging duration    : {avg_duration:.2f} minutes")
print(f"Average energy per session   : {avg_energy:.2f} kWh")

# ============================================================
# 6. STATION RANKINGS (FR7)
# ============================================================
print("\n" + "=" * 70)
print("6. STATION RANKINGS")
print("=" * 70)

station_sessions = (df.groupby('Station_ID')
                      .agg(Sessions=('Session_ID', 'count'),
                           Total_Energy_kWh=('Energy_kWh', 'sum'),
                           Avg_Duration_Mins=('Charging_Duration_Mins', 'mean'))
                      .sort_values('Sessions', ascending=False))

print("\nTop 10 stations by number of sessions:")
print(station_sessions.head(10).round(2))

print("\nTop 10 stations by total energy delivered:")
print(station_sessions.sort_values('Total_Energy_kWh', ascending=False).head(10).round(2))

# ============================================================
# 7. CHARGER TYPE COMPARISON (FR8)
# ============================================================
print("\n" + "=" * 70)
print("7. AVERAGE CHARGING DURATION BY CHARGER TYPE")
print("=" * 70)

charger_stats = (df.groupby('Charger_Type')
                   .agg(Sessions=('Session_ID', 'count'),
                        Avg_Duration_Mins=('Charging_Duration_Mins', 'mean'),
                        Median_Duration_Mins=('Charging_Duration_Mins', 'median'),
                        Avg_Energy_kWh=('Energy_kWh', 'mean'),
                        Total_Energy_kWh=('Energy_kWh', 'sum'))
                   .round(2))
print(charger_stats)

# ============================================================
# 8. PEAK HOURS & BUSIEST DAYS (FR9)
# ============================================================
print("\n" + "=" * 70)
print("8. PEAK CHARGING HOURS AND BUSIEST DAYS")
print("=" * 70)

hour_counts = df['Hour'].value_counts().sort_index()
print("\nSessions by Hour of Day:")
print(hour_counts.to_string())
print(f"\nPeak hour(s): {hour_counts.idxmax()} (with {hour_counts.max()} sessions)")

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_counts = df['Weekday'].value_counts().reindex(weekday_order)
print("\nSessions by Weekday:")
print(weekday_counts.to_string())
print(f"\nBusiest day: {weekday_counts.idxmax()} (with {weekday_counts.max()} sessions)")

# ============================================================
# 9. ENERGY CONSUMPTION BY STATION LOCATION (FR10)
# ============================================================
print("\n" + "=" * 70)
print("9. ENERGY CONSUMPTION ACROSS STATION LOCATIONS")
print("=" * 70)

location_stats = (df.groupby('Station_Location')
                    .agg(Sessions=('Session_ID', 'count'),
                         Total_Energy_kWh=('Energy_kWh', 'sum'),
                         Avg_Energy_kWh=('Energy_kWh', 'mean'),
                         Avg_Duration_Mins=('Charging_Duration_Mins', 'mean'))
                    .sort_values('Total_Energy_kWh', ascending=False)
                    .round(2))
print(location_stats)

# ============================================================
# 10. CORE PYTHON DATA STRUCTURES (FR11, FR12)
# ============================================================
print("\n" + "=" * 70)
print("10. CORE PYTHON DATA STRUCTURES")
print("=" * 70)

# Tuple – fixed charger types
charger_types_tuple = tuple(sorted(df['Charger_Type'].unique()))
print(f"Charger types (tuple): {charger_types_tuple}")

# Set – unique station locations
station_locations_set = set(df['Station_Location'].unique())
print(f"Unique station locations (set): {station_locations_set}")

# Dictionary – station-wise session counts
station_session_dict = df['Station_ID'].value_counts().to_dict()
print(f"\nSample station session counts (first 5 from dict):")
for i, (k, v) in enumerate(station_session_dict.items()):
    if i >= 5:
        break
    print(f"  {k}: {v} sessions")

# Reusable function – average energy for a selected station
def avg_energy_for_station(dataframe, station_id):
    """
    Return the average energy (kWh) delivered per session for the given station.
    Returns None if the station is not found.
    """
    subset = dataframe[dataframe['Station_ID'] == station_id]
    if subset.empty:
        return None
    return round(subset['Energy_kWh'].mean(), 2)

# Demonstrate the function
sample_station = 'ST001'
print(f"\nAverage energy for {sample_station}: {avg_energy_for_station(df, sample_station)} kWh")
print(f"Average energy for ST029: {avg_energy_for_station(df, 'ST029')} kWh")

# ============================================================
# 11. NUMPY STATISTICS (FR13)
# ============================================================
print("\n" + "=" * 70)
print("11. NUMPY STATISTICS ON CHARGING DURATION")
print("=" * 70)

durations = df['Charging_Duration_Mins'].to_numpy()
mean_dur = np.mean(durations)
median_dur = np.median(durations)
p90_dur = np.percentile(durations, 90)

print(f"Mean duration   : {mean_dur:.2f} minutes")
print(f"Median duration : {median_dur:.2f} minutes")
print(f"90th percentile : {p90_dur:.2f} minutes")

# ============================================================
# 12. IQR OUTLIER DETECTION & DURATION GROUPS (FR14)
# ============================================================
print("\n" + "=" * 70)
print("12. IQR OUTLIER DETECTION & DURATION GROUPS")
print("=" * 70)

q1 = np.percentile(durations, 25)
q3 = np.percentile(durations, 75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

print(f"Q1 (25th percentile) : {q1:.2f}")
print(f"Q3 (75th percentile) : {q3:.2f}")
print(f"IQR                  : {iqr:.2f}")
print(f"Lower fence (Q1-1.5×IQR): {lower_fence:.2f}")
print(f"Upper fence (Q3+1.5×IQR): {upper_fence:.2f}")

outliers = df[(df['Charging_Duration_Mins'] < lower_fence) |
              (df['Charging_Duration_Mins'] > upper_fence)]
print(f"\nNumber of unusually long/short sessions (IQR method): {len(outliers)}")
if len(outliers) == 0:
    print("→ Zero outliers flagged. All sessions fall within the IQR fences.")
else:
    print(outliers[['Session_ID', 'Station_ID', 'Charging_Duration_Mins', 'Charger_Type']].head(10))

# Duration groups using documented thresholds
# Short  <= 120 mins
# Medium 121–240 mins
# Long   > 240 mins
df['Duration_Group'] = pd.cut(
    df['Charging_Duration_Mins'],
    bins=[-np.inf, 120, 240, np.inf],
    labels=['Short', 'Medium', 'Long']
)

print("\nDuration Group counts:")
print(df['Duration_Group'].value_counts().sort_index())

# ============================================================
# 13. CHARGINGSESSION CLASS (FR15 – OOP)
# ============================================================
print("\n" + "=" * 70)
print("13. CHARGINGSESSION CLASS DEMONSTRATION")
print("=" * 70)

class ChargingSession:
    """Simple class representing a single EV charging session."""

    def __init__(self, session_id, station_id, energy_kwh):
        self.session_id = session_id
        self.station_id = station_id
        self.energy_kwh = energy_kwh

    def __repr__(self):
        return (f"ChargingSession(session_id='{self.session_id}', "
                f"station_id='{self.station_id}', "
                f"energy_kwh={self.energy_kwh:.2f})")

    def is_high_energy(self, threshold=60.0):
        """Return True if energy delivered exceeds the given threshold."""
        return self.energy_kwh > threshold


# Demonstrate with a few real sessions
sample_rows = df.sample(3, random_state=42)
sessions = [
    ChargingSession(row['Session_ID'], row['Station_ID'], row['Energy_kWh'])
    for _, row in sample_rows.iterrows()
]

for s in sessions:
    print(s, "→ High energy?" , s.is_high_energy())

# ============================================================
# 14. EXPORT CLEANED DATASET
# ============================================================
print("\n" + "=" * 70)
print("14. EXPORTING CLEANED DATASET")
print("=" * 70)

# Final column order
final_cols = [
    'Session_ID', 'Station_ID', 'Station_Location', 'Charger_Type',
    'Charging_Start_Time', 'Energy_kWh', 'Charging_Duration_Mins',
    'Vehicle_Type', 'Hour', 'Weekday', 'Month', 'Year', 'Duration_Group'
]
df_clean = df[final_cols].copy()
df_clean.to_csv("26_ev_charging_sessions_clean.csv", index=False)
print(f"Cleaned dataset saved → 26_ev_charging_sessions_clean.csv")
print(f"Final shape: {df_clean.shape} (850 rows expected, 13 columns)")

# ============================================================
# 15. FIVE EVIDENCE-BASED RECOMMENDATIONS (FR15)
# ============================================================
print("\n" + "=" * 70)
print("15. FIVE OPERATIONAL RECOMMENDATIONS")
print("=" * 70)

# Gather supporting numbers for recommendations
top_station = station_sessions.index[0]
top_station_sessions = station_sessions.loc[top_station, 'Sessions']
peak_hour = hour_counts.idxmax()
busiest_day = weekday_counts.idxmax()
long_pct = (df['Duration_Group'] == 'Long').mean() * 100
loc_top = location_stats.index[0]
charger_longest = charger_stats['Avg_Duration_Mins'].idxmax()

print(f"""
RECOMMENDATION 1 – Prioritise capacity at high-demand stations
Evidence: Station {top_station} recorded the highest number of sessions
({int(top_station_sessions)}). Rankings by sessions and by total energy
both highlight a small set of stations that carry disproportionate load.
Action: Add extra chargers or faster chargers at the top-5 stations by
session count to reduce waiting times.

RECOMMENDATION 2 – Align staffing / maintenance with peak hours
Evidence: The busiest hour is {peak_hour}:00 with {hour_counts.max()} sessions.
The busiest weekday is {busiest_day} ({int(weekday_counts.max())} sessions).
Action: Schedule preventive maintenance and technician availability outside
these peak windows; consider dynamic pricing or reservation slots for the
peak hour to spread demand.

RECOMMENDATION 3 – Address long-duration occupancy (idle / over-stay)
Evidence: {long_pct:.1f}% of sessions fall into the “Long” group (>240 min).
Mean duration is {mean_dur:.0f} min while the 90th percentile reaches {p90_dur:.0f} min.
IQR analysis flagged {len(outliers)} statistical outliers.
Action: Introduce gentle over-stay fees or app notifications after charging
completes so that long-idle vehicles free the connector sooner.

RECOMMENDATION 4 – Location-specific infrastructure planning
Evidence: {loc_top} locations delivered the highest total energy
({location_stats.loc[loc_top, 'Total_Energy_kWh']:,.0f} kWh).
Different site types show distinct average energy and duration profiles.
Action: Install a higher proportion of DC Fast chargers at Highway and
Transit Hub sites (shorter expected dwell time) and Level-2 units at
Residential / Office District sites (longer dwell acceptable).

RECOMMENDATION 5 – Charger-type mix optimisation
Evidence: Average duration differs across charger types; {charger_longest}
shows the longest average plug-in time ({charger_stats.loc[charger_longest, 'Avg_Duration_Mins']:.0f} min).
Action: Where space allows, replace a subset of Level-1 connectors with
Level-2 or DC Fast units at high-turnover stations to increase daily
throughput and improve overall network availability.
""")

print("=" * 70)
print("ANALYSIS COMPLETE – All 15 functional requirements satisfied.")
print("=" * 70)
