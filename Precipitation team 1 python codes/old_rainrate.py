import pandas as pd
import zipfile
import matplotlib.pyplot as plt

# ==========================================================
# CONFIGURATION
# ==========================================================
zip_path = "Precipitation.zip"   # Make sure this file is in same folder
rain_col = "Rain"
rain_rate_col = "Rain Rate"
time_col = "Timestamp"

# ==========================================================
# LOAD CSV FILES FROM ZIP
# ==========================================================
dataframes = []

with zipfile.ZipFile(zip_path, "r") as z:
    for file in z.namelist():
        if file.endswith(".csv"):
            with z.open(file) as f:
                temp_df = pd.read_csv(f)
                if not temp_df.empty:
                    temp_df["Source_File"] = file
                    dataframes.append(temp_df)

if not dataframes:
    raise ValueError("No valid CSV files found inside the ZIP.")

df = pd.concat(dataframes, ignore_index=True)

# ==========================================================
# CLEAN DATA
# ==========================================================
df[time_col] = pd.to_datetime(df[time_col], errors="coerce")
df = df.dropna(subset=[rain_rate_col, time_col])

# Ensure numeric
df[rain_rate_col] = pd.to_numeric(df[rain_rate_col], errors="coerce")
df = df.dropna(subset=[rain_rate_col])

# ==========================================================
# CALCULATE OUTLIER THRESHOLD (99th Percentile)
# ==========================================================
threshold = df[rain_rate_col].quantile(0.99)

print("=====================================")
print("Rain Rate Summary Statistics")
print(df[rain_rate_col].describe())
print("=====================================")
print(f"99th Percentile Threshold: {threshold:.3f} mm/hr")

# ==========================================================
# SPLIT DATA
# ==========================================================
regular = df[df[rain_rate_col] < threshold]
outliers = df[df[rain_rate_col] >= threshold]

print(f"Total Records: {len(df)}")
print(f"Outlier Records (Top 1%): {len(outliers)}")

# Save outliers
outliers.to_csv("rain_rate_outliers.csv", index=False)

# ==========================================================
# VISUALIZATION
# ==========================================================
plt.figure(figsize=(12, 6))

plt.scatter(
    regular[time_col],
    regular[rain_rate_col],
    alpha=0.35,
    label="Regular Data"
)

plt.scatter(
    outliers[time_col],
    outliers[rain_rate_col],
    alpha=0.9,
    label="Top 1% Rain Rate (Outliers)"
)

plt.axhline(
    threshold,
    linestyle="--",
    label=f"99th Percentile Threshold ({threshold:.2f} mm/hr)"
)

plt.title("Rain Rate Outliers (Top 1%) vs Regular Data")
plt.xlabel("Time")
plt.ylabel("Rain Rate (mm/hr)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Save figure
plt.savefig("rain_rate_outliers_plot.png", dpi=300)

plt.show()

print("Graph saved as: rain_rate_outliers_plot.png")
print("Outliers saved as: rain_rate_outliers.csv")

