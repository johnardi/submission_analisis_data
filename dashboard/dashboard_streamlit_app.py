import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from plotly.colors import sequential
import plotly.graph_objects as go
from babel.numbers import format_currency
sns.set(style='dark')

file_path = os.path.abspath("/mount/src/submission_analisis_data/dashboard/all_data.csv")
tiantan_df = pd.read_csv(file_path)


tiantan_df['datetime'] = pd.to_datetime(tiantan_df['datetime'])

pollutant_parameters = list(tiantan_df.columns[:6])
weather_parameters = list(tiantan_df.columns[6:10]) + [tiantan_df.columns[11]]

# Define the custom category order
category_ranges = [
    "Good",
    "Moderate",
    "Unhealthy for Sensitive Groups",
    "Unhealthy",
    "Very Unhealthy",
    "Hazardous"
]

st.title('Air Quality Dashboard 2013 - 2017')
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://www.logoai.com/oss/icons/2021/10/27/NTs7EMHlHtbJE3B.png"
                 , width=100)
    with col3:
        st.write(' ')
    st.header('Filters')


# Station filter with multiselect
selected_stations = st.sidebar.multiselect('Select Stations', ['Overall Station'] + list(tiantan_df['station'].unique()))

selected_category = st.sidebar.selectbox('Select Category',
                                         ['Overall Category'] + list(tiantan_df['Category'].unique()), index=0)
start_date = st.sidebar.date_input('Start Date', min(tiantan_df['datetime']).date(),
                                   min_value=pd.to_datetime('2013-03-01').date(),
                                   max_value=pd.to_datetime('2017-02-28').date())
end_date = st.sidebar.date_input('End Date', max(tiantan_df['datetime']).date(),
                                 min_value=pd.to_datetime('2013-03-01').date(),
                                 max_value=pd.to_datetime('2017-02-28').date())
start_hour = st.sidebar.slider('Start Hour', 0, 23, 0)
end_hour = st.sidebar.slider('End Hour', 0, 23, 23)


# Filter tiantan_df based on selected stations
if 'Overall Station' in selected_stations:
    selected_stations.remove('Overall Station')

start_datetime = pd.to_datetime(start_date).date
end_datetime = pd.to_datetime(end_date).date
tiantan_df['date'] = tiantan_df['datetime'].dt.date
tiantan_df['Hour'] = tiantan_df['datetime'].dt.hour

# Filter tiantan_df based on selected stations
if 'Overall Station' in selected_stations:
    selected_stations.remove('Overall Station')

if selected_category == 'Overall Category' and not selected_stations:
    # If no specific stations are selected, use all stations
    filtered_tiantan_df = tiantan_df[(tiantan_df['date'] >= start_datetime()) & (tiantan_df['date'] <= end_datetime()) &
                         (tiantan_df['Hour'] >= start_hour) & (tiantan_df['Hour'] <= end_hour)]
elif not selected_stations:
    filtered_tiantan_df = tiantan_df[(tiantan_df['Category'] == selected_category) &
                         (tiantan_df['date'] >= start_datetime()) & (tiantan_df['date'] <= end_datetime()) &
                         (tiantan_df['Hour'] >= start_hour) & (tiantan_df['Hour'] <= end_hour)]
elif selected_category == 'Overall Category':
    filtered_tiantan_df = tiantan_df[(tiantan_df['station'].isin(selected_stations)) &
                         (tiantan_df['date'] >= start_datetime()) & (tiantan_df['date'] <= end_datetime()) &
                         (tiantan_df['Hour'] >= start_hour) & (tiantan_df['Hour'] <= end_hour)]
else:
    filtered_tiantan_df = tiantan_df[(tiantan_df['station'].isin(selected_stations)) & (tiantan_df['Category'] == selected_category) &
                         (tiantan_df['date'] >= start_datetime()) & (tiantan_df['date'] <= end_datetime()) &
                         (tiantan_df['Hour'] >= start_hour) & (tiantan_df['Hour'] <= end_hour)]


selected_station_str = ', '.join(selected_stations) if selected_stations else 'All Stations'
st.write(f"**Key Metrics for {selected_station_str} - {selected_category}**")
category_counts = filtered_tiantan_df.groupby('Category')['datetime'].nunique()
cols = st.columns(3)
for index, (category, count) in enumerate(category_counts.items()):
    formatted_count = "{:,}".format(count)  # Format count with commas for thousands
    col = cols[index % 3]  # Cycle through the columns (3 columns)
    col.metric(category, f"{formatted_count} Days")


