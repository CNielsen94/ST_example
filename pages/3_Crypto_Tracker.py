import streamlit as st
import pandas as pd
import numpy as np

st.title("Real-Time Cryptocurrency Price Tracker")

# Simulated cryptocurrency prices
cryptos = ['Bitcoin', 'Ethereum', 'Litecoin', 'Dogecoin', 'Ripple']
prices = np.random.uniform(100, 50000, len(cryptos))

crypto_data = pd.DataFrame({
    'Cryptocurrency': cryptos,
    'Price (USD)': prices
})

# Display the data
st.write("Cryptocurrency Prices:")
st.write(crypto_data)

# Bar chart visualization
st.bar_chart(crypto_data.set_index('Cryptocurrency')['Price (USD)'])