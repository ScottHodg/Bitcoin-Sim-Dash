import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pickle
import pandas as pd

# --- NEW: LOAD THE DATA ---
try:
    with open('dashboard_data.pkl', 'rb') as f:
        data = pickle.load(f)
    
    # Extract variables from the dictionary
    df_plot = data['df_plot']
    stats_p = data['stats_p']
    stats_v = data['stats_v']
    correlation = data['correlation']
    price_only = data['price_only']
    volume_only = data['volume_only']
    both_signals = data['both_signals']
except FileNotFoundError:
    st.error("Data file not found! Please run the Colab cell that saves the data first.")
    st.stop()

# --- REST OF YOUR DASHBOARD CODE ---
st.set_page_config(page_title="BTC Analytics", layout="wide")
st.title("₿ Bitcoin Real-Time Analytics")

# 1. Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Strategy A ROI", f"{stats_p['roi']:.2f}%", f"${stats_p['total_value']:,.0f}")
col2.metric("Strategy B ROI", f"{stats_v['roi']:.2f}%", f"${stats_v['total_value']:,.0f}")
col3.metric("Correlation", f"{correlation:.4f}")

# 2. Main Price Chart
st.subheader("BTC Price Trend & Anomalies")
fig_price = px.line(df_plot, x="timestamp", y="Close", template="plotly_dark")
# Add anomalies markers
anomalies_only = df_plot[df_plot["price_signal"]]
fig_price.add_trace(go.Scatter(x=anomalies_only["timestamp"], y=anomalies_only["Close"], 
                               mode="markers", name="Anomalies", marker=dict(color='red')))
st.plotly_chart(fig_price, width=True)

# 3. Two-Column Layout for Volatility and Signals
left_col, right_col = st.columns(2)

with left_col:
    st.write("### Volatility Tracking")
    fig_vol = px.bar(df_plot, x="timestamp", y="drop_pct", template="plotly_dark")
    st.plotly_chart(fig_vol, width=True)

with right_col:
    st.write("### Signal Distribution")
    fig_corr = px.bar(x=["Price", "Volume", "Both"], y=[price_only, volume_only, both_signals], 
                      color=["Price", "Volume", "Both"], template="plotly_dark")
    st.plotly_chart(fig_corr, width=True)
