import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Voting System")

# Predefined voting options
options = ['Option A', 'Option B', 'Option C', 'Option D']

# Voting counts (stored in session state)
if 'votes' not in st.session_state:
    st.session_state['votes'] = [0] * len(options)

# Voting mechanism
st.write("### Vote for your favorite option:")
selected_option = st.selectbox('Choose an option:', options)

if st.button('Vote'):
    idx = options.index(selected_option)
    st.session_state['votes'][idx] += 1
    st.write(f"Thanks for voting for {selected_option}!")

# Display voting results
results_df = pd.DataFrame({
    'Option': options,
    'Votes': st.session_state['votes']
})

st.write("### Live Voting Results:")
st.write(results_df)

# Bar chart of results
fig = px.bar(results_df, x='Option', y='Votes', title='Voting Results')
st.plotly_chart(fig)
