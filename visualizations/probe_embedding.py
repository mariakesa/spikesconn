import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import base64

# Load the CSV data
data = pd.read_csv("probe_insertion_embeddings_index.csv")

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([

    # Add the scatter plot
    dcc.Graph(id="scatter-plot", figure={
        "data": [{
            "x": data["x"],
            "y": data["y"],
            "mode": "markers",
            "customdata": data["index"],
            "hovertemplate": "<b>Index:</b> %{customdata}<br>"
        }],
        "layout": {
            "xaxis": {"title": "X Axis"},
            "yaxis": {"title": "Y Axis"},
            "title": "My Scatter Plot"
        }
    }, style={"width": "50%", "display": "inline-block", "color": "cyan"}),

    # Add the image plot
    dcc.Graph(id="image-plot",
              style={"width": "50%", "display": "inline-block"}),

    # Store the image data
    html.Div(id="image-data", style={"display": "none"})

])

# Define the callback to update the image


@app.callback(
    Output("image-plot", "figure"),
    Input("scatter-plot", "hoverData"),
    State("image-data", "children")
)
def update_image(hover_data, image_data):
    if hover_data is not None:
        index = hover_data["points"][0]["customdata"]
        image_path = f"static/mlapdv_plot_{index}.png"
        if image_data is not None and image_data.startswith("data:image/png;base64,"):
            image_src = image_data
        else:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            image_src = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
        return {
            "data": [{
                "x": [0],
                "y": [0],
                "mode": "markers",
                "marker": {
                    "size": 1,
                    "color": "rgba(0, 0, 0, 0)"
                },
                "hoverinfo": "none",
                "showlegend": False
            }],
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "images": [{
                    "x": 0,
                    "y": 1,
                    "sizex": 1,
                    "sizey": 1,
                    "xref": "paper",
                    "yref": "paper",
                    "layer": "above",
                    "source": image_src
                }]
            }
        }
    else:
        return {
            "data": [],
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "images": []
            }
        }


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
