import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import os

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="CareFlow Dashboard",
    page_icon="🏥",
    layout="wide"
)

# -------------------------------------------------
# BLUE + LIGHT WHITE THEME
# -------------------------------------------------

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #F8FBFF 0%,
        #EEF6FF 50%,
        #FFFFFF 100%
    );
}

/* Main Content */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main Heading */
h1 {
    color: #0B3D91 !important;
    font-weight: 800 !important;
}

/* Section Headings */
h2, h3 {
    color: #1565C0 !important;
    font-weight: 700 !important;
}

/* Normal Text */
p {
    color: #334155;
}

/* KPI Cards */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #D6E8FF;
    border-left: 5px solid #1976D2;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0px 4px 14px rgba(30, 100, 180, 0.08);
}

/* KPI Label */
div[data-testid="stMetricLabel"] {
    color: #64748B;
    font-weight: 600;
}

/* KPI Value */
div[data-testid="stMetricValue"] {
    color: #0B3D91;
    font-weight: 800;
}

/* Dataframe */
div[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #D6E8FF;
    border-radius: 10px;
    padding: 5px;
}

/* Divider */
hr {
    border-color: #D6E8FF !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #EAF4FF;
}

/* Alert Box */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# CHART THEME FUNCTION
# -------------------------------------------------

def apply_chart_theme(fig):

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",

        font=dict(
            color="#334155"
        ),

        title_font=dict(
            color="#0B3D91",
            size=20
        ),

        xaxis=dict(
            gridcolor="#E5E7EB"
        ),

        yaxis=dict(
            gridcolor="#E5E7EB"
        ),

        margin=dict(
            l=30,
            r=30,
            t=60,
            b=30
        )
    )

    return fig


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🏥 CareFlow – Clinical Pathway Process Mining")

