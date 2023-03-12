import dash
from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
from dash.exceptions import PreventUpdate

# Create sample data
image_matrix = np.load('image_matrix.npy')
psth_prototype_arr = np.load('psth_prototypes_arr.npy')

# Define app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='image',
            figure=px.imshow(image_matrix),
            style={'width': '50%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id='psth',
            style={'width': '50%', 'display': 'inline-block'}
        ),
    ]),
])

@app.callback(
    dash.dependencies.Output('psth', 'figure'),
    [dash.dependencies.Input('image', 'hoverData')],
    [dash.dependencies.State('image', 'figure')]
)
def update_psth(hoverData, figure):
    if hoverData is None:
        raise PreventUpdate
    i = hoverData['points'][0]['x']
    j = hoverData['points'][0]['y']
    data = [dict(x=list(np.arange(-0.5,2.2,0.1)), y=psth_prototype_arr[i,j,:])]
    layout = figure['layout']['yaxis']
    layout['title'] = 'PSTH'
    layout['xaxis'] = dict(title='Time (ms)')
    return {'data': data, 'layout': layout}

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)