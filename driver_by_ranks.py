
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.nonparametric.smoothers_lowess import lowess

# Title
st.title("Vets Racing: Lap Time vs Rank by Round")

# Load data
csv_path = "Vets Season 23 Vets Ranking by pace.csv"
df = pd.read_csv(csv_path)

# Identify rounds and drivers
round_columns = [col for col in df.columns if col.startswith("Round")]
driver_names = df["display_name"].dropna().unique()

# User selects a round
selected_round = st.selectbox("Select a round", round_columns)

# User optionally selects a driver to highlight
highlight_driver = st.selectbox("Highlight a driver (optional)", ["None"] + sorted(driver_names.tolist()))

# Filter valid data
filtered_df = df.dropna(subset=["Rank", selected_round])
filtered_df = filtered_df[(filtered_df[selected_round] > 50) & (filtered_df[selected_round] < 200)]
rank = filtered_df["Rank"].values
lap_time = filtered_df[selected_round].values

# Apply LOWESS smoothing
lowess_smoothed = lowess(lap_time, rank, frac=0.2)

# Plot
fig = go.Figure()

# Add all driver lap times
fig.add_trace(go.Scatter(
    x=rank,
    y=lap_time,
    mode='markers',
    name='Lap Times',
    marker=dict(color='blue'),
    text=filtered_df["display_name"]
))

# Highlight selected driver
if highlight_driver != "None":
    driver_data = filtered_df[filtered_df["display_name"] == highlight_driver]
    if not driver_data.empty:
        fig.add_trace(go.Scatter(
            x=driver_data["Rank"],
            y=driver_data[selected_round],
            mode='markers+text',
            name=f"{highlight_driver}",
            marker=dict(color='red', size=10),
            text=[highlight_driver],
            textposition="top center"
        ))

# Add LOWESS curve
fig.add_trace(go.Scatter(
    x=lowess_smoothed[:, 0],
    y=lowess_smoothed[:, 1],
    mode='lines',
    name='Average time',
    line=dict(color='white')
))

fig.update_layout(
    title=f"Lap Time vs Rank - {selected_round}",
    xaxis_title="Rank",
    yaxis_title="Lap Time (s)",
    template="plotly_white"
)

st.plotly_chart(fig)
