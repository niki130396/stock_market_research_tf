# Import necessary libraries
import os

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from sqlalchemy.orm import (
    DeclarativeBase,
    mapped_column,
    relationship,
    Mapped,
    Session,
)

from utils.models import CompanyMetaData
from utils.sql_helpers import connect_to_cloud_sql

with Session(connect_to_cloud_sql()) as session:
    companies = session.query(
        CompanyMetaData.symbol,
        CompanyMetaData.name,
        CompanyMetaData.sector,
        CompanyMetaData.industry,
        CompanyMetaData.market_cap,
        CompanyMetaData.full_time_employees_count,
    ).all()


companies_df = pd.DataFrame(companies, columns=[
    "symbol",
    "name",
    "sector",
    "industry",
    "market_cap",
    "full_time_employees_count"
])

# Sample DataFrame
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50],
    'category': ['A', 'B', 'A', 'B', 'A']
})

top_10_companies_by_market_cap = companies_df.sort_values(by="market_cap", ascending=False)[:10][["name", "market_cap"]]
# Create a Plotly Express scatter plot
companies_by_market_cap_fig = px.bar(top_10_companies_by_market_cap, x='name', y='market_cap')

EXTERNAL_STYLESHEETS = [
    "https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
]
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

server = app.server

sidebar = html.Nav(className="sidebar", children=[
    html.Div(className="menu_content", children=[
        html.Ul(className="menu_items", children=[
            html.Div(className="menu_title menu_dashboard"),
            html.Li(className="item", children=[
                html.Div(className="nav_link submenu_item", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-home-alt")
                    ]),
                    html.Span("Home", className="navlink"),
                    html.I(className="bx bx-chevron-right arrow-left")
                ]),
                html.Ul(className="menu_items submenu", children=[
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink")
                ])
            ]),
            html.Li(className="item", children=[
                html.Div(className="nav_link submenu_item", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-grid-alt")
                    ]),
                    html.Span("Overview", className="navlink"),
                    html.I(className="bx bx-chevron-right arrow-left")
                ]),
                html.Ul(className="menu_items submenu", children=[
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink"),
                    html.A("Nav Sub Link", href="#", className="nav_link sublink")
                ])
            ])
        ]),
        html.Ul(className="menu_items", children=[
            html.Div(className="menu_title menu_editor"),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bxs-magic-wand")
                    ]),
                    html.Span("Magic build", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-loader-circle")
                    ]),
                    html.Span("Filters", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-filter")
                    ]),
                    html.Span("Filter", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-cloud-upload")
                    ]),
                    html.Span("Upload new", className="navlink")
                ])
            ])
        ]),
        html.Ul(className="menu_items", children=[
            html.Div(className="menu_title menu_setting"),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-flag")
                    ]),
                    html.Span("Notice board", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-medal")
                    ]),
                    html.Span("Award", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-cog")
                    ]),
                    html.Span("Setting", className="navlink")
                ])
            ]),
            html.Li(className="item", children=[
                html.A(href="#", className="nav_link", children=[
                    html.Span(className="navlink_icon", children=[
                        html.I(className="bx bx-layer")
                    ]),
                    html.Span("Features", className="navlink")
                ])
            ])
        ]),
        html.Div(className="bottom_content", children=[
            html.Div(className="bottom expand_sidebar", children=[
                html.Span(" Expand"),
                html.I(className='bx bx-log-in')
            ]),
            html.Div(className="bottom collapse_sidebar", children=[
                html.Span(" Collapse"),
                html.I(className='bx bx-log-out')
            ])
        ])
    ])
])


main_content = html.Div(className="main_content", children=[
    html.H1("Top 10 Companies by Market Cap"),
    dcc.Graph(
        id='scatter-plot',
        figure=companies_by_market_cap_fig
    ),
    # html.Label("Select X-axis:"),
    # dcc.Dropdown(
    #     id='x-axis-dropdown',
    #     options=[{'label': col, 'value': col} for col in df.columns if col != 'y'],
    #     value='x'
    # ),
    # html.Label("Select Y-axis:"),
    # dcc.Dropdown(
    #     id='y-axis-dropdown',
    #     options=[{'label': col, 'value': col} for col in df.columns if col != 'x'],
    #     value='y'
    # )
])

app.layout = html.Div(className="container", children=[
    sidebar,
    main_content,
    html.Script(src="./assets/sidebar_script.js")
])


# @app.callback(
#     Output('scatter-plot', 'figure'),
#     Input('x-axis-dropdown', 'value'),
#     Input('y-axis-dropdown', 'value')
# )
# def update_graph(x_axis, y_axis):
#     fig = px.scatter(df, x=x_axis, y=y_axis, color='category')
#     return fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
