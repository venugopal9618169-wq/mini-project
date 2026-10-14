import streamlit as st
import pandas as pd
import plotly.express as px
from pipeline import run_analytics_pipeline

st.set_page_config(page_title="Smart Grid Energy Analytics Dashboard", layout="wide")

st.title("⚡ Smart Grid Energy-Consumption Analytics Dashboard")
st.markdown("Distributed Spark-Simulated Analytics Pipeline & Utility Operator Interface")

# Load data with caching
@st.cache_data
def get_data():
    return run_analytics_pipeline()

try:
    df = get_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Top-level KPI Metrics
total_records = len(df)
total_anomalies = int(df['is_anomaly'].sum())
avg_consumption = df['Electricity_Consumed'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Meter Readings", f"{total_records:,}")
col2.metric("Flagged Anomalies", total_anomalies, delta_color="inverse")
col3.metric("Anomaly Rate", f"{(total_anomalies / total_records) * 100:.2f}%")
col4.metric("Avg Electricity Consumed", f"{avg_consumption:.3f} kWh")

st.divider()

# Time Series Visualization
st.subheader("📈 Electricity Consumption & Environmental Parameters over Time")
metric_choice = st.selectbox(
    "Select Metric to Visualize", 
    ['Electricity_Consumed', 'Temperature', 'Humidity', 'Wind_Speed', 'Avg_Past_Consumption']
)

fig = px.line(df, x='Timestamp', y=metric_choice, title=f"Trend Analysis: {metric_choice}")

# Highlight anomalies on Electricity Consumed chart
if metric_choice == 'Electricity_Consumed':
    anomalies_df = df[df['is_anomaly'] == 1]
    fig.add_scatter(
        x=anomalies_df['Timestamp'], 
        y=anomalies_df['Electricity_Consumed'],
        mode='markers', 
        marker=dict(color='red', size=8), 
        name='Anomaly Detected'
    )

st.plotly_chart(fig, use_container_width=True)

# Anomaly Log Table
st.subheader("🚨 Recent Anomaly Event Logs")
anomaly_logs = df[df['is_anomaly'] == 1].sort_values(by='Timestamp', ascending=False)
st.dataframe(anomaly_logs[['Timestamp', 'Electricity_Consumed', 'Temperature', 'Humidity', 'Wind_Speed', 'Avg_Past_Consumption', 'Anomaly_Label']], use_container_width=True)