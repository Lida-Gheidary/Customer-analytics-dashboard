import dash
from dash import dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# -----------------------
# Data
# -----------------------
df = pd.read_csv("WA_Fn-UseC_-Marketing-Customer-Value-Analysis.csv")

# -----------------------
# App
# -----------------------
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# -----------------------
# Style constants
# -----------------------
FONT_FAMILY = "'Lexend Peta', sans-serif"
COLOR_PRIMARY = "#111111"
COLOR_SECONDARY = "#555555"
COLOR_BACKGROUND = "#FFFFFF"
COLOR_CARD = "#F8F9FA"

KPI_COLORS = {
    "customers": "#3498db",  # blue
    "clv": "#2ecc71",        # green
    "premium": "#9b59b6",    # purple
    "avg": "#f39c12"         # orange
}

def card_container_style():
    return {
        "border": "none",
        "borderRadius": "12px",
        "backgroundColor": COLOR_CARD,
        "boxShadow": "0 2px 12px rgba(0,0,0,0.06)"
    }

def base_plot_layout(fig, title):
    fig.update_layout(
        title=title,
        font_family=FONT_FAMILY,
        title_font_size=18,
        title_font_color=COLOR_PRIMARY,
        paper_bgcolor=COLOR_BACKGROUND,
        plot_bgcolor=COLOR_BACKGROUND,
        margin=dict(t=60, b=30, l=30, r=30),
        legend_title_text=""
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EEEEEE", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEEEEE", zeroline=False)
    return fig

def create_kpi_card(title, default_value, value_id, accent_color, tooltip_text):
    tooltip_id = f"tip-{value_id}"
    return dbc.Card(
        dbc.CardBody([
            html.Div([
                html.Span(title, style={
                    "fontFamily": FONT_FAMILY,
                    "color": COLOR_SECONDARY,
                    "fontSize": "13px",
                    "letterSpacing": "0.2px",
                }),
                html.Span(" ⓘ", id=tooltip_id, style={
                    "cursor": "pointer",
                    "marginLeft": "6px",
                    "color": "#777",
                    "fontSize": "12px"
                })
            ], style={"marginBottom": "10px"}),
            html.Div(default_value, id=value_id, style={
                "fontFamily": FONT_FAMILY,
                "color": COLOR_PRIMARY,
                "fontSize": "34px",
                "fontWeight": "800",
                "lineHeight": "1.1"
            }),
            dbc.Tooltip(tooltip_text, target=tooltip_id, placement="top")
        ]),
        style={
            **card_container_style(),
            "borderLeft": f"6px solid {accent_color}",
            "minHeight": "112px"
        }
    )

# -----------------------
# Layout
# -----------------------
app.layout = dbc.Container([

    # NAVBAR
dbc.Navbar(
    dbc.Container([
        html.Div(),  # empty left side
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Live Demo", href="#", external_link=True)),
            dbc.NavItem(dbc.NavLink("GitHub", href="#", external_link=True)),
        ], navbar=True)
    ]),
    color="white",
    dark=False,
    className="mb-3",
    style={"borderBottom": "1px solid #EAEAEA"}
),

