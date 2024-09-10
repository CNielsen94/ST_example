import streamlit as st
import pandas as pd

st.title("Interactive DataFrame Editor")

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'Occupation': ['Engineer', 'Doctor', 'Artist']
}

df = pd.DataFrame(data)
edited_df = st.data_editor(df)
st.write("Updated DataFrame:")
st.write(edited_df)