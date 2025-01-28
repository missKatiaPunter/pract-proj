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
    1: '#bd1534',  # Red
    2: '#fc9d03',  # Orange
    3: '#e3fc03',  # Yellow
    4: '#135701'   # Green
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

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=dict(
            text="Fake Data for UK LADs",
            x=0.5,  # Center the title
            font=dict(size=20)  # Increase title font size
        ),
        margin=dict(l=20, r=200, t=80, b=0),  # Changed t=0 ➔ t=80
        legend=dict(x=1.05, y=0.5),
        height=800
    )

    return render_template('index.html', choropleth_map=fig.to_html(full_html=False))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(debug=True, host='0.0.0.0', port=port)
