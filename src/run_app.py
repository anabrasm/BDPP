import pandas as pd
import pycountry
import dash
import os
from dash.dependencies import Input, Output
import plotly.express as px
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import sys
from app_layout import init_layout


def load_data():
    """Loads the feather data and returns a dataframe."""
    dirname = sys.path[0]
    df = pd.read_feather(os.path.join(dirname, "../output/df_processed"))
    return df


df = load_data()


# Custom color scale
color_scale_renewables = [
    (0.0, "rgb(211,211,211)"),  # Light grey for 0
    (0.00001, "rgb(229,245,224)"),  # Start shades of green for any value higher than 0
    (0.1, "rgb(199,233,192)"),
    (0.2, "rgb(161,217,155)"),
    (0.3, "rgb(116,196,118)"),
    (0.4, "rgb(65,171,93)"),
    (0.5, "rgb(35,139,69)"),
    (0.6, "rgb(0,109,44)"),
    (0.7, "rgb(0,68,27)"),
    (0.8, "rgb(0,68,27)"),
    (0.9, "rgb(0,68,27)"),
    (1.0, "rgb(0,68,27)"),  # Dark green for all values above 150
]

color_scale_ff = [
    (0.0, "rgb(211,211,211)"),  # Light grey for 0
    (0.00001, "rgb(246,232,195)"),  # Very light beige
    (0.1, "rgb(223,194,125)"),
    (0.2, "rgb(191,129,45)"),
    (0.3, "rgb(141,109,49)"),
    (0.4, "rgb(140,81,10)"),
    (0.5, "rgb(129,89,23)"),
    (0.6, "rgb(103,65,15)"),
    (0.7, "rgb(80,50,20)"),
    (0.8, "rgb(60,38,22)"),
    (0.9, "rgb(40,25,15)"),
    (1.0, "rgb(20,10,5)"),  # Dark brown for all values above 150
]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = init_layout(df)

# Defining energy types and their respective color scales

def get_color_scale(energy_type):
    if energy_type == "ff":
        return color_scale_ff
    elif energy_type == "renewables":
        return color_scale_renewables
    elif energy_type == "share_ff":
        return color_scale_ff
    elif energy_type == "share_renewables":
        return color_scale_renewables
    else:
        return px.colors.sequential.Plasma

def get_energy_label(energy_type):
    return "% of Energy Patents" if energy_type in ["share_ff", "share_renewables"] else "# of Patents"

def get_country_trend_fig(dff, energy_type, energy_label):
    if energy_type in ['ff', 'share_ff']:
        line_color = '#D68200'
    else:
        line_color = '#94CFAB'
    
    fig = go.Figure().update_layout(
        font=dict(
            family="Montserrat, sans-serif",
            size=12,
            color="#7f7f7f"
        ),
        margin=dict(t=10, l=50, r=50, b=50),
        yaxis_title="# of Patents" if energy_type in ['ff', 'renewables'] else "% of Energy Patents",
        xaxis_title="Year",
        plot_bgcolor = '#FFFFFF',
        xaxis = dict(
            gridcolor = '#EAE8E8',
        ),
        yaxis = dict(
            gridcolor = '#EAE8E8',
        )
    )
    fig.add_trace(go.Scatter(x=dff["Year"], y=dff[energy_type], mode='lines+markers', name=energy_label, line = dict(color=line_color)))
    
    return fig

# Callbacks

@app.callback(
    Output("dummy-button", "n_clicks"),
    Input("world-map", "clickData"),
)
def update_dummy_button(clickData):
    return 1 if clickData else 0

@app.callback(
    Output("world-map", "figure"),
    [Input("type-selection", "value"), Input("year-slider", "value")],
)
def update_world_map(energy_type, selected_year):
    dff = df[df["Year"] == selected_year]
    color_scale = get_color_scale(energy_type)
    label = get_energy_label(energy_type)

    fig = px.choropleth(
        dff,
        locations="Country",
        color=energy_type,
        hover_name="Country_Name",
        projection="natural earth",
        color_continuous_scale=color_scale,
        labels={energy_type: label},
    )

    fig.update_layout(
        clickmode="event+select", 
        font=dict(
            family="Montserrat, sans-serif",
            size=12
        ),
    )

    return fig

@app.callback(
    Output("country-holder", "children"),
    [Input("world-map", "clickData")],
)
def update_country_holder(clickData):
    if clickData is None:
        return dash.no_update
    return clickData['points'][0]['location']

@app.callback(
    [Output('modal', 'is_open'), Output("country-trend", "figure"), Output("modal-header", "children")],
    [Input("country-holder", "children"), Input("type-selection", "value"), Input('world-map', 'clickData')],
    [State("modal", "is_open")]
)
def check_source(country_code, energy_type, clickData, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else: 
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0] 
        if trigger_id == 'world-map': 
            return update_country_trend(country_code, energy_type, is_open)
        elif trigger_id == 'type-selection': 
            if is_open:
                return update_country_trend(country_code, energy_type, is_open)
            else:
                return dash.no_update
        else:
            return dash.no_update

def update_country_trend(country_code, energy_type, is_open):
    if country_code is None:
        return is_open, go.Figure(), "Country Trends"
    
    dff = df[df.Country == country_code]
    country_name = dff['Country_Name'].values[0]
    energy_label_dict = {
        'ff': 'Fossil Fuel Energy Innovation', 
        'renewables': 'Renewable Energy Innovation', 
        'share_ff': 'Share of Fossil Fuel Innovations', 
        'share_renewables': 'Share of Renewable Energy Innovations'
    }
    energy_label = energy_label_dict[energy_type]
    fig = get_country_trend_fig(dff, energy_type, energy_label)
    
    return (not is_open), fig, "Time Trend of {} for {}".format(energy_label, country_name)

# Run the app

if __name__ == "__main__":
    port = os.getenv("PORT", 8050)
    host = os.getenv("HOST", "localhost")
    app.run_server(debug=True, host=host, port=port)
    print("The app is running at: http://" + host + ":" + str(port))