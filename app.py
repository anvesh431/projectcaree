import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="CareFlow | Hospital Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# BLUE + WHITE THEME (INCLUDES VISIBILITY FIXES)
# ============================================================
st.markdown("""
<style>
/* Page and header */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    background-color: #F5F9FF !important;
    color: #243B55 !important;
}
header[data-testid="stHeader"] {
    background-color: #F5F9FF !important;
}
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
    max-width: 1500px;
}

/* All ordinary text and section headings */
main [data-testid="stMarkdownContainer"] p,
main [data-testid="stCaptionContainer"] p,
main label p {
    color: #405672 !important;
}
h1, h2, h3, h4 {
    color: #123F85 !important;
    font-weight: 750 !important;
}
hr { border-color: #D7E5F6 !important; }

/* Sidebar: explicitly dark text on light background */
section[data-testid="stSidebar"] {
    background-color: #EAF3FF !important;
    border-right: 1px solid #D4E4F7 !important;
}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
    color: #193E70 !important;
}
section[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #17365D !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] [data-testid="stMetric"] {
    padding: 13px 15px !important;
    border-top: 3px solid #1976D2 !important;
}

/* KPI cards: fix faint/invisible labels */
div[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DCE8F8 !important;
    border-top: 4px solid #1976D2 !important;
    border-radius: 16px !important;
    padding: 20px 18px !important;
    box-shadow: 0 5px 20px rgba(22, 83, 160, 0.07);
}
div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] * {
    color: #465B74 !important;
    opacity: 1 !important;
    font-size: 14px !important;
    font-weight: 650 !important;
}
div[data-testid="stMetricValue"],
div[data-testid="stMetricValue"] * {
    color: #123F85 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

/* Plotly chart containers and tables */
div[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DFEAF8;
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 4px 14px rgba(22,83,160,0.04);
}
div[data-testid="stDataFrame"] {
    border: 1px solid #DCE8F8;
    border-radius: 12px;
    overflow: hidden;
}

/* Form widgets */
div[data-testid="stWidgetLabel"] p { color: #334E70 !important; }
.stSelectbox [data-baseweb="select"] > div,
.stTextInput [data-baseweb="input"] > div {
    background-color: #FFFFFF !important;
    color: #17365D !important;
    border-color: #D1E4FC !important;
}
.stSelectbox [data-baseweb="select"] span,
.stTextInput input { color: #17365D !important; }

/* Download buttons */
div[data-testid="stDownloadButton"] button {
    background: #1976D2 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
}
div[data-testid="stDownloadButton"] button * { color: #FFFFFF !important; }
div[data-testid="stDownloadButton"] button:hover {
    background: #0B4F9F !important;
}

/* Hero panel */
.careflow-hero {
    background: linear-gradient(115deg, #0B3D83, #1976D2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 22px;
    box-shadow: 0 8px 24px rgba(25, 118, 210, 0.13);
}
.careflow-hero h1 {
    margin: 0 0 10px 0 !important;
    color: #FFFFFF !important;
    font-size: 34px;
    line-height: 1.2;
}
.careflow-hero p {
    margin: 0 !important;
    color: #E3EFFF !important;
    font-size: 16px;
}
.careflow-footer {
    text-align: center;
    color: #60758E;
    padding: 10px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FILES AND DATA LOADING
# ============================================================
# Run from the project root (where app.py is saved).
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def read_csv(file_path):
    return pd.read_csv(file_path)


def required_csv(relative_path):
    file_path = BASE_DIR / relative_path
    if not file_path.exists():
        st.error(f"Required data file not found: {relative_path}")
        st.info("Generate dashboard CSV files using: python python/dashboard_data.py")
        st.stop()
    return read_csv(str(file_path))


summary = required_csv("data/dashboard/dashboard_summary.csv")
activity = required_csv("data/dashboard/activity_frequency.csv")
journey = required_csv("data/dashboard/patient_journey.csv")
bottleneck = required_csv("data/processed/bottleneck_analysis.csv")

if summary.empty:
    st.error("Dashboard summary CSV is empty.")
    st.stop()

kpi = summary.iloc[0]

# ============================================================
# CHARTS AND EXPORT HELPERS
# ============================================================
def style_chart(fig, height=400):
    fig.update_layout(
        height=height,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Arial", size=12, color="#334155"),
        title_font=dict(size=18, color="#123F85"),
        margin=dict(l=22, r=25, t=60, b=32),
        xaxis=dict(gridcolor="#E8F0FA", zerolinecolor="#E8F0FA"),
        yaxis=dict(gridcolor="#E8F0FA", zerolinecolor="#E8F0FA"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    return fig


def export_csv(df, filename):
    st.download_button(
        label="⬇️ Download CSV Report",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🏥 CareFlow")
    st.caption("Healthcare Intelligence Platform")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "📊 Overview",
            "🔄 Process Analytics",
            "🧑‍⚕️ Patient Journey",
            "✅ Conformance",
            "📁 Data Explorer",
        ],
    )

    st.divider()
    st.markdown("**Dataset Overview**")
    st.metric("Patients", int(kpi["Total_Patients"]))
    st.metric("Events", int(kpi["Total_Events"]))
    st.divider()
    st.caption("CareFlow • Hospital Operations Analytics")

# ============================================================
# COMMON HEADER
# ============================================================
st.markdown("""
<div class="careflow-hero">
    <h1>🏥 CareFlow Analytics</h1>
    <p>Clinical Pathway Process Mining • Hospital Performance • Patient Journey Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 1. OVERVIEW
# ============================================================
if page == "📊 Overview":
    st.subheader("📊 Hospital Performance Overview")
    st.caption("Key performance metrics derived from simulated hospital event logs")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Patients", int(kpi["Total_Patients"]))
    with col2:
        st.metric("Total Events", int(kpi["Total_Events"]))
    with col3:
        st.metric("Average Journey Time", f'{kpi["Average_Journey_Time"]:.1f} min')
    with col4:
        st.metric("Average Transition Time", f'{kpi["Average_Transition_Time"]:.2f} min')

    st.divider()
    st.subheader("🚨 Major Process Bottleneck")
    b1, b2 = st.columns([2, 1])
    with b1:
        st.metric("Biggest Bottleneck", str(kpi["Biggest_Bottleneck"]))
    with b2:
        st.metric("Average Bottleneck Time", f'{kpi["Bottleneck_Time"]:.1f} min')

    st.divider()
    st.subheader("📈 Analytics Overview")
    left, right = st.columns(2)
    with left:
        fig = px.bar(
            activity.sort_values("Frequency", ascending=True),
            x="Frequency",
            y="Activity_Name",
            orientation="h",
            title="Hospital Activity Frequency",
            labels={"Activity_Name": "Activity", "Frequency": "Events"},
            color_discrete_sequence=["#1976D2"],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

    with right:
        fig = px.histogram(
            journey,
            x="Journey_Time_Minutes",
            nbins=20,
            title="Patient Journey Duration Distribution",
            labels={"Journey_Time_Minutes": "Journey Time (min)"},
            color_discrete_sequence=["#42A5F5"],
        )
        st.plotly_chart(style_chart(fig), width="stretch")

# ============================================================
# 2. PROCESS ANALYTICS
# ============================================================
elif page == "🔄 Process Analytics":
    st.subheader("🔄 Process & Bottleneck Analysis")
    st.caption("Explore the transitions that contribute to patient delays")

    sorted_bottleneck = bottleneck.sort_values("Average_Time_Minutes", ascending=False)
    fig = px.bar(
        sorted_bottleneck,
        x="Average_Time_Minutes",
        y="Transition",
        orientation="h",
        color="Average_Time_Minutes",
        color_continuous_scale=["#CFE8FF", "#64B5F6", "#0D47A1"],
        title="Average Time per Patient Transition",
        labels={"Average_Time_Minutes": "Average Time (min)"},
    )
    fig.update_layout(
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(style_chart(fig, height=530), width="stretch")

    fig2 = px.bar(
        bottleneck.sort_values("Frequency", ascending=False),
        x="Transition",
        y="Frequency",
        title="Most Common Patient Transitions",
        color_discrete_sequence=["#1976D2"],
    )
    st.plotly_chart(style_chart(fig2), width="stretch")

    st.divider()
    st.subheader("🗺️ Clinical Pathway Process Map")
    process_map = BASE_DIR / "screenshots/careflow_process_map.png"
    if process_map.exists():
        st.image(
            str(process_map),
            caption="Discovered Directly-Follows Process Map",
            width="stretch",
        )
    else:
        st.warning("Process map image is missing in the screenshots folder.")

    st.subheader("Detailed Bottleneck Analysis")
    st.dataframe(sorted_bottleneck, width="stretch", hide_index=True)
    export_csv(sorted_bottleneck, "careflow_bottleneck_report.csv")

# ============================================================
# 3. PATIENT JOURNEY
# ============================================================
elif page == "🧑‍⚕️ Patient Journey":
    st.subheader("🧑‍⚕️ Patient Journey Intelligence")
    st.caption("Patient journey duration and case-wise exploration")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Average Journey", f'{journey["Journey_Time_Minutes"].mean():.1f} min')
    with c2:
        st.metric("Longest Journey", f'{journey["Journey_Time_Minutes"].max():.1f} min')
    with c3:
        st.metric("Shortest Journey", f'{journey["Journey_Time_Minutes"].min():.1f} min')

    st.divider()
    fig = px.histogram(
        journey,
        x="Journey_Time_Minutes",
        nbins=25,
        title="Patient Journey Time Distribution",
        labels={"Journey_Time_Minutes": "Time (minutes)"},
        color_discrete_sequence=["#1976D2"],
    )
    st.plotly_chart(style_chart(fig), width="stretch")

    st.subheader("🔎 Search Patient Journey")
    case_ids = sorted(journey["Case_ID"].dropna().astype(str).unique().tolist())
    selected_case = st.selectbox("Choose Patient Case ID", ["All Patients"] + case_ids)

    if selected_case == "All Patients":
        filtered = journey
    else:
        filtered = journey[journey["Case_ID"].astype(str) == selected_case]

    st.dataframe(filtered, width="stretch", hide_index=True)
    export_csv(filtered, "careflow_patient_journeys.csv")

# ============================================================
# 4. CONFORMANCE
# ============================================================
elif page == "✅ Conformance":
    st.subheader("✅ Clinical Pathway Conformance")
    st.caption("Compare actual case sequences with the project's ideal pathway")

    summary_path = BASE_DIR / "data/dashboard/conformance_summary.csv"
    results_path = BASE_DIR / "data/dashboard/conformance_results.csv"

    if summary_path.exists() and results_path.exists():
        conf_summary = read_csv(str(summary_path))
        conf_results = read_csv(str(results_path))

        if conf_summary.empty:
            st.warning("Conformance summary is empty. Re-run conformance_checking.py.")
        else:
            conf = conf_summary.iloc[0]
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric("Total Cases", int(conf["Total_Cases"]))
            with c2:
                st.metric("Compliant Cases", int(conf["Compliant_Cases"]))
            with c3:
                st.metric("Non-Compliant Cases", int(conf["Non_Compliant_Cases"]))
            with c4:
                st.metric("Compliance Rate", f'{conf["Compliance_Rate"]:.2f}%')

            st.divider()
            counts = conf_results["Status"].value_counts().rename_axis("Status").reset_index(name="Cases")
            fig = px.pie(
                counts,
                names="Status",
                values="Cases",
                hole=0.58,
                title="Clinical Pathway Compliance",
                color="Status",
                color_discrete_map={
                    "Compliant": "#1976D2",
                    "Non-Compliant": "#90CAF9",
                },
            )
            st.plotly_chart(style_chart(fig), width="stretch")

            st.subheader("Non-Compliant Patient Paths")
            non_compliant = conf_results[conf_results["Status"] == "Non-Compliant"]
            st.dataframe(non_compliant, width="stretch", hide_index=True)
            export_csv(non_compliant, "careflow_non_compliant_cases.csv")
    else:
        st.warning("Conformance CSV files are missing.")
        st.info("Run: python python/conformance_checking.py")

# ============================================================
# 5. DATA EXPLORER
# ============================================================
elif page == "📁 Data Explorer":
    st.subheader("📁 CareFlow Data Explorer")
    st.caption("View and export the processed dashboard datasets")

    datasets = {
        "Patient Journey": journey,
        "Activity Frequency": activity,
        "Bottleneck Analysis": bottleneck,
        "Dashboard Summary": summary,
    }
    dataset_name = st.selectbox("Choose Dataset", list(datasets.keys()))
    selected_df = datasets[dataset_name]

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Rows", len(selected_df))
    with c2:
        st.metric("Columns", len(selected_df.columns))

    st.dataframe(selected_df, width="stretch", hide_index=True)
    export_csv(selected_df, "careflow_data_export.csv")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    '<div class="careflow-footer">'
    '🏥 CareFlow • Clinical Pathway Process Mining | Healthcare Operations Analytics'
    '</div>',
    unsafe_allow_html=True,
)
