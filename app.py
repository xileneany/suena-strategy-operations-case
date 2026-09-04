import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CCO Strategy & Operations Dashboard",
    page_icon="⚡",
    layout="wide"
)

# --------------------------------------------------
# VISUAL THEME
# --------------------------------------------------

CHARCOAL = "#101214"
GRAPHITE = "#1A1D21"
SOFT_ORANGE = "#E6A15A"
MUTED_ORANGE = "#B9793E"
OFF_WHITE = "#F2F2F0"
MUTED_TEXT = "#A9ADB3"
BORDER = "#30343A"

st.markdown(
    f"""
    <style>

    /* Main application */
    .stApp {{
        background-color: {CHARCOAL};
        color: {OFF_WHITE};
    }}

    /* Main content width */
    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {GRAPHITE};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: {OFF_WHITE};
    }}

    /* Main headings */
    h1 {{
        color: {OFF_WHITE} !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
    }}

    h2 {{
        color: {OFF_WHITE} !important;
        font-weight: 650 !important;
        letter-spacing: -0.02em;
    }}

    h3 {{
        color: {SOFT_ORANGE} !important;
    }}

    /* Metric values */
    [data-testid="stMetricValue"] {{
        color: {OFF_WHITE};
        font-weight: 600;
    }}

    /* Metric labels */
    [data-testid="stMetricLabel"] {{
        color: {MUTED_TEXT};
    }}

    /* Dividers */
    hr {{
        border-color: {BORDER} !important;
    }}

    /* Info box */
    [data-testid="stAlert"] {{
        background-color: {GRAPHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {SOFT_ORANGE};
        color: {OFF_WHITE};
    }}

    /* Dataframe */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 8px;
    }}

    /* Captions */
    .stCaption {{
        color: {MUTED_TEXT} !important;
    }}

    /* Links */
    a {{
        color: {SOFT_ORANGE} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/pipeline.csv")
    df["weighted_value"] = df["deal_value"] * df["probability"]
    return df


df = load_data()


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("CCO Strategy & Operations Dashboard")

st.markdown(
    f"""
    <div style="
        width: 75px;
        height: 4px;
        background-color: {SOFT_ORANGE};
        border-radius: 4px;
        margin-top: -12px;
        margin-bottom: 22px;
    "></div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Independent case study for suena energy | "
    "Revenue Operations • Commercial Insights • Decision Support"
)

