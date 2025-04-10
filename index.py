import pandas as pd
import matplotlib.pyplot as plt
import os

# Load CSV
file1 = pd.read_csv("vius_2021_puf_csv/vius_2021_puf.csv")

# Merge body types
btypes_df = pd.DataFrame({
    "Code": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "X"],
    "Description": ["Pickup", "Minvan", "Other light van", "Sport utility vehicle", "Armored", "Beverage or bay", "Box truck",
        "Concrete mixer", "Concrete pumper", "Conveyor bed", "Crane", "Dump", "Flatbed, stake, or platform",
        "Hooklift/roll-off", "Logging", "Service, utility", "Service, other", "Street sweeper", "Tank, liquid or gases",
        "Tow/wrecker", "Trash, garbage, or recycling", "Vacuum", "Van, walk-in", "Van, other", "Wood chipper",
        "Other", "Not reported", "Not applicable (see 'Applicable Vehicles')"]
})
file1 = pd.merge(file1, btypes_df, left_on='BTYPE', right_on='Code', how='left')

# Map categorical variables
file1['CI_AUTOEBRAKE'] = file1['CI_AUTOEBRAKE'].map({0: 'Not Reported', 1: 'YES', 2: 'NO'})
file1['TRANSMISSION'] = file1['TRANSMISSION'].astype(str).map({
    '1': 'Automatic', '2': 'Manual', '3': 'Both', '4': 'Other transmission type', '5': 'Not reported'})
file1['VEHTYPE'] = file1['VEHTYPE'].astype(str).map({'SU': 'Single unit vehicle', 'TT': 'Truck tractor'})

file1['AVGWEIGHT'] = file1['AVGWEIGHT'].astype(str).map({
    '01': 'Less than 6,000 pounds', '02': '6,001 to 8,500 pounds', '03': '8,501 to 10,000 pounds',
    '04': '10,001 to 14,000 pounds', '05': '14,001 to 16,000 pounds', '06': '16,001 to 19,500 pounds',
    '07': '19,501 to 26,000 pounds', '08': '26,001 to 33,000 pounds', '09': '33,001 to 40,000 pounds',
    '10': '40,001 to 50,000 pounds', '11': '50,001 to 60,000 pounds', '12': '60,001 to 80,000 pounds',
    '13': '80,001 to 100,000 pounds', '14': '100,001 to 130,000 pounds', '15': '130,001 pounds or more',
    'X': 'Not applicable (see Applicable Vehicles)'
})
file1['FUELTYPE'] = file1['FUELTYPE'].map({
    '10': 'Gasoline', '20': 'Diesel', '31': 'Compressed natural gas', '32': 'Liquified natural gas',
    '33': 'Propane', '34': 'Alcohol fuels', '35': 'Electricity', '36': 'Combination', '40': 'Not reported'
})
file1['CYLINDERS'] = file1['CYLINDERS'].map({
    '4': '4 cylinders', '6': '6 cylinders', '8': '8 cylinders', 'Oth': 'All others'
})
file1['KINDOFBUS'] = file1['KINDOFBUS'].astype(str).map({
    '1': 'Accommodation and food services (for immediate consumption)', '2': 'Waste management and remediation',
    '3': 'Landscaping', '4': 'Other administrative and support and waste management and remediation services',
    '5': 'Agriculture (crop and animal production)', '6': 'Fishing, hunting, trapping', '7': 'Forestry and logging',
    '8': 'Other agriculture, forestry, fishing, and hunting', '9': 'Arts, entertainment, or recreation services',
    '10': 'Construction - residential', '11': 'Construction - non-residential', '12': 'Other construction',
    '13': 'Fuel wholesale or distribution', '14': 'Information services (includes telephone and television)',
    '15': 'Manufacturing', '16': 'Mining (includes quarrying, well operations, and beneficiating)', '17': 'Retail trade',
    '18': 'For-hire transportation (of goods or people)', '19': 'Warehousing and storage',
    '20': 'Other transportation and warehousing', '21': 'Utilities', '22': 'Vehicle leasing or rental',
    '23': 'Wholesale trade', '24': 'Other services', '25': 'Other business type', '26': 'Not reported', 'X': 'Not applicable'
})
file1['TTYPE'] = file1['TTYPE'].astype(str).map({
    '01': 'Automobile carrier (stinger-steered)',
    '02': 'Automobile carrier (conventional - rack above cab)',
    '03': 'Automobile carrier (high mount - no rack above cab)',
    '04': 'Beverage or bay',
    '05': 'Container',
    '06': 'Curtainside',
    '07': 'Dump',
    '08': 'Flatbed, platform',
    '09': 'Intermodal chassis',
    '10': 'Livestock',
    '11': 'Logging',
    '12': 'Low boy',
    '13': 'Mobile home toter',
    '14': 'Open top',
    '15': 'Tank, dry bulk',
    '16': 'Tank, liquids or gases',
    '17': 'Van, basic enclosed',
    '18': 'Van, drop frame',
    '19': 'Van, insulated nonrefrigerated',
    '20': 'Van, insulated refrigerated',
    '21': 'Other',
    '22': 'Not reported',
    'X': 'Not applicable (see \'Applicable Vehicles\')'
})

