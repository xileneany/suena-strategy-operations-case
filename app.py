import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CCO Strategy & Operations Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# VISUAL THEME
# ==================================================

CHARCOAL = "#101214"
GRAPHITE = "#1A1D21"
SOFT_ORANGE = "#E6A15A"
MUTED_ORANGE = "#B9793E"
OFF_WHITE = "#F2F2F0"
MUTED_TEXT = "#A9ADB3"
BORDER = "#30343A"

STAGE_ORDER = [
    "Qualified",
    "Technical Evaluation",
    "Proposal",
    "Negotiation",
    "Won"
]


st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {CHARCOAL};
        color: {OFF_WHITE};
    }}

    .block-container {{
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }}

    [data-testid="stSidebar"] {{
        background-color: {GRAPHITE};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] * {{
        color: {OFF_WHITE};
    }}

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

    [data-testid="stMetric"] {{
        background-color: {GRAPHITE};
        border: 1px solid {BORDER};
        border-top: 3px solid {SOFT_ORANGE};
        padding: 16px 18px;
        border-radius: 8px;
    }}

    [data-testid="stMetricValue"] {{
        color: {OFF_WHITE};
        font-weight: 600;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED_TEXT};
    }}

    hr {{
        border-color: {BORDER} !important;
    }}

    [data-testid="stAlert"] {{
        background-color: {GRAPHITE};
        border: 1px solid {BORDER};
        color: {OFF_WHITE};
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 8px;
    }}

    .stCaption {{
        color: {MUTED_TEXT} !important;
    }}

    a {{
        color: {SOFT_ORANGE} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# DATA
# ==================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/pipeline.csv")
    df["weighted_value"] = df["deal_value"] * df["probability"]
    return df


df = load_data()

@st.cache_data
def load_market_data():
    market_df = pd.read_csv("data/market_expansion.csv")
    return market_df


market_df = load_market_data()

# ==================================================
# HELPERS
# ==================================================

def euro_m(value):
    return f"€{value / 1_000_000:.2f}M"


def euro_k(value):
    return f"€{value / 1_000:.0f}K"


def style_chart(fig):
    fig.update_layout(
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            showgrid=False,
            linecolor=BORDER
        ),
        yaxis=dict(
            gridcolor=BORDER,
            zeroline=False
        )
    )
    return fig


def page_header(title, subtitle):
    st.title(title)

    st.markdown(
        f"""
        <div style="
            width: 75px;
            height: 4px;
            background-color: {SOFT_ORANGE};
            border-radius: 4px;
            margin-top: -12px;
            margin-bottom: 22px;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(subtitle)


def case_disclaimer():
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


def footer():
    st.divider()
    st.caption(
        "Independent Strategy & Operations case study • "
        "Synthetic dataset • Built by Xilene Siquero"
    )


def pipeline_filters(data, key_prefix):
    st.sidebar.markdown("### Filters")

    markets = st.sidebar.multiselect(
        "Market",
        options=list(data["market"].unique()),
        default=list(data["market"].unique()),
        key=f"{key_prefix}_markets"
    )

    stages = st.sidebar.multiselect(
        "Pipeline Stage",
        options=STAGE_ORDER,
        default=STAGE_ORDER,
        key=f"{key_prefix}_stages"
    )

    filtered = data[
        (data["market"].isin(markets))
        & (data["stage"].isin(stages))
    ].copy()

    return filtered


# ==================================================
# NAVIGATION
# ==================================================

st.sidebar.markdown("### Strategy & Operations")

page = st.sidebar.radio(
    "Navigate",
    [
        "Executive Overview",
        "Revenue & Pipeline",
        "Market Expansion",
        "Scenario Analysis",
        "Board Brief",
        "About This Case"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()


# ==================================================
# EXECUTIVE OVERVIEW
# ==================================================

def executive_overview():

    page_header(
        "CCO Strategy & Operations Dashboard",
        "Revenue Operations • Commercial Insights • Decision Support"
    )

    case_disclaimer()

    filtered = pipeline_filters(df, "overview")

    st.subheader("Executive Overview")

    total_pipeline = filtered["deal_value"].sum()
    weighted_pipeline = filtered["weighted_value"].sum()
    total_mw = filtered["mw"].sum()

    avg_deal = (
        filtered["deal_value"].mean()
        if not filtered.empty
        else 0
    )

    won_deals = len(
        filtered[filtered["stage"] == "Won"]
    )

    total_opportunities = len(filtered)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Pipeline",
        euro_m(total_pipeline)
    )

    c2.metric(
        "Weighted Pipeline",
        euro_m(weighted_pipeline)
    )

    c3.metric(
        "Assets in Pipeline",
        f"{total_mw:,.0f} MW"
    )

    c4.metric(
        "Average Deal Size",
        euro_k(avg_deal)
    )

    c5.metric(
        "Won / Opportunities",
        f"{won_deals} / {total_opportunities}"
    )

    st.divider()
    st.subheader("CCO Brief")

    market_pipeline = (
        filtered
        .groupby("market")["deal_value"]
        .sum()
        .sort_values(ascending=False)
    )

    stalled = filtered[
        (filtered["days_in_stage"] >= 30)
        & (filtered["stage"] != "Won")
    ].copy()

    stalled_weighted = stalled["weighted_value"].sum()

    if not market_pipeline.empty:

        largest_market = market_pipeline.index[0]

        st.markdown(
            f"""
### What matters

**{largest_market} currently represents the largest source of pipeline value.**

At the same time, **{len(stalled)} opportunities** have spent 30 or more
days in their current pipeline stage, representing approximately
**{euro_k(stalled_weighted)} in weighted pipeline**.

### Management question

Are these opportunities progressing slowly because of commercial
qualification, technical evaluation capacity, customer decision cycles,
or internal execution?

### Recommended action

Review every opportunity with **30+ days in stage** during the next
pipeline meeting and assign a clear blocker, owner, and next action.
"""
        )

    else:
        st.write(
            "Select at least one market and stage "
            "to display the executive analysis."
        )

    st.divider()
    st.subheader("Commercial Performance")

    left, right = st.columns(2)

    with left:

        st.markdown("#### Pipeline by Market")

        market_chart = (
            filtered
            .groupby("market", as_index=False)["deal_value"]
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

        style_chart(fig_market)

        st.plotly_chart(
            fig_market,
            use_container_width=True
        )

    with right:

        st.markdown("#### Pipeline by Stage")

        stage_chart = (
            filtered
            .groupby("stage", as_index=False)["deal_value"]
            .sum()
        )

        fig_stage = px.bar(
            stage_chart,
            x="stage",
            y="deal_value",
            category_orders={"stage": STAGE_ORDER},
            labels={
                "stage": "Pipeline Stage",
                "deal_value": "Pipeline Value (€)"
            }
        )

        fig_stage.update_traces(
            marker_color=MUTED_ORANGE
        )

        style_chart(fig_stage)

        st.plotly_chart(
            fig_stage,
            use_container_width=True
        )

    st.divider()
    st.subheader("Pipeline Attention Required")

    risk_df = filtered[
        (filtered["days_in_stage"] >= 30)
        & (filtered["stage"] != "Won")
    ].copy()

    if not risk_df.empty:

        display_risk = risk_df[
            [
                "opportunity",
                "market",
                "stage",
                "deal_value",
                "probability",
                "mw",
                "days_in_stage"
            ]
        ].copy()

        display_risk["probability"] = (
            display_risk["probability"] * 100
        ).round(0).astype(int).astype(str) + "%"

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
            "No opportunities currently exceed "
            "the 30-day attention threshold."
        )

    st.divider()
    st.subheader("Decision Support")

    risk_value = (
        risk_df["weighted_value"].sum()
        if not risk_df.empty
        else 0
    )

    if risk_value > 0:
        st.warning(
            f"{euro_k(risk_value)} of weighted pipeline is currently "
            "tied to opportunities that have spent 30+ days "
            "in their current stage."
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

    footer()


# ==================================================
# REVENUE & PIPELINE
# ==================================================

def revenue_pipeline():

    page_header(
        "Revenue & Pipeline",
        "Pipeline health • Stage ageing • Forecast exposure • Commercial priorities"
    )

    case_disclaimer()

    filtered = pipeline_filters(df, "revenue")

    if filtered.empty:
        st.warning(
            "Select at least one market and pipeline stage "
            "to display the analysis."
        )
        footer()
        return

    active = filtered[
        filtered["stage"] != "Won"
    ].copy()

    total_pipeline = filtered["deal_value"].sum()
    weighted_pipeline = filtered["weighted_value"].sum()

    active_opportunities = len(active)

    late_stage = filtered[
        filtered["stage"].isin(
            ["Proposal", "Negotiation"]
        )
    ]

    late_stage_value = late_stage["deal_value"].sum()

    stalled = active[
        active["days_in_stage"] >= 30
    ].copy()

    stalled_weighted = stalled["weighted_value"].sum()

    st.subheader("Pipeline Snapshot")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Pipeline",
        euro_m(total_pipeline)
    )

    c2.metric(
        "Weighted Pipeline",
        euro_m(weighted_pipeline)
    )

    c3.metric(
        "Active Opportunities",
        f"{active_opportunities}"
    )

    c4.metric(
        "Proposal + Negotiation",
        euro_m(late_stage_value)
    )

    # --------------------------------------------------
    # PIPELINE STRUCTURE
    # --------------------------------------------------

    st.divider()
    st.subheader("Pipeline Structure")

    stage_summary = (
        filtered
        .groupby("stage", as_index=False)
        .agg(
            opportunities=("opportunity", "count"),
            pipeline_value=("deal_value", "sum"),
            weighted_value=("weighted_value", "sum"),
            avg_days_in_stage=("days_in_stage", "mean")
        )
    )

    stage_summary["stage"] = pd.Categorical(
        stage_summary["stage"],
        categories=STAGE_ORDER,
        ordered=True
    )

    stage_summary = stage_summary.sort_values("stage")

    left, right = st.columns(2)

    with left:

        st.markdown("#### Pipeline Value by Stage")

        fig_stage_value = px.bar(
            stage_summary,
            x="stage",
            y="pipeline_value",
            category_orders={"stage": STAGE_ORDER},
            labels={
                "stage": "Pipeline Stage",
                "pipeline_value": "Pipeline Value (€)"
            }
        )

        fig_stage_value.update_traces(
            marker_color=SOFT_ORANGE
        )

        style_chart(fig_stage_value)

        st.plotly_chart(
            fig_stage_value,
            use_container_width=True
        )

    with right:

        st.markdown("#### Weighted Value by Stage")

        fig_weighted = px.bar(
            stage_summary,
            x="stage",
            y="weighted_value",
            category_orders={"stage": STAGE_ORDER},
            labels={
                "stage": "Pipeline Stage",
                "weighted_value": "Weighted Value (€)"
            }
        )

        fig_weighted.update_traces(
            marker_color=MUTED_ORANGE
        )

        style_chart(fig_weighted)

        st.plotly_chart(
            fig_weighted,
            use_container_width=True
        )

    # --------------------------------------------------
    # STAGE AGEING
    # --------------------------------------------------

    st.divider()
    st.subheader("Stage Ageing")

    st.caption(
        "Average days currently spent in each stage. "
        "This is a snapshot of pipeline ageing, not a historical sales-cycle metric."
    )

    ageing = (
        active
        .groupby("stage", as_index=False)
        .agg(
            avg_days=("days_in_stage", "mean"),
            max_days=("days_in_stage", "max"),
            opportunities=("opportunity", "count")
        )
    )

    ageing["stage"] = pd.Categorical(
        ageing["stage"],
        categories=STAGE_ORDER,
        ordered=True
    )

    ageing = ageing.sort_values("stage")

    fig_ageing = px.bar(
        ageing,
        x="stage",
        y="avg_days",
        category_orders={"stage": STAGE_ORDER},
        labels={
            "stage": "Pipeline Stage",
            "avg_days": "Average Days in Stage"
        }
    )

    fig_ageing.update_traces(
        marker_color=SOFT_ORANGE
    )

    style_chart(fig_ageing)

    st.plotly_chart(
        fig_ageing,
        use_container_width=True
    )

    # --------------------------------------------------
    # PIPELINE RISK
    # --------------------------------------------------

    st.divider()
    st.subheader("Pipeline Risk & Attention")

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Stalled Opportunities",
        f"{len(stalled)}"
    )

    r2.metric(
        "Weighted Value at Attention",
        euro_k(stalled_weighted)
    )

    if weighted_pipeline > 0:
        stalled_share = (
            stalled_weighted
            / weighted_pipeline
            * 100
        )
    else:
        stalled_share = 0

    r3.metric(
        "Share of Weighted Pipeline",
        f"{stalled_share:.1f}%"
    )

    if not stalled.empty:

        attention = stalled[
            [
                "opportunity",
                "market",
                "stage",
                "deal_value",
                "weighted_value",
                "days_in_stage"
            ]
        ].copy()

        attention = attention.sort_values(
            "weighted_value",
            ascending=False
        )

        attention.columns = [
            "Opportunity",
            "Market",
            "Stage",
            "Deal Value (€)",
            "Weighted Value (€)",
            "Days in Stage"
        ]

        st.dataframe(
            attention,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No active opportunities currently exceed "
            "the 30-day attention threshold."
        )

    # --------------------------------------------------
    # CONCENTRATION
    # --------------------------------------------------

    st.divider()
    st.subheader("Concentration Risk")

    market_concentration = (
        active
        .groupby("market", as_index=False)["weighted_value"]
        .sum()
        .sort_values("weighted_value", ascending=False)
    )

    if not market_concentration.empty:

        total_active_weighted = (
            market_concentration["weighted_value"].sum()
        )

        top_market = market_concentration.iloc[0]["market"]
        top_market_value = market_concentration.iloc[0]["weighted_value"]

        if total_active_weighted > 0:
            top_market_share = (
                top_market_value
                / total_active_weighted
                * 100
            )
        else:
            top_market_share = 0

        largest_deal = active.sort_values(
            "weighted_value",
            ascending=False
        ).iloc[0]

        largest_deal_share = (
            largest_deal["weighted_value"]
            / total_active_weighted
            * 100
            if total_active_weighted > 0
            else 0
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Largest Market Exposure",
            f"{top_market_share:.1f}%",
            top_market
        )

        c2.metric(
            "Largest Deal Exposure",
            f"{largest_deal_share:.1f}%",
            largest_deal["opportunity"]
        )

        fig_concentration = px.bar(
            market_concentration,
            x="market",
            y="weighted_value",
            labels={
                "market": "Market",
                "weighted_value": "Weighted Pipeline (€)"
            }
        )

        fig_concentration.update_traces(
            marker_color=MUTED_ORANGE
        )

        style_chart(fig_concentration)

        st.plotly_chart(
            fig_concentration,
            use_container_width=True
        )

    # --------------------------------------------------
    # QUARTER VIEW
    # --------------------------------------------------

    st.divider()
    st.subheader("Pipeline by Commercial Quarter")

    quarter_summary = (
        filtered
        .groupby("quarter", as_index=False)
        .agg(
            pipeline_value=("deal_value", "sum"),
            weighted_value=("weighted_value", "sum"),
            opportunities=("opportunity", "count")
        )
    )

    st.dataframe(
        quarter_summary.rename(
            columns={
                "quarter": "Quarter",
                "pipeline_value": "Pipeline Value (€)",
                "weighted_value": "Weighted Value (€)",
                "opportunities": "Opportunities"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # CCO DECISION SUPPORT
    # --------------------------------------------------

    st.divider()
    st.subheader("CCO Decision Support")

    if not stalled.empty:

        highest_risk = stalled.sort_values(
            "weighted_value",
            ascending=False
        ).iloc[0]

        st.markdown(
            f"""
### Commercial signal

**{len(stalled)} active opportunities** are currently above the
30-day attention threshold, representing **{euro_k(stalled_weighted)}**
in weighted pipeline.

The largest weighted exposure among these opportunities is
**{highest_risk["opportunity"]}** in **{highest_risk["market"]}**,
currently at the **{highest_risk["stage"]}** stage.

### Recommended CCO action

Prioritize the stalled late-stage opportunities by weighted value rather
than treating every open opportunity equally.

For the next pipeline review:

- validate the probability assigned to each material opportunity;
- identify the commercial, technical, or customer-side blocker;
- assign one accountable owner;
- define the next customer action and expected timing;
- remove or reweight opportunities that no longer support the forecast.
"""
        )

    else:

        st.markdown(
            """
### Commercial signal

No active opportunity currently exceeds the 30-day attention threshold.

### Recommended CCO action

Maintain stage-ageing discipline and focus the pipeline review on the
largest weighted opportunities and upcoming commercial milestones.
"""
        )

    st.info(
        "Analytical note: conversion rates and historical sales-cycle "
        "velocity are intentionally not calculated because the synthetic "
        "dataset represents a current pipeline snapshot rather than "
        "historical opportunity movements."
    )

    footer()


# ==================================================
# PLACEHOLDER PAGES
# ==================================================

def market_expansion():

    page_header(
        "Market Expansion",
        "Market prioritization • Strategic trade-offs • Resource allocation"
    )

    case_disclaimer()

    st.markdown(
        """
This framework explores a management question:

**If commercial resources are limited, which market should receive the next
increment of expansion effort?**
"""
    )

    st.caption(
        "Market scores are illustrative strategic assumptions on a 1–10 scale. "
        "They are not estimates of suena energy's actual market position or "
        "internal expansion priorities."
    )

    # --------------------------------------------------
    # WEIGHT CONTROLS
    # --------------------------------------------------

    st.divider()
    st.subheader("Strategic Assumptions")

    st.markdown(
        """
Adjust the relative importance of each criterion. The model automatically
normalizes the selected weights to 100%.
"""
    )

    w1, w2, w3, w4, w5 = st.columns(5)

    with w1:
        opportunity_weight = st.slider(
            "Market Opportunity",
            min_value=0,
            max_value=50,
            value=30,
            step=5
        )

    with w2:
        revenue_weight = st.slider(
            "Revenue Potential",
            min_value=0,
            max_value=50,
            value=25,
            step=5
        )

    with w3:
        accessibility_weight = st.slider(
            "Market Accessibility",
            min_value=0,
            max_value=50,
            value=20,
            step=5
        )

    with w4:
        competition_weight = st.slider(
            "Competitive Position",
            min_value=0,
            max_value=50,
            value=15,
            step=5
        )

    with w5:
        execution_weight = st.slider(
            "Execution Simplicity",
            min_value=0,
            max_value=50,
            value=10,
            step=5
        )

    raw_total = (
        opportunity_weight
        + revenue_weight
        + accessibility_weight
        + competition_weight
        + execution_weight
    )

    if raw_total == 0:
        st.warning(
            "At least one criterion must have a weight greater than zero."
        )
        footer()
        return

    weights = {
        "market_opportunity": opportunity_weight / raw_total,
        "revenue_potential": revenue_weight / raw_total,
        "market_accessibility": accessibility_weight / raw_total,
        "competitive_position": competition_weight / raw_total,
        "execution_simplicity": execution_weight / raw_total
    }

    st.caption(
        f"Selected weights: {raw_total}% before normalization • "
        "Normalized automatically to 100% for scoring."
    )

    # --------------------------------------------------
    # PRIORITY SCORE
    # --------------------------------------------------

    scored = market_df.copy()

    scored["priority_score"] = (
        scored["market_opportunity"] * weights["market_opportunity"]
        + scored["revenue_potential"] * weights["revenue_potential"]
        + scored["market_accessibility"] * weights["market_accessibility"]
        + scored["competitive_position"] * weights["competitive_position"]
        + scored["execution_simplicity"] * weights["execution_simplicity"]
    )

    scored = scored.sort_values(
        "priority_score",
        ascending=False
    ).reset_index(drop=True)

    scored["rank"] = scored.index + 1

    # --------------------------------------------------
    # PRIORITIZATION
    # --------------------------------------------------

    st.divider()
    st.subheader("Market Prioritization")

    top_market = scored.iloc[0]
    second_market = scored.iloc[1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Priority Market",
        top_market["market"],
        f"{top_market['priority_score']:.2f} / 10"
    )

    c2.metric(
        "Second Priority",
        second_market["market"],
        f"{second_market['priority_score']:.2f} / 10"
    )

    score_gap = (
        top_market["priority_score"]
        - second_market["priority_score"]
    )

    c3.metric(
        "Top-Two Score Gap",
        f"{score_gap:.2f}",
        "priority points"
    )

    # --------------------------------------------------
    # PRIORITY CHART
    # --------------------------------------------------

    fig_priority = px.bar(
        scored.sort_values("priority_score"),
        x="priority_score",
        y="market",
        orientation="h",
        text="priority_score",
        labels={
            "priority_score": "Priority Score",
            "market": "Market"
        }
    )

    fig_priority.update_traces(
        marker_color=SOFT_ORANGE,
        texttemplate="%{text:.2f}",
        textposition="outside"
    )

    fig_priority.update_layout(
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        showlegend=False,
        margin=dict(
            l=20,
            r=60,
            t=20,
            b=20
        ),
        xaxis=dict(
            range=[0, 10],
            gridcolor=BORDER,
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False
        )
    )

    st.plotly_chart(
        fig_priority,
        use_container_width=True
    )

    # --------------------------------------------------
    # SCORECARD
    # --------------------------------------------------

    st.subheader("Market Scorecard")

    scorecard = scored[
        [
            "rank",
            "market",
            "market_opportunity",
            "revenue_potential",
            "market_accessibility",
            "competitive_position",
            "execution_simplicity",
            "priority_score"
        ]
    ].copy()

    scorecard.columns = [
        "Rank",
        "Market",
        "Market Opportunity",
        "Revenue Potential",
        "Market Accessibility",
        "Competitive Position",
        "Execution Simplicity",
        "Priority Score"
    ]

    scorecard["Priority Score"] = (
        scorecard["Priority Score"].round(2)
    )

    st.dataframe(
        scorecard,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # PIPELINE ALIGNMENT
    # --------------------------------------------------

    st.divider()
    st.subheader("Strategy vs. Current Pipeline")

    st.caption(
        "This view combines the illustrative prioritization framework with "
        "the synthetic commercial pipeline to test whether current commercial "
        "exposure is aligned with the selected strategic priorities."
    )

    pipeline_market = (
        df[df["stage"] != "Won"]
        .groupby("market", as_index=False)
        .agg(
            active_pipeline=("deal_value", "sum"),
            weighted_pipeline=("weighted_value", "sum"),
            opportunities=("opportunity", "count")
        )
    )

    alignment = scored.merge(
        pipeline_market,
        on="market",
        how="left"
    )

    alignment[
        [
            "active_pipeline",
            "weighted_pipeline",
            "opportunities"
        ]
    ] = alignment[
        [
            "active_pipeline",
            "weighted_pipeline",
            "opportunities"
        ]
    ].fillna(0)

    total_active_pipeline = alignment["active_pipeline"].sum()

    if total_active_pipeline > 0:
        alignment["pipeline_share"] = (
            alignment["active_pipeline"]
            / total_active_pipeline
            * 100
        )
    else:
        alignment["pipeline_share"] = 0

    alignment_display = alignment[
        [
            "market",
            "priority_score",
            "active_pipeline",
            "weighted_pipeline",
            "pipeline_share",
            "opportunities"
        ]
    ].copy()

    alignment_display.columns = [
        "Market",
        "Priority Score",
        "Active Pipeline (€)",
        "Weighted Pipeline (€)",
        "Pipeline Share (%)",
        "Active Opportunities"
    ]

    alignment_display["Priority Score"] = (
        alignment_display["Priority Score"].round(2)
    )

    alignment_display["Pipeline Share (%)"] = (
        alignment_display["Pipeline Share (%)"].round(1)
    )

    st.dataframe(
        alignment_display,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # STRATEGIC INTERPRETATION
    # --------------------------------------------------

    st.divider()
    st.subheader("Strategic Interpretation")

    top_pipeline_market = (
        alignment
        .sort_values(
            "active_pipeline",
            ascending=False
        )
        .iloc[0]
    )

    same_market = (
        top_market["market"]
        == top_pipeline_market["market"]
    )

    if same_market:

        alignment_message = (
            f"The highest-priority market, **{top_market['market']}**, "
            "also has the largest active pipeline in the synthetic dataset. "
            "Under the current assumptions, commercial exposure and strategic "
            "priority are directionally aligned."
        )

    else:

        alignment_message = (
            f"The model currently ranks **{top_market['market']}** first, "
            f"while **{top_pipeline_market['market']}** has the largest active "
            "pipeline. This creates a resource-allocation question: whether to "
            "reinforce the strongest existing pipeline or increase effort in "
            "the market with the higher strategic score."
        )

    st.markdown(alignment_message)

    if score_gap < 0.5:

        st.warning(
            "The top-two markets are closely ranked. The recommendation is "
            "therefore sensitive to assumptions and should not be treated "
            "as a high-confidence market-selection decision."
        )

    else:

        st.info(
            "The current scoring model shows a clearer separation between "
            "the first- and second-ranked markets, although the result still "
            "depends on the illustrative assumptions."
        )

    # --------------------------------------------------
    # MANAGEMENT RECOMMENDATION
    # --------------------------------------------------

    st.subheader("Management Recommendation")

    st.markdown(
        f"""
Under the current weighting assumptions, **{top_market["market"]}** should
receive the next increment of expansion attention.

This does **not** imply an all-in market-entry decision. A more disciplined
next step would be to validate the assumptions driving the score before
committing additional commercial resources.

**Recommended validation questions**

- Is the addressable commercial opportunity materially larger than in the
  alternative markets?
- Does the current pipeline provide enough evidence of customer demand?
- What regulatory, technical, or partnership dependencies could slow execution?
- Is the commercial team positioned to convert additional market attention
  into qualified opportunities?
- Would reallocating resources create material risk in an already-strong market?
"""
    )

    # --------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------

    with st.expander("Methodology & limitations"):

        st.markdown(
            """
**Scoring methodology**

Each market receives an illustrative score from 1 to 10 across five criteria.
The user-selected weights are normalized to 100%, and the priority score is
calculated as a weighted average.

**Important limitation**

The market scores are assumptions created for this portfolio case. They are
not based on suena energy's internal strategy, confidential market research,
or proprietary commercial information.

The purpose of the model is to demonstrate a transparent decision framework:
how assumptions can be structured, challenged, reweighted, and connected to
commercial pipeline information before a management decision is made.
"""
        )

    footer()


def scenario_analysis():

    page_header(
        "Scenario Analysis",
        "Downside • Base case • Upside • Revenue sensitivity"
    )

    st.info(
        "Scenario Analysis will be developed in Step 8."
    )

    footer()


def board_brief():

    page_header(
        "Board Brief",
        "Executive KPIs • Commercial developments • Risks • Decisions required"
    )

    st.info(
        "Board-ready reporting will be developed in Step 9."
    )

    footer()


def about_case():

    page_header(
        "About This Case",
        "Background • Transferable experience • Analytical approach"
    )

    st.info(
        "The case-study narrative will be developed in Step 10."
    )

    footer()


# ==================================================
# PAGE ROUTER
# ==================================================

if page == "Executive Overview":
    executive_overview()

elif page == "Revenue & Pipeline":
    revenue_pipeline()

elif page == "Market Expansion":
    market_expansion()

elif page == "Scenario Analysis":
    scenario_analysis()

elif page == "Board Brief":
    board_brief()

elif page == "About This Case":
    about_case()
