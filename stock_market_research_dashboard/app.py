import os

import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd


EXTERNAL_STYLESHEETS = [
    "https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css"
]
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, use_pages=True)

server = app.server


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

df_sorted = df.sort_values(by=['country', 'year'])


def population_stats(group):
    max_pop = group['pop'].max()
    last_pop = group.iloc[-1]['pop']
    pop_diff = last_pop - max_pop
    pop_diff_percentage = (pop_diff / max_pop) * 100
    return pd.Series({'max_population': max_pop, 'last_population': last_pop,
                      'population_difference': pop_diff, 'population_difference_percentage': pop_diff_percentage})


population_stats_df = df_sorted.groupby('country').apply(population_stats).reset_index()

declining_population_df = population_stats_df[population_stats_df['population_difference'] < 0]

declining_population_df_sorted = declining_population_df.sort_values(by='population_difference_percentage')

population_of_country_difference_fig = px.bar(declining_population_df_sorted, x='country', y='population_difference_percentage')

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

graph_1 = html.Div(className="graph_1", children=[
    html.H1(children='Title of Dash App', style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

graph_2 = html.Div(
    className="graph_2", children=[
        html.H1(children="Population Difference by Country From Last Year to First Year", style={'textAlign': 'center'}),
        dcc.Graph(id="population_difference_graph", figure=population_of_country_difference_fig)
    ]
)

main_content = html.Div(className="main_content", children=[
    graph_1,
    graph_2
])


app.layout = html.Div(className="container", children=[
    sidebar,
    main_content,
    dash.page_container,
    html.Script(src="./assets/sidebar_script.js")
])


@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')


# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