# HERO HEADER (light grey gradient + white text)
html.Div(
    [
        html.H1(
            "Customer Analytics Dashboard",
            style={
                "fontFamily": FONT_FAMILY,
                "fontWeight": "900",
                "color": "white",
                "marginBottom": "6px",
            },
        ),
        html.Div(
            "Insurance Marketing Performance Analysis",
            style={
                "fontFamily": FONT_FAMILY,
                "color": "rgba(255,255,255,0.85)",
                "fontSize": "14px",
                "letterSpacing": "0.4px",
            },
        ),
    ],
    style={
        "textAlign": "center",
        "padding": "34px 18px",
        "borderRadius": "14px",
        "marginBottom": "22px",
        "backgroundColor": "#6a6a6a",
        "backgroundImage": (
            "linear-gradient(135deg, #9a9a9a 0%, #6a6a6a 50%, #7f7f7f 100%), "
            "radial-gradient(circle at 25% 20%, rgba(255,255,255,0.25) 0%, rgba(255,255,255,0) 60%)"
        ),
        "backgroundRepeat": "no-repeat",
        "backgroundSize": "cover",
    },
),
# CONTEXT / DATASET EXPLANATION
dbc.Card(
    dbc.CardBody([
        html.H5("Context", style={"fontFamily": FONT_FAMILY, "fontWeight": "900", "marginBottom": "10px"}),
        html.P(
            "This dashboard uses a public IBM Watson insurance customer dataset for marketing/CRM analytics practice. "
            "It includes customer segments, policy attributes, monthly premium (monthly revenue), estimated CLV, and a "
            "campaign outcome field (Response).",
            style={"fontFamily": FONT_FAMILY, "color": COLOR_SECONDARY, "marginBottom": "8px"}
        ),
        html.P(
            "Response = Yes means the customer took the campaign’s intended action (e.g., accepted the offer/renewed). "
            "Response = No means they did not.",
            style={"fontFamily": FONT_FAMILY, "color": COLOR_SECONDARY, "marginBottom": "0px"}
        ),
    ]),
    style={
        "border": "none",
        "borderRadius": "12px",
        "backgroundColor": "#FFFFFF",
        "boxShadow": "0 2px 12px rgba(0,0,0,0.06)",
        "marginBottom": "12px"
    }
),

    # FILTERS
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Sales Channel", style={
                        "fontFamily": FONT_FAMILY, "fontWeight": "700", "marginBottom": "8px"
                    }),
                    dcc.Dropdown(
                        id="sales-channel-dropdown",
                        options=[{"label": "All Channels", "value": "All"}] +
                                [{"label": v, "value": v} for v in sorted(df["Sales Channel"].dropna().unique())],
                        value="All",
                        clearable=False,
                        style={"fontFamily": FONT_FAMILY}
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Policy Type", style={
                        "fontFamily": FONT_FAMILY, "fontWeight": "700", "marginBottom": "8px"
                    }),
                    dcc.Dropdown(
                        id="policy-type-dropdown",
                        options=[{"label": "All Types", "value": "All"}] +
                                [{"label": v, "value": v} for v in sorted(df["Policy Type"].dropna().unique())],
                        value="All",
                        clearable=False,
                        style={"fontFamily": FONT_FAMILY}
                    )
                ], md=4),

                dbc.Col([
                    html.Label("Coverage", style={
                        "fontFamily": FONT_FAMILY, "fontWeight": "700", "marginBottom": "8px"
                    }),
                    dcc.Dropdown(
                        id="coverage-dropdown",
                        options=[{"label": "All Coverage", "value": "All"}] +
                                [{"label": v, "value": v} for v in sorted(df["Coverage"].dropna().unique())],
                        value="All",
                        clearable=False,
                        style={"fontFamily": FONT_FAMILY}
                    )
                ], md=4),
            ], className="g-3")
        ]),
        style={
            "border": "none",
            "borderRadius": "12px",
            "backgroundColor": "#F0F4F8",
            "boxShadow": "0 2px 12px rgba(0,0,0,0.06)",
            "marginBottom": "12px"
        }
    ),

    # DOWNLOAD BUTTON
    dbc.Row([
        dbc.Col([
            dbc.Button(
                "Download filtered CSV",
                id="btn-download-csv",
                color="dark",
                outline=True,
                style={"fontFamily": FONT_FAMILY, "fontWeight": "700"}
            ),
            dcc.Download(id="download-csv")
        ], md="auto"),
    ], className="mb-3"),

    # KPI ROW
    dbc.Row([
        dbc.Col(create_kpi_card(
            "Total Customers", "0", "kpi-customers", KPI_COLORS["customers"],
            "Number of customers in the current selection."
        ), md=3),
        dbc.Col(create_kpi_card(
            "Total CLV", "$0", "kpi-clv", KPI_COLORS["clv"],
            "Sum of Customer Lifetime Value (estimated total value from these customers)."
        ), md=3),
        dbc.Col(create_kpi_card(
            "Total Monthly Premium", "$0", "kpi-premium", KPI_COLORS["premium"],
            "Sum of Monthly Premium Auto (monthly revenue from the selected customers)."
        ), md=3),
        dbc.Col(create_kpi_card(
            "Avg CLV", "$0", "kpi-avg-clv", KPI_COLORS["avg"],
            "Average Customer Lifetime Value per customer in the selection."
        ), md=3),
    ], className="g-3", style={"marginBottom": "12px"}),

    # INSIGHTS PANEL
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Insights", style={
                        "fontFamily": FONT_FAMILY,
                        "fontWeight": "900",
                        "marginBottom": "10px"
                    }),
                    html.Div(id="insights-panel", style={
                        "fontFamily": FONT_FAMILY,
                        "color": COLOR_SECONDARY
                    })
                ]),
                style=card_container_style()
            ),
            md=12
        )
    ], className="mb-3"),

    # CHARTS ROW 1
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody(dcc.Graph(id="treemap-chart")), style=card_container_style()),
            md=8
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody(dcc.Graph(id="response-pie-chart")), style=card_container_style()),
            md=4
        ),
    ], className="g-3", style={"marginBottom": "12px"}),

    # CHARTS ROW 2
    dbc.Row([
        dbc.Col(
            dbc.Card(dbc.CardBody(dcc.Graph(id="clv-distribution")), style=card_container_style()),
            md=6
        ),
        dbc.Col(
            dbc.Card(dbc.CardBody(dcc.Graph(id="scatter-chart")), style=card_container_style()),
            md=6
        ),
    ], className="g-3", style={"marginBottom": "40px"}),

], fluid=True, style={
    "background": "linear-gradient(180deg, #f7f7f7 0%, #ececec 100%)",
    "minHeight": "100vh",
    "paddingBottom": "40px"
})



