import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Sample DataFrame
data = {
    'x': [1, 2, 3, 4, 5],
    'y': [10, 11, 12, 13, 14]
}
df = pd.DataFrame(data)

# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Expose the Flask instance (required for Gunicorn)
# This is super important and app.server is what you call in the docker
server = app.server

# Define the layout for the app
app.layout = html.Div([
    html.H1("Sample Dash App"),
    dcc.Graph(
        id='example-graph',
        figure=px.scatter(df, x='x', y='y', title="Sample Scatter Plot")
    )
])

# Run the app (only used when running directly, not with Gunicorn)
#if __name__ == '__main__':
#    app.run_server(debug=True)

# Run the app with Gunicorn
# You need this for GCR
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host='0.0.0.0', port=port)