# Filter
file1 = file1[file1['REGSTATE'] == 'MD']
print("Unique raw TTYPE values:", file1['VEHTYPE'].unique())
print("Unique raw TTYPE values:",file1['VEHTYPE'].value_counts())
# Get top 10 TTYPEs including all
top_ttypes = file1['TTYPE'].value_counts().head(10)

# Drop the ones you don't want to plot
top_ttypes = top_ttypes[~top_ttypes.index.isin([
    "Not applicable (see 'Applicable Vehicles')",
    'Not reported',
    'Other'
])]

print("Unique VEHTYPE values before mapping:", file1['VEHTYPE'].unique())




# Create output directory
output_dir = "vius_2021_puf_csv/md_vehicle_charts"
os.makedirs(output_dir, exist_ok=True)

# Utility: Generate a color list
def get_colors(n):
    from matplotlib import cm
    colors = cm.get_cmap('tab20', n)
    return [colors(i) for i in range(n)]

print("Unique VEHTYPE values before mapping:", file1['VEHTYPE'].unique())
# 3. CHART 7: Pie chart (Vehicle Type Distribution)
vehicle_type_counts = file1['VEHTYPE'].dropna().value_counts()
fig, ax = plt.subplots()
vehicle_type_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140)
ax.set_title('Vehicle Type Distribution in Maryland')
ax.set_ylabel('')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "7_vehicle_type.png"))



file1 = file1[~file1['Description'].isin(['Not applicable (see \'Applicable Vehicles\')', 'Not reported'])]


# Chart 1
data = file1['Description'].value_counts()
fig, ax = plt.subplots()
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Vehicle Body Types Distribution in Maryland')
ax.set_xlabel('Vehicle Body Type')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "1_body_types.png"))

# Chart 2
fig, ax = plt.subplots()
file1['CI_AUTOEBRAKE'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=140)
ax.set_title('Automatic Emergency Braking Usage in Maryland')
ax.set_ylabel('')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "2_autobrake.png"))

# Chart 3
data = file1['FUELTYPE'].value_counts()
fig, ax = plt.subplots()
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Fuel Type Distribution in Maryland')
ax.set_xlabel('Fuel Type')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "3_fuel_type.png"))

# Chart 4
data = file1['CYLINDERS'].value_counts()
fig, ax = plt.subplots()
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Cylinder Count in Maryland Vehicles')
ax.set_xlabel('Cylinders')
ax.set_ylabel('Count')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "4_cylinders.png"))

# Chart 5
data = file1['KINDOFBUS'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(12, 8))
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Top 10 Bus Types Using Vehicles in Maryland')
ax.set_xlabel('Business Type')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "5_business_types.png"))

# Chart 6
data = file1['TRANSMISSION'].value_counts()
fig, ax = plt.subplots()
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Transmission Type Distribution in Maryland Vehicles')
ax.set_xlabel('Transmission Type')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "6_transmission.png"))


# Chart 8: Trailer Type (Filtered and Colored)
ttype_filtered = file1[~file1['TTYPE'].isin(['Not applicable', 'Not reported', 'Other'])]
data = ttype_filtered['TTYPE'].value_counts()

