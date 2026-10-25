import streamlit as st
import pandas as pd
import plotly.express as px
from utils import validate_dataframe, calculate_pump_metrics, logging

st.set_page_config(
    page_title="SmartPump Analytics Dashboard",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ SmartPump Analytics Dashboard")
st.markdown("Industrial centrifugal pump performance monitoring and health diagnostics.")

# Sidebar
st.sidebar.header("Data Ingestion")
uploaded_file = st.sidebar.file_uploader("Upload Telemetry CSV", type=["csv"])

# Load sample data option if no file uploaded
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Custom CSV loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading file: {e}")
        st.stop()
else:
    if st.sidebar.button("Load Sample Dataset"):
        try:
            df = pd.read_csv("data/sample_telemetry.csv")
            st.sidebar.success("Sample dataset loaded!")
        except FileNotFoundError:
            st.sidebar.error("Sample dataset not found in data/ directory.")
            st.stop()
    else:
        st.info("Please upload a CSV file or click 'Load Sample Dataset' in the sidebar to begin.")
        st.stop()

# Main workflow execution
try:
    validate_dataframe(df)
    processed_df = calculate_pump_metrics(df)
    logging.info("Pipeline executed successfully.")
except Exception as e:
    st.error(f"Application Error: {e}")
    st.stop()

# Controls
pump_list = processed_df['pump_id'].unique()
selected_pump = st.sidebar.selectbox("Select Pump ID", pump_list)

filtered_df = processed_df[processed_df['pump_id'] == selected_pump]

# Display Metrics
st.header(f"Diagnostics for Pump: {selected_pump}")
col1, col2, col3 = st.columns(3)

latest_row = filtered_df.iloc[-1]
with col1:
    st.metric("Latest Efficiency", f"{latest_row['efficiency']:.1f}%")
with col2:
    st.metric("Flow Rate", f"{latest_row['flow_rate']} m³/h")
with col3:
    status = latest_row['health_state']
    if status == 'HEALTHY':
        st.success(f"Status: {status}")
    elif status == 'DEGRADED':
        st.warning(f"Status: {status}")
    else:
        st.error(f"Status: {status}")

# Charts
st.subheader("Head-Flow Performance Curve")
fig = px.scatter(
    filtered_df, 
    x="flow_rate", 
    y="head_pressure", 
    color="health_state",
    labels={"flow_rate": "Flow Rate (m³/h)", "head_pressure": "Head Pressure (m)"},
    title=f"Head vs Flow for {selected_pump}"
)
st.plotly_chart(fig, use_container_width=True)

# Data Table
st.subheader("Raw Telemetry & Calculated Metrics")
st.dataframe(filtered_df)
