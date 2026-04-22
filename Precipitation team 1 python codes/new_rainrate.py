import pandas as pd
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# Make sure the CSV file is in the same folder as your Python script, 
# or update this path to point to your file's location.
file_path = 'rain_rate.csv'

# Set your specific outlier threshold value here (in millimeters)
OUTLIER_THRESHOLD = 5.0
# ---------------------

def main():
    # 1. Load the data
    try:
        print(f"Loading data from {file_path}...")
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find '{file_path}'. Please check the file name and path.")
        return

    # 2. Clean and prepare the data
    # Ensure the rain_rate_mm column exists
    if 'rain_rate_mm' not in df.columns:
        print("Error: The column 'rain_rate_mm' was not found in the CSV.")
        return

    # Convert to numeric, forcing any text/errors to NaN, then drop the NaNs
    df['rain_rate_mm'] = pd.to_numeric(df['rain_rate_mm'], errors='coerce')
    df = df.dropna(subset=['rain_rate_mm'])

    # Use 'Last Report Time' for the X-axis if available, otherwise use row index
    if 'Last Report Time' in df.columns:
        df['Last Report Time'] = pd.to_datetime(df['Last Report Time'], errors='coerce')
        x_data = df['Last Report Time']
        x_label = 'Report Time'
    else:
        x_data = df.index
        x_label = 'Data Point Index'

    # 3. Identify outliers based on your threshold
    normal_data = df[df['rain_rate_mm'] <= OUTLIER_THRESHOLD]
    outliers = df[df['rain_rate_mm'] > OUTLIER_THRESHOLD]
    
    print(f"Found {len(outliers)} outliers (Rain rate > {OUTLIER_THRESHOLD} mm).")

    # 4. Create the plot
    plt.figure(figsize=(12, 6))

    # Plot normal data points (Blue)
    plt.scatter(x_data[normal_data.index], normal_data['rain_rate_mm'], 
                color='#1f77b4', label='Normal Rain Rate', alpha=0.6, s=30)

    # Plot outlier data points (Red)
    plt.scatter(x_data[outliers.index], outliers['rain_rate_mm'], 
                color='red', label=f'Outliers (> {OUTLIER_THRESHOLD} mm)', edgecolors='black', s=60, zorder=5)

    # 5. Customize the graph formatting
    plt.title(f'Rain Rate Analysis (Outlier Threshold = {OUTLIER_THRESHOLD} mm)', fontsize=14, pad=15)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel('Rain Rate (mm)', fontsize=12)
    
    # Add a visual horizontal line for the threshold
    plt.axhline(y=OUTLIER_THRESHOLD, color='red', linestyle='--', alpha=0.5, label='Threshold Line')
    
    # Format axes and legend
    plt.legend(loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout() # Ensures labels aren't cut off

    # 6. Show the graph
    plt.show()

if __name__ == "__main__":
    main()