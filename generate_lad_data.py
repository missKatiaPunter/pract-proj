import requests
import json
import pandas as pd
import random

# Step 1: Fetch the GeoJSON data
def fetch_geojson():
    geojson_url = "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/json/administrative/gb/lad.json"
    response = requests.get(geojson_url)
    response.raise_for_status()  # Ensure the request was successful
    geojson_data = response.json()
    return geojson_data

# Step 2: Extract LAD names
def extract_lad_names(geojson_data):
    return [feature['properties']['LAD13NM'] for feature in geojson_data['features']]

# Step 3: Generate fake data with only LAD and fake_data (values 1, 2, 3, 4)
def generate_fake_data(lad_names):
    lad_data = {
        "LAD": lad_names,
        "fake_data": [random.choice([1, 2, 3, 4]) for _ in lad_names],  # Random discrete values
    }
    return pd.DataFrame(lad_data)

# Step 4: Save data to files
def save_files(geojson_data, lad_df):
    # Save GeoJSON file
    with open('data/lad_geojson.json', 'w') as geojson_file:
        json.dump(geojson_data, geojson_file)
    print("GeoJSON saved to data/lad_geojson.json")

    # Save CSV file
    lad_df.to_csv('data/lads_data.csv', index=False)
    print("Fake data saved to data/lads_data.csv")

# Main script execution
if __name__ == '__main__':
    print("Fetching GeoJSON data...")
    geojson_data = fetch_geojson()

    print("Extracting LAD names...")
    lad_names = extract_lad_names(geojson_data)
    print(f"Extracted {len(lad_names)} LADs")

    print("Generating fake data...")
    lad_df = generate_fake_data(lad_names)

    print("Saving data files...")
    save_files(geojson_data, lad_df)

    print("Done!")