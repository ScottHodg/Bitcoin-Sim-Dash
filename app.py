import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="BTC Strategy Results", layout="wide")

# Load the data files
@st.cache_data
def load_data():
    df = pd.read_csv('df_plot.csv')
    stats = pd.read_csv('stats_summary.csv').set_index('metric')
    return df, stats

df, stats = load_data()

st.title("₿ BTC Strategy Analysis (Choice A)")

# Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Strategy A ROI", f"{stats.loc['roi_p', 'value']:.2f}%")
col2.metric("Strategy B ROI", f"{stats.loc['roi_v', 'value']:.2f}%")
col3.metric("Correlation", f"{stats.loc['correlation', 'value']:.4f}")

# Main Chart
st.subheader("Price & Anomalies")
fig = px.line(df, x='timestamp', y='Close', template='plotly_dark')
# Add red dots for anomalies
anomalies = df[df['drop_pct'] > 0.05] # Adjust based on your threshold
fig.add_trace(go.Scatter(x=anomalies['timestamp'], y=anomalies['Close'], 
                         mode='markers', name='Anomalies', marker=dict(color='red')))
st.plotly_chart(fig, use_container_width=True)

st.write("### Data Overview")
st.dataframe(df.head(20), use_container_width=True)