# Calculate counts for each category and set the custom order
custom_colors = {
    "Good": "#008000",
    "Moderate": "#FFFF00",
    "Unhealthy for Sensitive Groups": "#FFA500",
    "Unhealthy": "#FF0000",
    "Very Unhealthy": "#800080",
    "Hazardous": "#800000"
}

category_counts = tiantan_df['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']
category_counts['Category'] = pd.Categorical(category_counts['Category'], categories=category_ranges, ordered=True)
category_counts = category_counts.sort_values('Category')
# Create a pie chart
fig = px.pie(category_counts, values='Count', names='Category', title='Air Quality Categories Percentage', color='Category', color_discrete_map=custom_colors)
# Display the chart in Streamlit
st.plotly_chart(fig)


col1, col2 = st.columns(2)
with col1:
    selected_parameter = st.selectbox('Select Air Pollutant Parameter', pollutant_parameters)
with col2:
    frequency_options = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Yearly']
    selected_frequency = st.selectbox('Select Time Frequency', frequency_options)

# Plot the chart for the selected stations
filtered_tiantan_df_resampled = filtered_tiantan_df.groupby(['station',
                                                 pd.Grouper(key='datetime',
                                                            freq=selected_frequency[0])])[selected_parameter].mean().reset_index()
fig = px.line(filtered_tiantan_df_resampled, x='datetime', y=selected_parameter, color='station',
              title=f'{selected_parameter} {selected_frequency} Levels Over Time')
st.plotly_chart(fig)



# Group and pivot the tiantan_df to get the counts for each category and station
pivot_tiantan_df = filtered_tiantan_df.pivot_table(index='station', columns='Category', values='PM2.5', aggfunc='count', fill_value=0)

# Convert pivot_tiantan_df to long format
long_format_tiantan_df = pivot_tiantan_df.reset_index().melt(
    id_vars='station', 
    var_name='Category', 
    value_name='Count'
)

# Create a grouped bar chart with labels using Graph Objects
fig = go.Figure()

for category in category_ranges:
    category_tiantan_df = long_format_tiantan_df[long_format_tiantan_df['Category'] == category]
    fig.add_trace(go.Bar(
        x=category_tiantan_df['station'],
        y=category_tiantan_df['Count'],
        name=category,
        text=category_tiantan_df['Count'],  # Add labels
        textposition='outside',  # Position labels outside the bars
        marker_color=custom_colors[category]
    ))

# Customize the layout
fig.update_layout(
    barmode='group',  # Grouped bar chart
    title='Air Quality by Station',
    xaxis_title='Station',
    yaxis_title='Count',
    legend_title='Air Quality Categories',
    template='plotly_white'
)

# Display the chart in Streamlit
st.plotly_chart(fig)




# Map categories to a numerical order based on the custom order
category_order_mapping = {category: i for i, category in enumerate(category_ranges)}

# Assign a numerical order to each row in the tiantan_dfset
tiantan_df['Category_Order'] = filtered_tiantan_df['Category'].map(category_order_mapping)

# Group and aggregate tiantan_df
grouped_tiantan_df = tiantan_df.groupby(['wd', 'Category']).size().reset_index(name='count')

# Sort the tiantan_df based on the custom category order and category order mapping
grouped_tiantan_df['Category_Order'] = grouped_tiantan_df['Category'].map(category_order_mapping)
grouped_tiantan_df = grouped_tiantan_df.sort_values(by=['Category_Order', 'wd'])

# Create a colormap with varying shades of a single color (e.g., blue)
# color_scale = pc.sequential.Blues
color_scale = sequential.GnBu
# Create polar bar chart
fig = go.Figure()


categories = category_ranges

for i, category in enumerate(categories):
    category_tiantan_df = grouped_tiantan_df[grouped_tiantan_df['Category'] == category]
    color = color_scale[i]  # Get a shade of blue from the colormap
    fig.add_trace(go.Barpolar(
        r=category_tiantan_df['count'],
        theta=category_tiantan_df['wd'],
        name=category,
        text=category_tiantan_df['count'],
        hoverinfo='text',
        marker=dict(color=color)
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, max(grouped_tiantan_df['count'])])
    ),
    title="Air Quality by Wind Direction",
)

# Display the chart in Streamlit
st.plotly_chart(fig)
