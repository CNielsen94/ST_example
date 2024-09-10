import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv('https://sds-aau.github.io/SDS-master/M1/data/RI-clean.csv.gz', low_memory=False)

    # Drop unnecessary columns
    df.drop(['id', 'county_name', 'county_fips', 'fine_grained_location', "out_of_state"], axis='columns', inplace=True)

    # Drop rows with missing crucial data
    df.dropna(subset=['stop_date', 'stop_time', 'driver_gender', 'driver_age'], inplace=True)

    # Create two datasets: one for search instances and one for the rest
    df_search_type = df[~df['search_type'].isna()]
    df_no_search = df[df['search_type'].isna()]

    return df_search_type, df_no_search

# Load cleaned datasets
df_search_type, df_no_search = load_data()

# Sidebar filters
st.sidebar.header("Filter the data")

# State selector
states = df_no_search['location_raw'].unique()
selected_state = st.sidebar.selectbox('Select a Location', states)

# Violation selector
violations = df_no_search['violation'].unique()
selected_violation = st.sidebar.selectbox('Select a Violation', violations)

# Gender multi-select
selected_genders = st.sidebar.multiselect('Select Genders', df_no_search['driver_gender'].unique(), default=df_no_search['driver_gender'].unique())

# Age range slider
age_range = st.sidebar.slider('Select Age Range', int(df_no_search['driver_age'].min()), int(df_no_search['driver_age'].max()), (18, 60))

# Dataset selector
dataset_option = st.sidebar.radio(
    "Choose Dataset",
    ('No Search Dataset', 'Search Type Dataset')
)

# Use selected dataset
if dataset_option == 'No Search Dataset':
    filtered_data = df_no_search
else:
    filtered_data = df_search_type

# Apply filters
filtered_data = filtered_data[(filtered_data['location_raw'] == selected_state) &
                              (filtered_data['violation'] == selected_violation) &
                              (filtered_data['driver_gender'].isin(selected_genders)) &
                              (filtered_data['driver_age'].between(age_range[0], age_range[1]))]

st.write(f"### Data for location: {selected_state}, Violation: {selected_violation}")
st.write("Data Preview:", filtered_data.head())

### 1. Univariate Analysis ###
st.subheader('Univariate Analysis')

# Driver Age Distribution (Interactive)
st.write("#### Driver Age Distribution")
fig_age = px.histogram(filtered_data, x='driver_age', nbins=20, title='Driver Age Distribution')
st.plotly_chart(fig_age)

#st.write("#### Driver Age Distribution")
#fig_age = px.histogram(filtered_data, x='driver_age', nbins=50, title='Driver Age Distribution')
#fig_age.update_layout(yaxis_title='Number of Drivers', xaxis_title='Age', 
#                      xaxis=dict(showgrid=True), yaxis=dict(showgrid=True))
#st.plotly_chart(fig_age)

#fig_age = px.histogram(filtered_data, x='driver_age', nbins=20, title='Driver Age Distribution')
#fig_age.update_layout(
#    yaxis_title='Number of Drivers',
#    xaxis_title='Age',
#    xaxis=dict(showgrid=True),
#    yaxis=dict(showgrid=True, tickmode='linear', dtick=10)  # Set a linear tick mode with a tick interval of 10
#)
#st.plotly_chart(fig_age)


# Violation Distribution
st.write("#### Distribution of Violations")
fig_violation = px.histogram(df_no_search, x='violation', title='Violation Distribution')
st.plotly_chart(fig_violation)

### 2. Bivariate Analysis ###
st.subheader('Bivariate Analysis')

# Gender vs Race
st.write("#### Driver Gender vs Driver Race")
fig_gender_race = px.histogram(filtered_data, x='driver_gender', color='driver_race', title='Driver Gender vs Driver Race')
st.plotly_chart(fig_gender_race)

# Stop Duration vs Stop Outcome
#st.write("#### Stop Duration vs Stop Outcome")
#fig_duration_outcome = px.scatter(filtered_data, x='stop_duration', y='stop_outcome', color='driver_race', title='Stop Duration vs Stop Outcome')
#st.plotly_chart(fig_duration_outcome)
st.write("#### Stop Duration vs Stop Outcome (Box Plot)")
fig_duration_outcome = px.box(filtered_data, x='stop_outcome', y='stop_duration', color='stop_outcome', title='Stop Duration vs Stop Outcome')
st.plotly_chart(fig_duration_outcome)


### 3. Multivariate Analysis ###
st.subheader('Multivariate Analysis')

# Gender, Race, and Stop Outcome (Categorical Relationships)
st.write("#### Driver Gender, Race, and Stop Outcome")
fig_multivariate = px.parallel_categories(filtered_data, dimensions=['driver_gender', 'driver_race', 'stop_outcome'], title='Gender, Race, and Stop Outcome')
st.plotly_chart(fig_multivariate)

### 4. Time Series Analysis ###
st.subheader('Time Series Analysis')

# Convert 'stop_date' to datetime
filtered_data['stop_date'] = pd.to_datetime(filtered_data['stop_date'])

# Stops Over Time
st.write("#### Stops Over Time")
stops_over_time = filtered_data.groupby('stop_date').size().reset_index(name='counts')
fig_timeseries = px.line(stops_over_time, x='stop_date', y='counts', title='Stops Over Time')
st.plotly_chart(fig_timeseries)

# Stop Duration Over Time
#st.write("#### Stop Duration Over Time")
#fig_duration_time = px.line(filtered_data, x='stop_date', y='stop_duration', title='Stop Duration Over Time')
#st.plotly_chart(fig_duration_time)
# Aggregate by month and calculate the average stop duration

# Plot the monthly average stop duration
#st.write("#### Monthly Average Stop Duration Over Time")
#fig_duration_time = px.line(monthly_duration, x='month_year', y='stop_duration', title='Monthly Average Stop Duration Over Time')
#st.plotly_chart(fig_duration_time)
# Ensure stop_duration is numeric
# Convert 'stop_date' to datetime format
filtered_data['stop_date'] = pd.to_datetime(filtered_data['stop_date'], errors='coerce')

# Drop rows where 'stop_date' is NaT
filtered_data = filtered_data.dropna(subset=['stop_date'])

# Extract month-year from the stop_date
filtered_data['month_year'] = filtered_data['stop_date'].dt.to_period('M')

# Group by month_year and stop_duration, and count occurrences
monthly_duration_counts = filtered_data.groupby(['month_year', 'stop_duration']).size().reset_index(name='counts')

# Convert 'month_year' to string for better display in Plotly
monthly_duration_counts['month_year'] = monthly_duration_counts['month_year'].astype(str)

# Plot the stop duration counts over time, grouped by duration category
st.write("#### Stop Duration Distribution Over Time")
fig_duration_time = px.line(
    monthly_duration_counts, 
    x='month_year', 
    y='counts', 
    color='stop_duration', 
    title='Stop Duration Distribution Over Time',
    labels={'counts': 'Number of Stops', 'month_year': 'Month-Year', 'stop_duration': 'Stop Duration'}
)
st.plotly_chart(fig_duration_time)

