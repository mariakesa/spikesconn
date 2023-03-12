import dash
from dash import dcc
from dash import html
import plotly.express as px
import numpy as np
from dash.exceptions import PreventUpdate
import pickle
import plotly.graph_objs as go

# Create sample data
image_matrix = np.load('image_matrix.npy')
psth_prototype_arr = np.load('psth_prototypes_arr.npy')
psth_arr = np.load('psth_arr.npy')
with open('bmu_dct.pickle', 'rb') as handle:
    bmu_dct = pickle.load(handle)

# Define app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='image',
            figure=px.imshow(image_matrix),
            style={'height':'50%','width': '50%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id='psth',
            style={'height':'50%','width': '50%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id='psth_individual',
            style={'height':'50%','width': '50%', 'display': 'inline-block'}
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

@app.callback(
    dash.dependencies.Output('psth_individual', 'figure'),
    [dash.dependencies.Input('image', 'hoverData')],
    [dash.dependencies.State('image', 'figure')]
)
def update_psth_individual(hoverData, figure):
    if hoverData is None:
        raise PreventUpdate
    i = hoverData['points'][0]['x']
    j = hoverData['points'][0]['y']
    d=psth_arr[bmu_dct[(i,j)],:]
    x=np.arange(-0.5,2.1,0.1)
    fig = go.Figure()

    for i in range(d.shape[0]):
        fig.add_trace(
            go.Scatter(
                x=x,
                y=d[i],
                mode='lines+markers',
                name=f'Data {i+1}'
            )
        )

    fig.update_layout(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        title='Plot of Data'
    )

    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)