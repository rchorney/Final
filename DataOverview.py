import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px

# Function to load data from a CSV file
def load_data():
    df = pd.read_csv("Parking_Meters.csv")
    return df

# Function to analyze parking data
def analyze_parking_data(df, column_name="X"):
    avg_value = df[column_name].mean(skipna=True)
    max_value = df[column_name].max(skipna=True)
    return avg_value, max_value

# Function to create a map visualization
def create_map(df):
    point_layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=['LONGITUDE', 'LATITUDE'],
        get_color=[180, 0, 200, 140],  # RGBA color configuration
        get_radius=100,
    )
    view_state = pdk.ViewState(
        latitude=df['LATITUDE'].mean(),
        longitude=df['LONGITUDE'].mean(),
        zoom=11,
        pitch=0,
    )
    r = pdk.Deck(layers=[point_layer], initial_view_state=view_state, map_style="mapbox://styles/mapbox/light-v9")
    st.pydeck_chart(r)

# Function to create a pie chart
def create_pie_chart(df):
    zone_counts_dict = {}
    for zone in df['G_ZONE'].unique():
        count = df[df['G_ZONE'] == zone].shape[0]
        zone_counts_dict[zone] = count

    zone_counts = pd.DataFrame(list(zone_counts_dict.items()), columns=['Zone', 'Count'])

    zone_counts.sort_values(by='Zone', inplace=True)

    fig = px.pie(zone_counts, names='Zone', values='Count',
                 hover_data=['Zone'],
                 title='Distribution of Parking Meters by Zone')
    fig.update_traces(textinfo='percent')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Function to create a bar chart
def create_bar_chart(df):
    st.subheader("Zone-wise Distribution of Parking Meters")

    unique_zones = set(df['G_ZONE'])
    unique_zones = sorted(unique_zones)

    zone_counts = {}
    for zone in unique_zones:
        count = 0
        for zone_value in df['G_ZONE']:
            if zone_value == zone:
                count += 1
        zone_counts[zone] = count

    zones = list(zone_counts.keys())
    counts = list(zone_counts.values())
    zone_df = pd.DataFrame({"Zone": zones, "Count": counts})
    zone_df.set_index("Zone", inplace=True)

    st.bar_chart(zone_df)

# Main function to display the data overview page
def data_overview_page():
    df = load_data()
    df.dropna(subset=['LONGITUDE', 'LATITUDE', 'G_ZONE'], inplace=True)

    st.title("Data Overview: Parking Meters Distribution.")
    image_path = "https://dailyfreepress.com/wp-content/uploads/parkingmeter_betsey.jpg"
    st.image(image_path, caption='Boston Parking Meter', use_column_width=True)

    st.write("In this section, we will explore the distribution and utilization patterns of parking meters across different zones - and just a general overview of important information. This will be in part to suggest where parking is most fortunate.")

    st.subheader("Basic Statistics")
    st.write(df[['X', 'Y', 'BASE_RATE']].describe())

    avg_rate, max_rate = analyze_parking_data(df, 'BASE_RATE')
    st.write(f"Average Base Rate: {avg_rate}, Maximum Base Rate: {max_rate}")

    avg_rate, max_rate = analyze_parking_data(df)
    st.write(f"Average X: {avg_rate}, Maximum X: {max_rate}")

    create_bar_chart(df)

    st.subheader("Map of Meter locations by Zone")
    selected_zone = st.selectbox("Select a Zone for Map", ['All'] + sorted(df['G_ZONE'].unique().tolist()))
    map_df = df if selected_zone == 'All' else df[df['G_ZONE'] == selected_zone]
    create_map(map_df)

    create_pie_chart(df)

# Call the function to display the page
data_overview_page()