st.markdown(
    """
    <p style="
        font-size:18px;
        color:#64748B;
        margin-top:-10px;
    ">
    Hospital Patient Journey, Process Mining and Bottleneck Analytics
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

summary = pd.read_csv(
    "data/dashboard/dashboard_summary.csv"
)

activity = pd.read_csv(
    "data/dashboard/activity_frequency.csv"
)

journey = pd.read_csv(
    "data/dashboard/patient_journey.csv"
)

bottleneck = pd.read_csv(
    "data/processed/bottleneck_analysis.csv"
)

kpi = summary.iloc[0]


# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

st.subheader("📊 Hospital Performance Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Patients",
        int(kpi["Total_Patients"])
    )

with col2:

    st.metric(
        "Total Events",
        int(kpi["Total_Events"])
    )

with col3:

    st.metric(
        "Average Journey Time",
        f'{kpi["Average_Journey_Time"]:.1f} min'
    )

with col4:

    st.metric(
        "Average Transition Time",
        f'{kpi["Average_Transition_Time"]:.2f} min'
    )


# -------------------------------------------------
# BOTTLENECK KPI
# -------------------------------------------------

st.divider()

st.subheader("🚨 Major Process Bottleneck")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Biggest Bottleneck",
        kpi["Biggest_Bottleneck"]
    )

with col2:

    st.metric(
        "Average Bottleneck Time",
        f'{kpi["Bottleneck_Time"]:.1f} min'
    )


# -------------------------------------------------
# ACTIVITY FREQUENCY
# -------------------------------------------------

st.divider()

st.subheader("📈 Hospital Activity Analysis")

fig_activity = px.bar(
    activity,
    x="Activity_Name",
    y="Frequency",
    title="Hospital Activity Frequency",

    labels={
        "Activity_Name": "Hospital Activity",
        "Frequency": "Number of Events"
    },

    color_discrete_sequence=["#1976D2"]
)

fig_activity = apply_chart_theme(
    fig_activity
)

st.plotly_chart(
    fig_activity,
    use_container_width=True
)


# -------------------------------------------------
# BOTTLENECK ANALYSIS
# -------------------------------------------------

st.subheader("⏱️ Transition Bottleneck Analysis")

bottleneck_sorted = bottleneck.sort_values(
    "Average_Time_Minutes",
    ascending=False
)

fig_bottleneck = px.bar(
    bottleneck_sorted,
    x="Transition",
    y="Average_Time_Minutes",

    title="Average Transition Time",

    labels={
        "Transition": "Patient Transition",
        "Average_Time_Minutes":
            "Average Time (Minutes)"
    },

    color_discrete_sequence=["#42A5F5"]
)

fig_bottleneck = apply_chart_theme(
    fig_bottleneck
)

st.plotly_chart(
    fig_bottleneck,
    use_container_width=True
)


# -------------------------------------------------
# TRANSITION FREQUENCY
# -------------------------------------------------

st.subheader("🔄 Patient Transition Frequency")

fig_frequency = px.bar(

    bottleneck.sort_values(
        "Frequency",
        ascending=False
    ),

    x="Transition",
    y="Frequency",

    title="Most Common Patient Transitions",

    color_discrete_sequence=["#1565C0"]
)

fig_frequency = apply_chart_theme(
    fig_frequency
)

st.plotly_chart(
    fig_frequency,
    use_container_width=True
)


# -------------------------------------------------
# PATIENT JOURNEY ANALYSIS
# -------------------------------------------------

st.divider()

st.subheader("🧑‍⚕️ Patient Journey Analysis")

average_journey = journey[
    "Journey_Time_Minutes"
].mean()

maximum_journey = journey[
    "Journey_Time_Minutes"
].max()

minimum_journey = journey[
    "Journey_Time_Minutes"
].min()


col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Average Journey",
        f"{average_journey:.1f} min"
    )

with col2:

    st.metric(
        "Longest Journey",
        f"{maximum_journey:.1f} min"
    )

with col3:

    st.metric(
        "Shortest Journey",
        f"{minimum_journey:.1f} min"
    )


# -------------------------------------------------
# JOURNEY DISTRIBUTION
# -------------------------------------------------

fig_journey = px.histogram(

    journey,

    x="Journey_Time_Minutes",

    nbins=20,

    title="Patient Journey Time Distribution",

    labels={
        "Journey_Time_Minutes":
            "Journey Time (Minutes)"
    },

    color_discrete_sequence=["#2196F3"]
)

fig_journey = apply_chart_theme(
    fig_journey
)

st.plotly_chart(
    fig_journey,
    use_container_width=True
)


# -------------------------------------------------
# PROCESS MINING MAP
# -------------------------------------------------

st.divider()

st.subheader("🔄 Clinical Pathway Process Map")

process_map = (
    "screenshots/careflow_process_map.png"
)

if os.path.exists(process_map):

    image = Image.open(
        process_map
    )

    st.image(
        image,
        caption="CareFlow Directly-Follows Process Map",
        use_container_width=True
    )

else:

    st.warning(
        "Process map image was not found."
    )


# -------------------------------------------------
# BOTTLENECK TABLE
# -------------------------------------------------

st.divider()

st.subheader("📋 Detailed Bottleneck Analysis")

st.dataframe(
    bottleneck_sorted,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# PATIENT JOURNEY TABLE
# -------------------------------------------------

st.subheader("🏥 Patient Journey Details")

st.dataframe(
    journey,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# CONFORMANCE CHECKING
# -------------------------------------------------

st.divider()

st.subheader("✅ Clinical Pathway Conformance")


conformance_summary = pd.read_csv(
    "data/dashboard/conformance_summary.csv"
)

conformance_results = pd.read_csv(
    "data/dashboard/conformance_results.csv"
)

conf = conformance_summary.iloc[0]


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Cases",
        int(conf["Total_Cases"])
    )


with col2:

    st.metric(
        "Compliant Cases",
        int(conf["Compliant_Cases"])
    )


with col3:

    st.metric(
        "Non-Compliant Cases",
        int(conf["Non_Compliant_Cases"])
    )


with col4:

    st.metric(
        "Compliance Rate",
        f'{conf["Compliance_Rate"]:.2f}%'
    )


# -------------------------------------------------
# COMPLIANCE PIE CHART
# -------------------------------------------------

status_counts = (
    conformance_results["Status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Cases"
]


fig_conformance = px.pie(

    status_counts,

    names="Status",

    values="Cases",

    title="Clinical Pathway Compliance",

    color="Status",

    color_discrete_map={
        "Compliant": "#1976D2",
        "Non-Compliant": "#90CAF9"
    }
)


fig_conformance.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    font=dict(
        color="#334155"
    ),

    title_font=dict(
        color="#0B3D91",
        size=20
    )
)


st.plotly_chart(
    fig_conformance,
    use_container_width=True
)


# -------------------------------------------------
# NON-COMPLIANT CASES
# -------------------------------------------------

st.subheader("⚠️ Non-Compliant Patient Paths")


non_compliant = conformance_results[
    conformance_results["Status"]
    == "Non-Compliant"
]


st.dataframe(
    non_compliant,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748B;
        padding:20px;
        font-size:14px;
    ">
        🏥 CareFlow – Clinical Pathway Process Mining
        <br>
        Healthcare Operations & Process Analytics
    </div>
    """,
    unsafe_allow_html=True
)