# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50],
    'category': ['A', 'B', 'A', 'B', 'A']
})

# Create a Plotly Express scatter plot
fig = px.scatter(df, x='x', y='y', color='category')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Simple Scatter Plot"),
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    ),
    html.Label("Select X-axis:"),
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns if col != 'y'],
        value='x'
    ),
    html.Label("Select Y-axis:"),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns if col != 'x'],
        value='y'
    )
])

# Define the callback to update the graph
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('x-axis-dropdown', 'value'),
    Input('y-axis-dropdown', 'value')
)
def update_graph(x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis, color='category')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)