st.markdown(
    f"""
    <div style="
        background-color: {GRAPHITE};
        border: 1px solid {BORDER};
        border-left: 4px solid {SOFT_ORANGE};
        padding: 14px 18px;
        border-radius: 7px;
        color: {MUTED_TEXT};
        font-size: 0.9rem;
        margin: 18px 0 30px 0;
    ">
        <strong style="color:{OFF_WHITE};">
            Independent case study
        </strong>
        &nbsp;•&nbsp;
        All commercial figures are synthetic and used solely to demonstrate
        analytical and decision-support capabilities. No internal suena energy
        data is used.
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Pipeline Filters")

markets = st.sidebar.multiselect(
    "Market",
    options=df["market"].unique(),
    default=list(df["market"].unique())
)

stages = st.sidebar.multiselect(
    "Pipeline Stage",
    options=df["stage"].unique(),
    default=list(df["stage"].unique())
)

filtered = df[
    (df["market"].isin(markets))
    & (df["stage"].isin(stages))
]


# --------------------------------------------------
# EXECUTIVE KPIs
# --------------------------------------------------

st.subheader("Executive Overview")

total_pipeline = filtered["deal_value"].sum()
weighted_pipeline = filtered["weighted_value"].sum()
total_mw = filtered["mw"].sum()
avg_deal = filtered["deal_value"].mean()

won_deals = len(filtered[filtered["stage"] == "Won"])
total_opportunities = len(filtered)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Pipeline",
    f"€{total_pipeline / 1_000_000:.2f}M"
)

c2.metric(
    "Weighted Pipeline",
    f"€{weighted_pipeline / 1_000_000:.2f}M"
)

c3.metric(
    "Assets in Pipeline",
    f"{total_mw:,.0f} MW"
)

c4.metric(
    "Average Deal Size",
    f"€{avg_deal / 1_000:.0f}K"
)

c5.metric(
    "Won / Opportunities",
    f"{won_deals} / {total_opportunities}"
)


# --------------------------------------------------
# CCO BRIEF
# --------------------------------------------------

st.divider()

st.subheader("CCO Brief")

market_pipeline = (
    filtered.groupby("market")["deal_value"]
    .sum()
    .sort_values(ascending=False)
)

if not market_pipeline.empty:

    largest_market = market_pipeline.index[0]

    stalled = filtered[
        (filtered["days_in_stage"] >= 30)
        & (filtered["stage"] != "Won")
    ]

    stalled_weighted_value = stalled["weighted_value"].sum()

    st.markdown(
        f"""
### What changed / what matters

**{largest_market} currently represents the largest source of pipeline value.**

At the same time, **{len(stalled)} opportunities** have spent 30 or more days
in their current pipeline stage, representing approximately
**€{stalled_weighted_value:,.0f} in weighted pipeline**.

### Management question

Are these opportunities progressing slowly because of commercial qualification,
technical evaluation capacity, customer decision cycles, or internal execution?

### Recommended action

Review every opportunity with **30+ days in stage** during the next pipeline
meeting and assign a clear blocker, owner, and next action.
"""
    )


# --------------------------------------------------
# PIPELINE CHARTS
# --------------------------------------------------

st.divider()

st.subheader("Commercial Performance")

left, right = st.columns(2)


with left:

    st.markdown("#### Pipeline by Market")

    market_chart = (
        filtered.groupby("market", as_index=False)["deal_value"]
        .sum()
        .sort_values("deal_value", ascending=False)
    )

    fig_market = px.bar(
        market_chart,
        x="market",
        y="deal_value",
        labels={
            "market": "Market",
            "deal_value": "Pipeline Value (€)"
        }
    )

fig_market.update_traces(
    marker_color=SOFT_ORANGE
)

fig_market.update_layout(
    paper_bgcolor=CHARCOAL,
    plot_bgcolor=CHARCOAL,
    font_color=OFF_WHITE,
    showlegend=False,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(
        showgrid=False,
        linecolor=BORDER
    ),
    yaxis=dict(
        gridcolor=BORDER,
        zeroline=False
    )
)
    st.plotly_chart(
        fig_market,
        use_container_width=True
    )


with right:

    st.markdown("#### Pipeline by Stage")

    stage_chart = (
        filtered.groupby("stage", as_index=False)["deal_value"]
        .sum()
    )

    fig_stage = px.bar(
        stage_chart,
        x="stage",
        y="deal_value",
        labels={
            "stage": "Pipeline Stage",
            "deal_value": "Pipeline Value (€)"
        }
    )
    fig_stage.update_traces(
    marker_color=MUTED_ORANGE
)

    fig_stage.update_layout(
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(
            showgrid=False,
            linecolor=BORDER
        ),
        yaxis=dict(
            gridcolor=BORDER,
            zeroline=False
        )
    )
    
    st.plotly_chart(
        fig_stage,
        use_container_width=True
    )


# --------------------------------------------------
# PIPELINE RISK
# --------------------------------------------------

st.divider()

st.subheader("Pipeline Attention Required")

risk_df = filtered[
    (filtered["days_in_stage"] >= 30)
    & (filtered["stage"] != "Won")
].copy()

if not risk_df.empty:

    risk_df["Probability"] = (
        risk_df["probability"] * 100
    ).round(0).astype(int).astype(str) + "%"

    display_risk = risk_df[
        [
            "opportunity",
            "market",
            "stage",
            "deal_value",
            "Probability",
            "mw",
            "days_in_stage"
        ]
    ].copy()

    display_risk.columns = [
        "Opportunity",
        "Market",
        "Stage",
        "Deal Value (€)",
        "Probability",
        "MW",
        "Days in Stage"
    ]

    st.dataframe(
        display_risk,
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "No opportunities currently exceed the 30-day attention threshold."
    )


# --------------------------------------------------
# DECISION SUPPORT
# --------------------------------------------------

st.divider()

st.subheader("Decision Support")

risk_value = risk_df["weighted_value"].sum()

if risk_value > 0:

    st.warning(
        f"€{risk_value:,.0f} of weighted pipeline is currently tied to "
        "opportunities that have spent 30+ days in their current stage."
    )

st.markdown(
    """
**Suggested next steps**

1. Identify the primary blocker for each stalled opportunity.
2. Separate commercial blockers from technical and customer-side blockers.
3. Assign an owner and next action to every material opportunity.
4. Reassess whether current forecast probabilities remain realistic.
5. Escalate material revenue risks during the next CCO pipeline review.
"""
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Independent Strategy & Operations case study • "
    "Synthetic dataset • Built by Xilene Siquero"
)
