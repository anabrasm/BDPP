import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

def init_layout(df):
    layout = html.Div(
    [
        html.Header(
            [
                html.H1("Green Energy Innovation"),
                html.H5(
                    "Work by Ana Brás Monteiro, Theodor Friederiszick, Carole Marullaz"
                ),
            ]
        ),
        html.Main(
            [
                html.P(
                    [
                        "Welcome to our page! ",
                        "Here, you will find a range of interactive world maps showcasing the progress of energy innovation.",
                    ],
                    className="main-text",
                ),
                html.P(
                    [
                        "Our maps show the number of patents filed globally for both renewable and fossil fuel energy technologies, ",
                        "and also the weight that these represent in the total amount of energy innovations. ",
                        "You can also use our slider to select a specific year and the maps will adjust accordingly! ",
                        "If you want to know more about a specific country, click on it and a window will pop up with the time trend of the chosen variable for that country.",
                    ],
                    className="main-text",
                ),
                html.P(
                    [
                        "Scroll further down to learn more about our data sources and how we categorize the different variables. ",
                        "Hope you enjoy it!",
                    ],
                    className="main-text",
                ),
                dcc.Dropdown(
                    id="type-selection",
                    options=[
                        {"label": "Renewable Energy Innovation", "value": "renewables"},
                        {"label": "Fossil Fuel Energy Innovation", "value": "ff"},
                        {
                            "label": "Share of Renewable Energy Innovations",
                            "value": "share_renewables",
                        },
                        {
                            "label": "Share of Fossil Fuel Innovations",
                            "value": "share_ff",
                        },
                        
                    ],
                    value="renewables",
                    clearable=False,
                    className="dropdown",
                ),
                dcc.Slider(
                    id="year-slider",
                    min=df["Year"].min(),
                    max=df["Year"].max(),
                    value=df["Year"].max(),  # Set last year as the default value
                    marks={str(year): str(year) for year in df["Year"].unique()},
                    step=None,
                ),
                dcc.Graph(id="world-map"),
                html.Div(
                    id="country-holder"
                ),  # Add hidden Div
                dbc.Modal(
                    [
                        dbc.ModalHeader(id="modal-header"),
                        dbc.ModalBody(dcc.Graph(id="country-trend")),
                    ],
                    id="modal",
                    is_open=False,
                ),
            ]
        ),
        html.Footer(
            [
                html.Div(
                    [
                        html.H4("Data Source", className="footer-heading"),
                        html.P(
                            "PATSTAT is a database that contains bibliographical and legal status patent data from more than 150 countries. It is maintained by the European Patent Office (EPO) and is available to the public for free. PATSTAT contains information on about 150 million patent documents. In particular, information about the inventors, patent classifications and citations are available. The data used in this project was downloaded in March 2021 and covers the period 1978 to 2019.",
                            className="footer-text",
                        ),
                        html.H4("Classification", className="footer-heading"),
                        html.P(
                            [
                                "We allocate a patent to a country based on the nationality of its inventors. ",
                                "If they have different nationalities, we use the nationality that occurs the most. ",
                                "To classify the patents, we use the international patent classification (IPC) ",
                                "and the cooperative patent classification (CPC) systems. ",
                                "For fossil fuel energy innovations, we follow ",
                                "Lanzi et al. (2011)",
                                html.Sup("1"),
                                " who gather the IPC that correspond to fossil fuel energy innovations. ",
                                "For renewable energy innovations, we use the dedicated CPC code.",
                            ],
                            className="footer-text",
                        ),
                        html.P(
                            [
                                html.Small(
                                    html.I(
                                        '1 Lanzi, Elisa, Elena Verdolini, and Ivan Haščič. 2011. "Efficiency-improving fossil fuel technologies for electricity generation: Data selection and trends." Energy Policy, 39(11): 7000–7014.'
                                    )
                                )
                            ],
                            className="footer-text small-font",
                        ),
                    ],
                    className="footer-column",
                ),
                html.Div(
                    [
                        html.H4("Variables", className="footer-heading"),
                        html.P(
                            [
                                html.U("Fossil Fuel Energy Innovation:"),
                                " Number of innovations in fossil fuel energy technologies",
                            ],
                            className="footer-text",
                        ),
                        html.P(
                            [
                                html.U("Renewable Energy Innovation:"),
                                "Number of innovations in renewable energy technologies",
                            ],
                            className="footer-text",
                        ),
                        html.P(
                            [
                                html.U("Share of Fossil Fuel Innovations:"),
                                "Number of innovations in fossil fuel energy technologies relative to the total number of innovations in energy technologies",
                            ],
                            className="footer-text",
                        ),
                        html.P(
                            [
                                html.U("Share of Renewable Energy Innovations:"),
                                "Number of innovations in renewable energy technologies relative to the total number of innovations in energy technologies",
                            ],
                            className="footer-text",
                        ),
                    ],
                    className="footer-column",
                ),
            ]
        ),
        html.Button(id="dummy-button"),
    ]
)
    return layout

