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
        "Revenue sensitivity • Target coverage • Pipeline requirements • Decision support"
    )

    case_disclaimer()

    st.markdown(
        """
This model explores a management question:

**How resilient is the current commercial pipeline under different assumptions,
and what additional pipeline would be required to support a revenue target?**
"""
    )

    st.caption(
        "All targets and scenario assumptions are illustrative. "
        "They do not represent suena energy's actual revenue targets, "
        "forecast methodology, or internal commercial expectations."
    )

    # --------------------------------------------------
    # CURRENT PIPELINE BASELINE
    # --------------------------------------------------

    active = df[
        df["stage"] != "Won"
    ].copy()

    current_pipeline = active["deal_value"].sum()
    current_weighted = active["weighted_value"].sum()

    avg_probability = (
        active["probability"].mean()
        if not active.empty
        else 0
    )

    avg_deal = (
        active["deal_value"].mean()
        if not active.empty
        else 0
    )

    # --------------------------------------------------
    # MODEL ASSUMPTIONS
    # --------------------------------------------------

    st.divider()
    st.subheader("Scenario Assumptions")

    st.markdown(
        """
Adjust the target and commercial assumptions below to test how changes in
pipeline creation and probability affect expected revenue coverage.
"""
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        revenue_target = st.number_input(
            "Illustrative Revenue Target (€)",
            min_value=500000,
            max_value=10000000,
            value=3000000,
            step=100000
        )

    with a2:
        pipeline_growth = st.slider(
            "Base Pipeline Growth (%)",
            min_value=-30,
            max_value=100,
            value=10,
            step=5
        )

    with a3:
        probability_adjustment = st.slider(
            "Base Probability Adjustment (pp)",
            min_value=-20,
            max_value=20,
            value=0,
            step=5
        )

    st.caption(
        "Probability adjustments are expressed in percentage points (pp), "
        "not percentage growth."
    )

    # --------------------------------------------------
    # SCENARIO DEFINITIONS
    # --------------------------------------------------

    scenarios = pd.DataFrame(
        {
            "Scenario": [
                "Downside",
                "Base Case",
                "Upside"
            ],
            "Pipeline Growth (%)": [
                pipeline_growth - 15,
                pipeline_growth,
                pipeline_growth + 20
            ],
            "Probability Adjustment (pp)": [
                probability_adjustment - 10,
                probability_adjustment,
                probability_adjustment + 10
            ]
        }
    )

    # --------------------------------------------------
    # SCENARIO CALCULATIONS
    # --------------------------------------------------

    scenario_results = []

    for _, row in scenarios.iterrows():

        growth_factor = (
            1 + row["Pipeline Growth (%)"] / 100
        )

        adjusted_pipeline = (
            current_pipeline * growth_factor
        )

        adjusted_probability = (
            avg_probability
            + row["Probability Adjustment (pp)"] / 100
        )

        adjusted_probability = max(
            0,
            min(
                adjusted_probability,
                1
            )
        )

        projected_weighted_revenue = (
            adjusted_pipeline
            * adjusted_probability
        )

        revenue_gap = (
            projected_weighted_revenue
            - revenue_target
        )

        target_coverage = (
            projected_weighted_revenue
            / revenue_target
            * 100
            if revenue_target > 0
            else 0
        )

        additional_weighted_required = max(
            0,
            revenue_target
            - projected_weighted_revenue
        )

        if adjusted_probability > 0:
            additional_gross_pipeline = (
                additional_weighted_required
                / adjusted_probability
            )
        else:
            additional_gross_pipeline = 0

        scenario_results.append(
            {
                "Scenario": row["Scenario"],
                "Pipeline Growth (%)": row["Pipeline Growth (%)"],
                "Probability Adjustment (pp)": row[
                    "Probability Adjustment (pp)"
                ],
                "Adjusted Pipeline": adjusted_pipeline,
                "Adjusted Probability": adjusted_probability,
                "Projected Weighted Revenue": projected_weighted_revenue,
                "Revenue Gap": revenue_gap,
                "Target Coverage": target_coverage,
                "Additional Pipeline Required": additional_gross_pipeline
            }
        )

    results = pd.DataFrame(
        scenario_results
    )

    # --------------------------------------------------
    # BASELINE
    # --------------------------------------------------

    st.divider()
    st.subheader("Current Commercial Baseline")

    b1, b2, b3, b4 = st.columns(4)

    b1.metric(
        "Active Pipeline",
        euro_m(current_pipeline)
    )

    b2.metric(
        "Current Weighted Value",
        euro_m(current_weighted)
    )

    b3.metric(
        "Average Probability",
        f"{avg_probability * 100:.1f}%"
    )

    b4.metric(
        "Average Deal Size",
        euro_k(avg_deal)
    )

    # --------------------------------------------------
    # SCENARIO OUTPUT
    # --------------------------------------------------

    st.divider()
    st.subheader("Scenario Outcomes")

    downside = results[
        results["Scenario"] == "Downside"
    ].iloc[0]

    base = results[
        results["Scenario"] == "Base Case"
    ].iloc[0]

    upside = results[
        results["Scenario"] == "Upside"
    ].iloc[0]

    s1, s2, s3 = st.columns(3)

    with s1:

        st.markdown("### Downside")

        st.metric(
            "Projected Weighted Revenue",
            euro_m(
                downside[
                    "Projected Weighted Revenue"
                ]
            )
        )

        st.metric(
            "Target Coverage",
            f"{downside['Target Coverage']:.1f}%"
        )

    with s2:

        st.markdown("### Base Case")

        st.metric(
            "Projected Weighted Revenue",
            euro_m(
                base[
                    "Projected Weighted Revenue"
                ]
            )
        )

        st.metric(
            "Target Coverage",
            f"{base['Target Coverage']:.1f}%"
        )

    with s3:

        st.markdown("### Upside")

        st.metric(
            "Projected Weighted Revenue",
            euro_m(
                upside[
                    "Projected Weighted Revenue"
                ]
            )
        )

        st.metric(
            "Target Coverage",
            f"{upside['Target Coverage']:.1f}%"
        )

    # --------------------------------------------------
    # TARGET COVERAGE CHART
    # --------------------------------------------------

    st.subheader("Revenue Target Coverage")

    coverage_chart = results.copy()

    fig_coverage = px.bar(
        coverage_chart,
        x="Scenario",
        y="Target Coverage",
        text="Target Coverage",
        category_orders={
            "Scenario": [
                "Downside",
                "Base Case",
                "Upside"
            ]
        },
        labels={
            "Target Coverage": "Target Coverage (%)"
        }
    )

    fig_coverage.update_traces(
        marker_color=SOFT_ORANGE,
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig_coverage.update_layout(
        paper_bgcolor=CHARCOAL,
        plot_bgcolor=CHARCOAL,
        font_color=OFF_WHITE,
        showlegend=False,
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        yaxis=dict(
            gridcolor=BORDER,
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False
        )
    )

    st.plotly_chart(
        fig_coverage,
        use_container_width=True
    )

    # --------------------------------------------------
    # TARGET GAP
    # --------------------------------------------------

    st.divider()
    st.subheader("Target Gap & Pipeline Requirement")

    target_table = results[
        [
            "Scenario",
            "Projected Weighted Revenue",
            "Revenue Gap",
            "Target Coverage",
            "Additional Pipeline Required"
        ]
    ].copy()

    target_table[
        "Projected Weighted Revenue"
    ] = target_table[
        "Projected Weighted Revenue"
    ].round(0)

    target_table[
        "Revenue Gap"
    ] = target_table[
        "Revenue Gap"
    ].round(0)

    target_table[
        "Target Coverage"
    ] = target_table[
        "Target Coverage"
    ].round(1)

    target_table[
        "Additional Pipeline Required"
    ] = target_table[
        "Additional Pipeline Required"
    ].round(0)

    target_table.columns = [
        "Scenario",
        "Projected Weighted Revenue (€)",
        "Gap vs Target (€)",
        "Target Coverage (%)",
        "Additional Gross Pipeline Required (€)"
    ]

    st.dataframe(
        target_table,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # BASE CASE MANAGEMENT VIEW
    # --------------------------------------------------

    st.divider()
    st.subheader("Base Case Decision Support")

    base_revenue = base[
        "Projected Weighted Revenue"
    ]

    base_gap = base[
        "Revenue Gap"
    ]

    base_coverage = base[
        "Target Coverage"
    ]

    base_additional_pipeline = base[
        "Additional Pipeline Required"
    ]

    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Projected Revenue",
        euro_m(base_revenue)
    )

    d2.metric(
        "Gap vs Target",
        (
            f"+{euro_k(base_gap)}"
            if base_gap >= 0
            else f"-{euro_k(abs(base_gap))}"
        )
    )

    d3.metric(
        "Additional Pipeline Needed",
        (
            euro_m(base_additional_pipeline)
            if base_additional_pipeline > 0
            else "€0"
        )
    )

    # --------------------------------------------------
    # MANAGEMENT INTERPRETATION
    # --------------------------------------------------

    st.subheader("Management Interpretation")

    if base_coverage >= 100:

        st.success(
            f"Under the current Base Case assumptions, projected weighted "
            f"revenue covers approximately {base_coverage:.1f}% of the "
            "illustrative target."
        )

        st.markdown(
            """
**Management implication**

The target appears supported under the Base Case assumptions. The priority
should therefore shift from pure pipeline creation toward protecting the
quality and progression of the existing pipeline.

Recommended focus:

- validate probability assumptions on the largest opportunities;
- protect late-stage opportunities from slippage;
- monitor concentration risk by market and deal;
- maintain pipeline creation as protection against downside.
"""
        )

    else:

        st.warning(
            f"Under the current Base Case assumptions, projected weighted "
            f"revenue covers approximately {base_coverage:.1f}% of the "
            "illustrative target."
        )

        st.markdown(
            f"""
**Management implication**

The current Base Case does not fully support the illustrative target.

At the current adjusted probability, approximately
**{euro_m(base_additional_pipeline)} in additional gross pipeline**
would be required to close the expected revenue gap.

This creates three potential management levers:

1. **Pipeline creation** — generate additional qualified commercial opportunities.
2. **Pipeline progression** — improve the expected value of existing opportunities.
3. **Target / forecast reassessment** — test whether the assumptions supporting
   the commercial plan remain realistic.
"""
        )

    # --------------------------------------------------
    # SENSITIVITY
    # --------------------------------------------------

    st.divider()
    st.subheader("Sensitivity View")

    st.markdown(
        """
The scenario model separates two commercial levers:

**Pipeline volume** determines how much gross commercial opportunity exists.

**Probability** determines how much of that pipeline contributes to expected
weighted revenue.

This distinction matters because the same revenue gap can require different
management actions depending on whether the underlying issue is insufficient
pipeline creation or weak expected conversion.
"""
    )

    fig_sensitivity = px.scatter(
        results,
        x="Adjusted Pipeline",
        y="Projected Weighted Revenue",
        text="Scenario",
        size="Target Coverage",
        labels={
            "Adjusted Pipeline": "Adjusted Pipeline (€)",
            "Projected Weighted Revenue": "Projected Weighted Revenue (€)"
        }
    )

    fig_sensitivity.update_traces(
        marker=dict(
            color=SOFT_ORANGE,
            line=dict(
                color=BORDER,
                width=1
            )
        ),
        textposition="top center"
    )

    style_chart(
        fig_sensitivity
    )

    st.plotly_chart(
        fig_sensitivity,
        use_container_width=True
    )

    # --------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------

    with st.expander("Methodology & limitations"):

        st.markdown(
            """
**Model logic**

The scenario model begins with the  active pipeline and applies two changes:

1. a change in gross pipeline volume; and
2. an adjustment to the average pipeline probability.

Projected weighted revenue is then calculated as:

**Adjusted Pipeline × Adjusted Average Probability**

If projected weighted revenue is below the illustrative revenue target, the
model estimates the additional gross pipeline required at the scenario's
adjusted probability.

**Important limitation**

This is a simplified management scenario model, not a financial forecast.

A production revenue forecast would normally require opportunity-level timing,
historical conversion rates, sales-cycle behavior, contract economics, revenue
recognition assumptions, and other commercial information that is not
available in this synthetic case study.

The purpose here is to demonstrate structured scenario thinking 
rather than to reproduce suena energy's forecasting
methodology.
"""
        )

    footer()


def board_brief():

    page_header(
        "Board Brief",
        "Commercial performance • Key developments • Risks • Decisions required"
    )

    case_disclaimer()

    st.caption(
        "Illustrative one-page management brief designed to translate "
        "commercial pipeline data into board-level signals and decisions."
    )

    # --------------------------------------------------
    # COMMERCIAL BASELINE
    # --------------------------------------------------

    active = df[
        df["stage"] != "Won"
    ].copy()

    won = df[
        df["stage"] == "Won"
    ].copy()

    total_pipeline = active["deal_value"].sum()
    weighted_pipeline = active["weighted_value"].sum()
    active_opportunities = len(active)

    late_stage = active[
        active["stage"].isin(
            ["Proposal", "Negotiation"]
        )
    ].copy()

    late_stage_value = late_stage["deal_value"].sum()

    stalled = active[
        active["days_in_stage"] >= 30
    ].copy()

    stalled_weighted = stalled["weighted_value"].sum()

    # --------------------------------------------------
    # BOARD KPI STRIP
    # --------------------------------------------------

    st.divider()
    st.subheader("Commercial Snapshot")

    k1, k2, k3, k4 = st.columns(4)

    k1.metric(
        "Active Pipeline",
        euro_m(total_pipeline)
    )

    k2.metric(
        "Weighted Pipeline",
        euro_m(weighted_pipeline)
    )

    k3.metric(
        "Active Opportunities",
        f"{active_opportunities}"
    )

    k4.metric(
        "Late-Stage Pipeline",
        euro_m(late_stage_value)
    )

    # --------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------

    st.divider()
    st.subheader("Executive Summary")

    market_summary = (
        active
        .groupby("market", as_index=False)
        .agg(
            pipeline_value=("deal_value", "sum"),
            weighted_value=("weighted_value", "sum"),
            opportunities=("opportunity", "count")
        )
        .sort_values(
            "pipeline_value",
            ascending=False
        )
    )

    top_market = market_summary.iloc[0]

    largest_opportunity = (
        active
        .sort_values(
            "weighted_value",
            ascending=False
        )
        .iloc[0]
    )

    stalled_share = (
        stalled_weighted
        / weighted_pipeline
        * 100
        if weighted_pipeline > 0
        else 0
    )

    st.markdown(
        f"""
The synthetic commercial pipeline currently contains
**{euro_m(total_pipeline)} in active opportunity value**, representing
**{euro_m(weighted_pipeline)} on a probability-weighted basis**.

**{top_market["market"]}** is currently the largest market by active
pipeline value, while **{largest_opportunity["opportunity"]}** represents
the largest single weighted opportunity.

Pipeline quality requires attention: **{len(stalled)} opportunities**
have remained in their current stage for at least 30 days, representing
**{euro_k(stalled_weighted)}**, or approximately
**{stalled_share:.1f}% of weighted active pipeline**.
"""
    )

    # --------------------------------------------------
    # WHAT CHANGED / WHAT MATTERS
    # --------------------------------------------------

    st.divider()
    st.subheader("What Matters")

    left, right = st.columns(2)

    with left:

        st.markdown("### Commercial Strength")

        st.markdown(
            f"""
- **{euro_m(late_stage_value)}** of active pipeline is currently in
  Proposal or Negotiation.
- **{top_market["market"]}** represents the largest current source of
  commercial pipeline.
- The pipeline spans **{active["market"].nunique()} markets** and
  **{active["mw"].sum():,.0f} MW** of synthetic asset opportunities.
"""
        )

    with right:

        st.markdown("### Commercial Risk")

        if not stalled.empty:

            highest_stalled = (
                stalled
                .sort_values(
                    "weighted_value",
                    ascending=False
                )
                .iloc[0]
            )

            st.markdown(
                f"""
- **{len(stalled)} opportunities** exceed the 30-day stage-ageing threshold.
- **{euro_k(stalled_weighted)}** of weighted pipeline is currently
  associated with these opportunities.
- The largest stalled weighted exposure is
  **{highest_stalled["opportunity"]}** in
  **{highest_stalled["market"]}**.
"""
            )

        else:

            st.markdown(
                """
- No active opportunities currently exceed the 30-day attention threshold.
- Stage ageing does not currently represent a material synthetic pipeline signal.
"""
            )

    # --------------------------------------------------
    # MARKET EXPOSURE
    # --------------------------------------------------

    st.divider()
    st.subheader("Market Exposure")

    market_summary["pipeline_share"] = (
        market_summary["pipeline_value"]
        / total_pipeline
        * 100
        if total_pipeline > 0
        else 0
    )

    fig_board_market = px.bar(
        market_summary,
        x="market",
        y="weighted_value",
        text="pipeline_share",
        labels={
            "market": "Market",
            "weighted_value": "Weighted Pipeline (€)"
        }
    )

    fig_board_market.update_traces(
        marker_color=SOFT_ORANGE,
        texttemplate="%{text:.1f}% gross pipeline share",
        textposition="outside"
    )

    style_chart(
        fig_board_market
    )

    st.plotly_chart(
        fig_board_market,
        use_container_width=True
    )

    # --------------------------------------------------
    # KEY RISKS
    # --------------------------------------------------

    st.divider()
    st.subheader("Key Risks")

    top_market_share = (
        top_market["pipeline_value"]
        / total_pipeline
        * 100
        if total_pipeline > 0
        else 0
    )

    largest_deal_share = (
        largest_opportunity["weighted_value"]
        / weighted_pipeline
        * 100
        if weighted_pipeline > 0
        else 0
    )

    risk1, risk2, risk3 = st.columns(3)

    risk1.metric(
        "Stage-Ageing Exposure",
        f"{stalled_share:.1f}%",
        "of weighted pipeline"
    )

    risk2.metric(
        "Largest Market Share",
        f"{top_market_share:.1f}%",
        top_market["market"]
    )

    risk3.metric(
        "Largest Deal Exposure",
        f"{largest_deal_share:.1f}%",
        largest_opportunity["opportunity"]
    )

    # --------------------------------------------------
    # BOARD DECISIONS
    # --------------------------------------------------

    st.divider()
    st.subheader("Decisions Required")

    st.markdown(
        f"""
### 1. Pipeline quality

Should management continue to carry the current probabilities on opportunities
that have remained in stage for 30+ days, or should selected opportunities be
reweighted?

**Why it matters:** {euro_k(stalled_weighted)} of weighted pipeline is
currently associated with the stage-ageing attention group.

### 2. Commercial resource allocation

Should additional commercial effort reinforce **{top_market["market"]}**,
where current pipeline exposure is strongest, or be directed toward markets
with lower current pipeline concentration?

**Why it matters:** resource allocation affects both near-term pipeline
progression and longer-term market diversification.

### 3. Forecast protection

Is the current late-stage pipeline sufficient to support commercial
expectations, or should management increase pipeline-generation activity as
downside protection?

**Why it matters:** Proposal and Negotiation currently represent
{euro_m(late_stage_value)} of active gross pipeline.
"""
    )

    # --------------------------------------------------
    # MANAGEMENT ACTIONS
    # --------------------------------------------------

    st.divider()
    st.subheader("Management Actions")

    st.markdown(
        """
**Before the next board update:**

1. Review all opportunities above the 30-day stage-ageing threshold.
2. Validate probability and next-action assumptions on material late-stage deals.
3. Confirm the commercial rationale for market-level resource allocation.
4. Run downside and upside scenarios against the current commercial target.
5. Escalate only the risks and decisions that require executive intervention.
"""
    )

    # --------------------------------------------------
    # BOARD NOTE
    # --------------------------------------------------

    st.markdown(
        f"""
        <div style="
            background-color: {GRAPHITE};
            border: 1px solid {BORDER};
            border-left: 4px solid {SOFT_ORANGE};
            padding: 20px 22px;
            border-radius: 8px;
            margin-top: 30px;
            margin-bottom: 20px;
        ">
            <div style="
                color: {SOFT_ORANGE};
                font-weight: 700;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 10px;
            ">
                Board-level takeaway
            </div>
            <div style="
                color: {OFF_WHITE};
                font-size: 1.05rem;
                line-height: 1.6;
            ">
                Commercial opportunity remains meaningful, but management
                attention should focus on pipeline quality rather than gross
                pipeline volume alone. Stage ageing, probability discipline,
                concentration exposure, and market-level resource allocation
                are the primary decision areas surfaced by this synthetic case.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------

    with st.expander("Board brief methodology & limitations"):

        st.markdown(
            """
This page intentionally prioritizes management signals.

It uses the same synthetic pipeline dataset as the Revenue & Pipeline view,
but reduces the information to:

- headline commercial KPIs;
- material developments;
- concentration and stage-ageing risks;
- management decisions;
- immediate actions.

It does not represent an actual suena energy board report. No internal company
targets, financial information, board materials, or confidential commercial
data are used.

A real board report would also require information and targets that are not available
in this independent case study.
"""
        )

    footer()


def about_case():

    page_header(
        "About This Case",
        "Why I built it • Transferable experience • How I approach Strategy & Operations"
    )

    # --------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------

    st.markdown(
    f"""
<div style="background-color:{GRAPHITE}; border:1px solid {BORDER}; border-left:4px solid {SOFT_ORANGE}; padding:24px 26px; border-radius:8px; margin:20px 0 32px 0;">
<div style="color:{SOFT_ORANGE}; font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px;">WHY I BUILT THIS</div>
<div style="color:{OFF_WHITE}; font-size:1.12rem; line-height:1.7;">
My professional background is not in energy (yet). I have worked in international commodity-market and commercial environments, supporting price fixation, contracts, inventory positions, customer operations, reporting, and cross-functional execution.<br><br>
Across those roles, I often found myself solving a similar problem which is taking commercial and operational information from different places and turning it into something people could actually work with data, dashboards, and next steps.<br><br>
I built this case to see how I could bring that experience into the Strategy & Operations challenges of a growing energy-tech company.
</div>
</div>
""",
    unsafe_allow_html=True
)

    # --------------------------------------------------
    # BACKGROUND
    # --------------------------------------------------

    st.subheader("From Commodity Markets to Energy Tech")

    st.markdown(
        """
My experience includes commercial and operational work in international
**coffee commodity markets**, where I supported activities including
**price fixation, contract execution, inventory positions, supplier and
customer coordination, and performance reporting**.

That experience does not make me an energy trader, and this project is not
intended to suggest otherwise.

What it does provide is familiarity with environments where commercial
decisions are connected to **market-driven pricing, contracts, operational
execution, data quality, and timing**.

"""
    )

    # --------------------------------------------------
    # TRANSFERABLE EXPERIENCE
    # --------------------------------------------------

    st.divider()
    st.subheader("What I Bring")

    c1, c2 = st.columns(2)

    with c1:

        st.markdown("### Commercial Operations")

        st.markdown(
            """
My previous roles have involved coordinating commercial execution across
customers, suppliers, sales teams, finance, operations, and technology.

This taught me to understand how information,
ownership, timing, and process design affect commercial outcomes.
"""
        )

        st.markdown("### Data & Reporting")

        st.markdown(
            """
I have built and used dashboards and automated reporting to improve visibility
and helping identify a problem, prioritize an action, or make a better
decision.
"""
        )

    with c2:

        st.markdown("### Commodity-Market Exposure")

        st.markdown(
            """
Working with coffee commodities gave me practical exposure to price fixation,
contracts, inventory requirements, international counterparties, and
market-dependent commercial execution.

I see this as a useful foundation for learning a new market context.
"""
        )

        st.markdown("### Cross-Functional Execution")

        st.markdown(
            """
Much of my work has happened between functions rather than inside a single
functional silo.

I am comfortable structuring ambiguous work, coordinating stakeholders,
tracking dependencies, and translating operational detail into information
that commercial teams can act on.
"""
        )

    # --------------------------------------------------
    # PROJECT CAPABILITIES
    # --------------------------------------------------

    st.divider()
    st.subheader("What This Case Demonstrates")

    st.markdown(
        """
Rather than creating a technical energy-trading simulation, I focused this
case on the Strategy & Operations problems I could approach credibly from
day one.
"""
    )

    d1, d2 = st.columns(2)

    with d1:

        st.markdown(
            f"""
            <div style="
                background-color: {GRAPHITE};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 16px;
            ">
                <div style="color:{SOFT_ORANGE}; font-weight:700;">
                    01 — Revenue Operations
                </div>
                <div style="color:{MUTED_TEXT}; margin-top:8px; line-height:1.6;">
                    Structuring pipeline information, identifying stage ageing,
                    weighted exposure, concentration risk, and commercial
                    priorities.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background-color: {GRAPHITE};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 16px;
            ">
                <div style="color:{SOFT_ORANGE}; font-weight:700;">
                    02 — Market Expansion
                </div>
                <div style="color:{MUTED_TEXT}; margin-top:8px; line-height:1.6;">
                    Build a
                    prioritization model and connecting those priorities to
                    commercial pipeline exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with d2:

        st.markdown(
            f"""
            <div style="
                background-color: {GRAPHITE};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 16px;
            ">
                <div style="color:{SOFT_ORANGE}; font-weight:700;">
                    03 — Scenario Analysis
                </div>
                <div style="color:{MUTED_TEXT}; margin-top:8px; line-height:1.6;">
                    Testing commercial outcomes under changing assumptions and
                     identifying potential pipeline requirements.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background-color: {GRAPHITE};
                border: 1px solid {BORDER};
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 16px;
            ">
                <div style="color:{SOFT_ORANGE}; font-weight:700;">
                    04 — Executive Communication
                </div>
                <div style="color:{MUTED_TEXT}; margin-top:8px; line-height:1.6;">
                    Reducing detailed analysis into management signals, risks,
                    recommendations, and decisions suitable for an executive
                    or board-level conversation.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # ANALYTICAL PRINCIPLES
    # --------------------------------------------------

    st.divider()
    st.subheader("How I Approached the Analysis")

    st.markdown(
        """
A few principles guided the project:

**Be clear about what is assumed.**  
Since I don't have access to suena's internal data, I used synthetic data where needed and kept those assumptions visible throughout the case.

**Work with data.**  
The pipeline data is useful for looking at value, stage ageing, concentration, and current commercial exposure. I avoided adding metrics that would require historical data I don't have.

**Always ask: so what?**  
Each section tries to connect the analysis to a question, an action, or a decision.

**Keep the executive view simple.**  
The Board Brief is intentionally shorter than the analytical sections. The idea is to bring forward the few things that actually need management attention.
"""
    )

    # --------------------------------------------------
    # HOW THE CASE IS STRUCTURED
    # --------------------------------------------------

    st.divider()
    st.subheader("Case Structure")

    case_structure = pd.DataFrame(
        {
            "View": [
                "Executive Overview",
                "Revenue & Pipeline",
                "Market Expansion",
                "Scenario Analysis",
                "Board Brief"
            ],
            "Management Question": [
                "What requires the CCO's attention?",
                "Where is commercial value, risk, and pipeline friction?",
                "Where should the next increment of expansion effort go?",
                "How resilient is the commercial plan under changing assumptions?",
                "What should management communicate and decide?"
            ]
        }
    )

    st.dataframe(
        case_structure,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------
    # FINAL NOTE
    # --------------------------------------------------

    st.markdown(
        f"""
        <div style="
            margin-top: 40px;
            padding: 28px;
            text-align: center;
            border-top: 1px solid {BORDER};
            border-bottom: 1px solid {BORDER};
        ">

            <div style="
                color: {OFF_WHITE};
                font-size: 1.25rem;
                font-weight: 600;
                margin-bottom: 10px;
            ">
                Built by Xilene Siquero
            </div>

            <div style="
                color: {SOFT_ORANGE};
                font-size: 1rem;
                margin-bottom: 8px;
            ">
                Strategy & Operations Candidate
            </div>

            <div style="
                color: {MUTED_TEXT};
                font-size: 0.9rem;
            ">
                Hamburg • 2026
            </div>

        </div>
        """,
        unsafe_allow_html=True
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