# -----------------------
# Main dashboard callback
# -----------------------
@app.callback(
    [
        Output("kpi-customers", "children"),
        Output("kpi-clv", "children"),
        Output("kpi-premium", "children"),
        Output("kpi-avg-clv", "children"),
        Output("treemap-chart", "figure"),
        Output("response-pie-chart", "figure"),
        Output("clv-distribution", "figure"),
        Output("scatter-chart", "figure"),
        Output("insights-panel", "children"),
    ],
    [
        Input("sales-channel-dropdown", "value"),
        Input("policy-type-dropdown", "value"),
        Input("coverage-dropdown", "value"),
    ]
)
def update_dashboard(selected_channel, selected_policy, selected_coverage):
    filtered_df = df.copy()

    if selected_channel != "All":
        filtered_df = filtered_df[filtered_df["Sales Channel"] == selected_channel]
    if selected_policy != "All":
        filtered_df = filtered_df[filtered_df["Policy Type"] == selected_policy]
    if selected_coverage != "All":
        filtered_df = filtered_df[filtered_df["Coverage"] == selected_coverage]

    # KPIs
    total_customers = f"{len(filtered_df):,}"
    total_clv_val = filtered_df["Customer Lifetime Value"].sum()
    total_premium_val = filtered_df["Monthly Premium Auto"].sum()
    avg_clv_val = filtered_df["Customer Lifetime Value"].mean()

    total_clv = f"${total_clv_val:,.0f}"
    total_premium = f"${total_premium_val:,.0f}"
    avg_clv = f"${avg_clv_val:,.0f}" if pd.notna(avg_clv_val) else "$0"

    # Treemap (colorful)
    treemap_fig = px.treemap(
        filtered_df,
        path=["Sales Channel", "Policy Type"],
        values="Customer Lifetime Value",
        color="Customer Lifetime Value",
        color_continuous_scale="Viridis",
    )
    treemap_fig = base_plot_layout(treemap_fig, "Customer Lifetime Value Breakdown")

    # Response pie (clear labels)
    response_counts = filtered_df["Response"].value_counts(dropna=False)
    total_resp = response_counts.sum() if response_counts.sum() else 1

    pie_labels = []
    pie_values = []
    pie_colors = []

    for key in response_counts.index:
        val = int(response_counts[key])
        pct = (val / total_resp) * 100
        pie_labels.append(f"{key}: {pct:.1f}%")
        pie_values.append(val)

        if str(key).lower() == "yes":
            pie_colors.append("#2ecc71")  # green
        elif str(key).lower() == "no":
            pie_colors.append("#e74c3c")  # red
        else:
            pie_colors.append("#95a5a6")  # gray

    pie_fig = go.Figure(data=[go.Pie(
        labels=pie_labels,
        values=pie_values,
        hole=0.45,
        marker=dict(colors=pie_colors),
        textposition="inside",
        hovertemplate="%{label}<br>Count: %{value}<extra></extra>"
    )])
    pie_fig = base_plot_layout(pie_fig, "Customers Who Responded to the Campaign")
    pie_fig.update_layout(showlegend=True)

    # Box plot (colorful)
    box_fig = px.box(
        filtered_df,
        x="Policy Type",
        y="Customer Lifetime Value",
        color="Policy Type",
        color_discrete_sequence=["#2ecc71", "#3498db", "#e74c3c"]
    )
    box_fig = base_plot_layout(box_fig, "CLV Distribution by Policy Type")
    box_fig.update_layout(showlegend=False)

    # Scatter (colorful)
    scatter_fig = px.scatter(
        filtered_df,
        x="Monthly Premium Auto",
        y="Customer Lifetime Value",
        color="Policy Type",
        size="Income",
        opacity=0.70,
        color_discrete_sequence=["#9b59b6", "#f39c12", "#1abc9c"]
    )
    scatter_fig = base_plot_layout(scatter_fig, "CLV vs Monthly Premium (Bubble size = Income)")

    # Insights panel (simple, readable)
    insights_items = []

    if len(filtered_df) == 0:
        insights = html.Div("No data available for the selected filters.")
    else:
        # Top policy type by total CLV
        top_policy = (
            filtered_df.groupby("Policy Type")["Customer Lifetime Value"].sum()
            .sort_values(ascending=False)
        )
        top_policy_name = top_policy.index[0] if len(top_policy) else "N/A"

        # Response rate (Yes)
        response_rate = (filtered_df["Response"].astype(str).str.lower().eq("yes").mean() * 100)

        # Top sales channel by total premium (within selection)
        top_channel = (
            filtered_df.groupby("Sales Channel")["Monthly Premium Auto"].sum()
            .sort_values(ascending=False)
        )
        top_channel_name = top_channel.index[0] if len(top_channel) else "N/A"

        insights_items = [
            f"Top CLV policy type in this selection: {top_policy_name}.",
            f"Response rate (Yes) in this selection: {response_rate:.1f}%.",
            f"Highest monthly premium channel in this selection: {top_channel_name}.",
        ]
        insights = html.Ul([html.Li(x) for x in insights_items])

    return (
        total_customers,
        total_clv,
        total_premium,
        avg_clv,
        treemap_fig,
        pie_fig,
        box_fig,
        scatter_fig,
        insights,
    )


# -----------------------
# Download callback
# -----------------------
@app.callback(
    Output("download-csv", "data"),
    Input("btn-download-csv", "n_clicks"),
    State("sales-channel-dropdown", "value"),
    State("policy-type-dropdown", "value"),
    State("coverage-dropdown", "value"),
    prevent_initial_call=True
)
def download_filtered_csv(n_clicks, selected_channel, selected_policy, selected_coverage):
    # Only download when the button is what triggered the callback
    if ctx.triggered_id != "btn-download-csv":
        return dash.no_update

    filtered_df = df.copy()
    if selected_channel != "All":
        filtered_df = filtered_df[filtered_df["Sales Channel"] == selected_channel]
    if selected_policy != "All":
        filtered_df = filtered_df[filtered_df["Policy Type"] == selected_policy]
    if selected_coverage != "All":
        filtered_df = filtered_df[filtered_df["Coverage"] == selected_coverage]

    return dcc.send_data_frame(filtered_df.to_csv, "filtered_customers.csv", index=False)

# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)
