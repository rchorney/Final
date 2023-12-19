import streamlit as st

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

    # Embedding a video file
    st.video("C:/Users/reube/Downloads/pexels-james-hamar-12595889 (2160p).mp4")

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
