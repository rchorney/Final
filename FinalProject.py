import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px

def Data_Source_Page():
    def load_data_source_page():
        # Title of the page
        st.title("Parking Meters Data Source Information")

        # Markdown for dataset overview
        st.markdown("""
            ## Dataset Overview
            **Title:** Parking Meters  
            **Type:** Geospatial  
            **Description:** This dataset includes comprehensive information about parking meters in the City of Boston. It is updated and maintained by the Boston Transportation Department (BTD) Parking Clerk, ensuring accurate and current data for various applications.  
    
            ## Accessibility and Usage
            **Released:** 2015-08-25  
            **Last Modified:** 2023-10-13  
            **Publisher:** Boston Maps  
            **Classification:** Public Record  
            **License:** Open Data Commons Public Domain Dedication and License (PDDL) - This license allows for free usage, modification, and distribution of the data.  

            ## Contact and Additional Information
            **Contact Point:** Analytics Team  
            **Contact Email:** [analyticsteam@boston.gov](mailto:analyticsteam@boston.gov)  
            **Landing Page:** [Parking Meters Dataset](https://bostonopendata-boston.opendata.arcgis.com/maps/boston::parking-meters)  
        """)
    
        # Additional information about the dataset
        st.markdown("""
            ### About the Dataset
            The "Parking Meters" dataset provides geospatial data on parking meters across Boston, valuable for urban planning, transportation analysis, and economic studies. It reflects the city's efforts in digitizing and making public essential urban data for broader use.
        """)
    
        # Initializing a session state for feedback list
        if 'feedback_list' not in st.session_state:
            st.session_state.feedback_list = []

            # Section for user feedback
            st.title("Feedback")
            with st.form("feedback_form"):
                st.text_area("Please provide your feedback:")
                submit_button = st.form_submit_button("Submit")

                if submit_button:
                    # Display a success message upon submission
                    st.success("Thank you for your feedback!")

    # Call the function to display the data source page
    load_data_source_page()

def data_Overview_Page():
    st.title("Data Overview")
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

def main():
    # Sidebar navigation
    st.sidebar.title("Navigation")
    # Create a dictionary of your pages
    pages_dict = {
        "Home": render_home_page,
        "Data Source": Data_Source_Page,
        "Data Overview": data_Overview_Page
    }
    # Radio button for page selection
    selected_page = st.sidebar.radio("Select a page:", list(pages_dict.keys()))

    # Call the app function based on selection
    pages_dict[selected_page]()

def render_home_page():
    
    # Load the data
    df = pd.read_csv("Parking_Meters.csv")

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
