import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BTC Analytics Pro", layout="wide")

# Load existing and new data
@st.cache_data
def load_all_data():
    df = pd.read_csv('df_plot.csv')
    stats = pd.read_csv('stats_summary.csv').set_index('metric')
    monthly = pd.read_csv('monthly_stats.csv')
    hourly = pd.read_csv('hourly_volume.csv')
    daily = pd.read_csv('daily_volume.csv')
    return df, stats, monthly, hourly, daily

df, stats, monthly, hourly, daily = load_all_data()

st.title("₿ Bitcoin Strategic Analytics Dashboard")

# --- ROW 1: CORE METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Strategy A ROI", f"{stats.loc['roi_p', 'value']:.2f}%")
col2.metric("Strategy B ROI", f"{stats.loc['roi_v', 'value']:.2f}%")
col3.metric("Signal Correlation", f"{stats.loc['correlation', 'value']:.4f}")
col4.metric("Anomalies Found", len(df[df['drop_pct'] > 0.05]))

# --- ROW 2: PRICE & MONTHLY TRENDS ---
c1, c2 = st.columns([2, 1])
with c1:
    st.subheader("Price Action & Detected Flash Crashes")
    fig_p = px.line(df, x='timestamp', y='Close', template='plotly_dark', color_discrete_sequence=['#f2a900'])
    anomalies = df[df['drop_pct'] > 0.05]
    fig_p.add_trace(go.Scatter(x=anomalies['timestamp'], y=anomalies['Close'], mode='markers', name='Flash Drops', marker=dict(color='red', size=8)))
    st.plotly_chart(fig_p, use_container_width=True)

with c2:
    st.subheader("Monthly Volume Growth")
    fig_m = px.bar(monthly, x='Month', y='Total_Volume', template='plotly_dark', title="Volume by Month")
    st.plotly_chart(fig_m, use_container_width=True)

# --- ROW 3: MARKET TIMING (SPARK ANALYSIS) ---
st.divider()
st.subheader("⏱️ Market Timing Insights (When do whales trade?)")
left, right = st.columns(2)

with left:
    st.write("#### Average Volume by Hour (UTC)")
    fig_h = px.bar(hourly, x='hour', y='avg_volume', template='plotly_dark', color='avg_volume', color_continuous_scale='Viridis')
    st.plotly_chart(fig_h, use_container_width=True)

with right:
    st.write("#### Average Volume by Day of Week")
    # Sort days for better visualization
    day_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    fig_d = px.bar(daily, x='day_name', y='avg_volume', template='plotly_dark', category_orders={"day_name": day_order})
    st.plotly_chart(fig_d, use_container_width=True)
#4
st.divider()
st.subheader("Minute-Level Activity (Systemic Check)")
st.write("This chart identifies volume spikes within the hour (0-59 minutes). Peaks often indicate automated algorithmic trading or 'top of the hour' liquidations.")
fig_m = px.line(minute, x='minute', y='avg_volume', template='plotly_dark', markers=True, color_discrete_sequence=['#00CC96'])
fig_m.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=5))
st.plotly_chart(fig_m, use_container_width=True)
st.write("---")
st.dataframe(df.head(10), use_container_width=True)

# --- HIDE STREAMLIT ELEMENTS ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