if not data.empty:
    fig, ax = plt.subplots()
    top_ttypes.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Trailer Body Types in Maryland')
    ax.set_xlabel('Trailer Type')
    ax.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "8_trailer_type.png"))

else:
    print("No valid trailer body types to plot.")



# Chart 9
data = file1['AVGWEIGHT'].value_counts().sort_index()
fig, ax = plt.subplots()
data.plot(kind='bar', ax=ax, color=get_colors(len(data)))
ax.set_title('Average Vehicle Weight Categories in Maryland')
ax.set_xlabel('Weight Category')
ax.set_ylabel('Count')
plt.xticks(rotation=45, ha='right')
fig.tight_layout()
fig.savefig(os.path.join(output_dir, "9_weight.png")


)

# Filter out non-numeric MPG values
file1_clean = file1[~file1['MPG'].isin(['.', '.X'])].copy()
file1_clean['MPG'] = pd.to_numeric(file1_clean['MPG'], errors='coerce')

# Drop any remaining NaNs
file1_clean = file1_clean.dropna(subset=['MPG'])

# Plot histogram
plt.figure(figsize=(10, 6))
plt.hist(file1_clean['MPG'], bins=30, color='skyblue', edgecolor='black')
plt.title('Distribution of MPG (Miles Per Gallon)')
plt.xlabel('Miles Per Gallon')
plt.ylabel('Number of Vehicles')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "10_weight.png"))

avg_mpg_by_btype = file1_clean.groupby('Description')['MPG'].mean().sort_values()
avg_mpg_by_btype.plot(kind='barh', figsize=(10, 6), color='lightgreen', edgecolor='black')
plt.title('Average MPG by Vehicle Body Type')
plt.xlabel('Average MPG')
plt.ylabel('Body Type')
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "11_weight.png"))

# Convert '.' and '.X' to NaN, then cast to numeric
file1['DEADHEADPCT'] = pd.to_numeric(file1['DEADHEADPCT'], errors='coerce')
file1['LOADEDPCT'] = pd.to_numeric(file1['LOADEDPCT'], errors='coerce')







html_content = """
<html>
<head>
    <title>Maryland Vehicle Data Charts</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 {
            text-align: center;
        }
        .chart-container {
            background: #fff;
            padding: 20px;
            margin: 20px auto;
            width: 90%;
            max-width: 900px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }
        img {
            width: 100%;
            height: auto;
            border-radius: 6px;
        }
    </style>
</head>
<body>
    <h1>Maryland Vehicle Data Charts</h1>

    <div class="chart-container"><h2>1. Vehicle Body Types Distribution in Maryland</h2><img src="1_body_types.png"/></div>
    <div class="chart-container"><h2>2. Automatic Emergency Braking Usage in Maryland</h2><img src="2_autobrake.png"/></div>
    <div class="chart-container"><h2>3. Fuel Type Distribution in Maryland</h2><img src="3_fuel_type.png"/></div>
    <div class="chart-container"><h2>4. Cylinder Count in Maryland Vehicles</h2><img src="4_cylinders.png"/></div>
    <div class="chart-container"><h2>5. Top 10 Bus Type Distribution in Maryland</h2><img src="5_business_types.png"/></div>
    <div class="chart-container"><h2>6. Transmission Type Distribution in Maryland Vehicles</h2><img src="6_transmission.png"/></div>
    <div class="chart-container"><h2>7. Vehicle Type Distribution in Maryland</h2><img src="7_vehicle_type.png"/></div>
    <div class="chart-container"><h2>8. Top 10 Trailer Body Types in Maryland</h2><img src="8_trailer_type.png"/></div>
    <div class="chart-container"><h2>9. Average Vehicle Weight Categories in Maryland</h2><img src="9_weight.png"/></div>
    <div class="chart-container"><h2>10. Distribution of MPG (Miles Per Gallon) in Maryland</h2><img src="10_weight.png"/></div>
    <div class="chart-container"><h2>11. Average MPG by Vehicle Body Type in Maryland</h2><img src="11_weight.png"/></div>

</body>
</html>
"""


# Save HTML
html_path = os.path.join(output_dir, "maryland_vehicle_analysis.html")
with open(html_path, "w") as f:
    f.write(html_content)
    