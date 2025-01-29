import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
import json
import os

app = Flask(__name__)

# Load data
data = pd.read_csv('data/lads_data.csv')
geojson_file = 'data/lad_geojson.json'

# Discrete color mapping
COLOR_MAP = {
    1: '#440154',  # Deep Purple  
    2: '#31688e',  # Steel Blue  
    3: '#35b779',  # Medium Sea Green  
    4: '#fde725',  # Bright Yellow  
}

@app.route('/')
def index():
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)

    # Create discrete color scale
    discrete_colorscale = [
        [0.0, COLOR_MAP[1]],
        [0.249, COLOR_MAP[1]],
        [0.25, COLOR_MAP[2]],
        [0.499, COLOR_MAP[2]],
        [0.5, COLOR_MAP[3]],
        [0.749, COLOR_MAP[3]],
        [0.75, COLOR_MAP[4]],
        [1.0, COLOR_MAP[4]]
    ]

    fig = go.Figure(go.Choropleth(
        geojson=geojson_data,
        locations=data['LAD'],
        featureidkey="properties.LAD13NM",
        z=data['fake_data'],
        colorscale=discrete_colorscale,
        zmin=0.5,  # Set to 0.5 below minimum value
        zmax=4.5,  # Set to 0.5 above maximum value
        marker_line_width=0.1,
        colorbar=dict(
            title='Fake Data Value',
            thickness=20,
            tickvals=[1.5, 2.5, 3.5, 4.5],  # Midpoints of ranges
            ticktext=['1', '2', '3', '4'],
            lenmode='fraction',
            len=0.75
        )
    ))

    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(
        title=dict(
            text="Fake Data for UK LADs",
            x=0.5,
            y=0.95,
            font=dict(size=20),
            pad=dict(t=50, b=20)
        ),
        margin=dict(l=10, r=200, t=30, b=10),  # 🔥 Keeps spacing balanced
        height=900,  # 🔥 Ensures proper size on desktop
        geo=dict(
            projection=dict(type="equirectangular"),  # 🔥 Prevents stretching
            domain=dict(x=[0, 1], y=[0, 1]),  # 🔥 Ensures full use of space
            center={"lat": 55.5, "lon": -3},  # 🔥 Moves UK slightly up
        )
    )
    fig.update_geos(
        visible=False,
        projection=dict(type="equirectangular", scale=3),
        center={"lat": 52, "lon": -3}, 
        fitbounds="locations"
    )


    return render_template('index.html', choropleth_map=fig.to_html(full_html=False))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5003))  # Use Render's assigned port
    app.run(debug=True, host='0.0.0.0', port=port)
