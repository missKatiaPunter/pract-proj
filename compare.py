import pandas as pd
import json

# Load CSV and GeoJSON
csv_data = pd.read_csv('data/lads_data.csv')
with open('data/lad_geojson.json', 'r') as f:
    geojson_data = json.load(f)

# Extract LAD names from GeoJSON
geojson_lads = [feature['properties']['LAD13NM'] for feature in geojson_data['features']]

# Compare LAD names
csv_lads = set(csv_data['LAD'])
geojson_lads_set = set(geojson_lads)
mismatched = csv_lads - geojson_lads_set

print("Mismatched LADs:", mismatched)
print(f"Number of mismatches: {len(mismatched)}")
