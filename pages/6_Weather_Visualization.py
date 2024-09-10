import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Weather Data Visualization")

# Simulated weather data for two cities
city_data = pd.DataFrame({
    'City': ['City A', 'City B'],
    'Temperature (°C)': [20, 25],
    'Humidity (%)': [60, 70]
})

# Display the data
st.write("Weather Data for Two Cities:")
st.write(city_data)

# Bar chart visualization
fig = px.bar(city_data, x='City', y=['Temperature (°C)', 'Humidity (%)'],
             title='Weather Data Comparison')
st.plotly_chart(fig)
