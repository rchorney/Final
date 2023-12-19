import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

def main():
    # Load the data
    path = "C:/Users/reube/OneDrive - Bentley University/School 23-24/CS230/Final/"
    file = "Parking_Meters.csv"
    pathFile = path + file
    df = pd.read_csv(pathFile)

    # Convert 'TOW_AWAY' column to boolean - new code I used
    df['TOW_AWAY'] = ~df['TOW_AWAY'].isna()

    # Streamlit title and introduction
    st.title("Python Final Project")
    st.write("Data Source: Parking Meters")
    st.write("by: Reuben Chorney")

    # Display an image
    image_path = "https://www.spotangels.com/blog/wp-content/uploads/2018/11/boston-street-parking-guide.jpg"
    st.image(image_path, caption='Boston Parking Meter', use_column_width=True)

    # Sidebar filter for 'TOW_AWAY'
    st.sidebar.title("Filters")
    tow_away_filter = st.sidebar.radio('Show meters in tow-away zones:', ['All', 'Yes', 'No'])

    # Apply filter based on tow-away zone
    if tow_away_filter == 'Yes':
        filtered_df = df[df['TOW_AWAY'] == True]
    elif tow_away_filter == 'No':
        filtered_df = df[df['TOW_AWAY'] == False]
    else:
        filtered_df = df

    # Radio button for chart type selection
    map_selection = st.radio(
        "Click for a different view of the same data",
        ("Option 1 (3-D)", "Option 2 (flat)", "Option 3 (heat)")
    )

    # Display selected visualization
    if map_selection == "Option 1 (3-D)":
        visual1(filtered_df)
    elif map_selection == "Option 2 (flat)":
        visual2(filtered_df)
    elif map_selection == "Option 3 (heat)":
        visual3(filtered_df)

    # Display installation chart
    create_installation_chart(df)

    st.title("Summary of Parking Meters Analysis")

    summary_text = """
        **Summary and Insights from the Parking Meters Analysis**

        Through our analysis of parking meter data in the city, we've uncovered key insights that could significantly enhance urban parking strategies. 

        One primary finding is the potential benefit of seeking parking in areas with a high density of parking meters but fewer tow-away zones. These areas are likely to offer more parking opportunities and less risk of penalties. 

        Additionally, our data exploration revealed that most parking meters charge a nominal rate of $0.25. This affordable rate suggests that, for a majority of parking spaces in the city, cost-effective parking is feasible, which is advantageous for both daily commuters and occasional visitors.
        """
    st.write(summary_text)

# Visualization 1: 3D Grid Layer
def visual1(filtered_df):
    # Filter out NaN values in coordinates
    clean_df = filtered_df.dropna(subset=['LONGITUDE', 'LATITUDE'])

    # Create GridLayer for 3D visualization
    grid_layer = pdk.Layer(
        "GridLayer",
        clean_df,
        get_position=['LONGITUDE', 'LATITUDE'],
        cell_size=200,
        elevation_scale=4,
        pickable=True,
        extruded=True,
    )

    # Define the map view
    view_state = pdk.ViewState(
        latitude=clean_df['LATITUDE'].mean(),
        longitude=clean_df['LONGITUDE'].mean(),
        zoom=11,
        pitch=45,  # Angled view
        bearing=0
    )

    # Render the map with the GridLayer
    r = pdk.Deck(
        layers=[grid_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9',
        tooltip={"text": "Count: {count}"}
    )

    # Display the map in Streamlit
    st.pydeck_chart(r)

# Visualization 2: Flat Scatterplot Layer
def visual2(filtered_df):
    # Filter out NaN values in coordinates
    clean_df = filtered_df.dropna(subset=['LONGITUDE', 'LATITUDE'])

    # Create ScatterplotLayer for 2D visualization
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        clean_df,
        get_position=['LONGITUDE', 'LATITUDE'],
        get_color='[200, 30, 0, 160]',
        get_radius=100,
    )

    # Define the map view
    view_state = pdk.ViewState(
        latitude=clean_df['LATITUDE'].mean(),
        longitude=clean_df['LONGITUDE'].mean(),
        zoom=11
    )

    # Render the map with the ScatterplotLayer
    r = pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    )

    # Display the map in Streamlit
    st.pydeck_chart(r)

# Visualization 3: Heatmap Layer
def visual3(filtered_df):
    # Filter out NaN values in coordinates
    clean_df = filtered_df.dropna(subset=['LONGITUDE', 'LATITUDE'])

    # Create HeatmapLayer for heat map visualization
    heat_map_layer = pdk.Layer(
        "HeatmapLayer",
        data=clean_df,
        get_position=['LONGITUDE', 'LATITUDE'],
        radius=100,
        opacity=0.9,
        get_weight='BASE_RATE' if 'BASE_RATE' in clean_df.columns else 1  # Use BASE_RATE as weight if available
    )

    # Define the map view
    view_state = pdk.ViewState(
        latitude=clean_df['LATITUDE'].mean(),
        longitude=clean_df['LONGITUDE'].mean(),
        zoom=11
    )

    # Render the map with the HeatmapLayer
    r = pdk.Deck(
        layers=[heat_map_layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9'
    )

    # Display the map in Streamlit
    st.pydeck_chart(r)

# Function to create an installation timeline chart
def create_installation_chart(df):
    # Convert 'INSTALLED_ON' column to datetime and group by date
    df['INSTALLED_ON'] = pd.to_datetime(df['INSTALLED_ON'])
    installation_counts = df.groupby(df['INSTALLED_ON'].dt.date).size()

    # Display the installation timeline chart
    st.write("Installation Timeline of Parking Meters")
    st.line_chart(installation_counts)

# Run the main function
main()
