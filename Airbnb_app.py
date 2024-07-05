# import requirements
import streamlit as st
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px 


# create a streamlit page 
st.set_page_config(page_title="Airbnb Data Visualization",
                   page_icon="random", 
                   layout="wide", 
                   initial_sidebar_state="expanded", 
                   menu_items={'About': "# This dashboard app visualizes and analyzes data."
                              }
                  )


# create main menu selectbox
with st.sidebar:
    select = option_menu("Main Menu", ["Home", "Data Exploration", "About"], key="main_menu")

if select == "Home":

    st.title("Welcome to the Airbnb Data Explorer")

    col1, col2 = st.columns([3, 1])  



    # Content for the first column
    with col1:
        st.markdown("### :sparkles:**Introduction**")
        st.write("""
            Dive into our interactive platform to discover trends, analyze prices, and explore locations of Airbnb listings worldwide.
            
            Explore various aspects of Airbnb data through interactive maps, detailed price analysis, and seasonal availability insights.
        """)

        st.markdown("### :sparkles: **Key Features**")
        st.write("""
            - **Interactive Maps**: Visualize listings and their details.
            - **Price Analysis**: Compare prices across locations and property types.
            - **Seasonal Insights**: Analyze booking patterns and demand fluctuations.
        """)

    # Content for the second column

    with col2:
        st.image(
            r"C:\Users\ELCOT\Downloads\Airbnb_Logo_Over_Gradient.png",  # Path to your image
            caption="Explore with Airbnb",
            use_column_width=True
        )
#**************************  Completd Home Page  *****************************************************************************

elif select == "Data Exploration":
    st.title("Data Exploration")
    st.subheader("Upload Airbnb Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")


    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())  
    else:
        st.write("Please choose a CSV file.")





    # Secondary option menu for "Data Exploration"

    exploration_select = option_menu(
        "Explore", 
        ["Price Analysis", "Availability Analysis", "Location Analysis", "Geospatial Visualization"],
        key="explore_menu"
    )
    
    if exploration_select=="Geospatial Visualization":

        # Create a scatter mapbox
                                                     
        fig_map = px.scatter_mapbox(
            df,
            lat='Latitude',
            lon='Longitude',
            color='Price',
            size='Accomodates',
            hover_name='Name',
            hover_data=['Property_Type', 'Room_Type'],
            color_continuous_scale="rainbow",
            size_max=15,
            zoom=1,

            title='Geospatial Distribution of Listings'
        )


        fig_map.update_layout(
                  mapbox_style="open-street-map",
                  width=1150, height=800,)

        st.plotly_chart(fig_map)

    elif exploration_select=="Price Analysis":
        
        # Use multiselect for room types 

        country_price = st.multiselect("Select the Country(s)", df["Country"].unique(),default=df["Country"].unique())
        df_country = df[df['Country'].isin(country_price)]
        Room_Types = st.multiselect("Select the Room Type(s)", df_country["Room_Type"].unique(), default=df_country["Room_Type"].unique())
        
        # Filter the DataFrame based on selected room types

        df_Room_Type = df_country[df_country["Room_Type"].isin(Room_Types)]

        fig_bar = px.bar(df_Room_Type, x='Property_Type', y='Price', title='PRICE FOR PROPERTY_TYPES',
                        hover_data=["Number_Of_Reviews", "Review_Scores"], color='Price',
                        color_continuous_scale=px.colors.sequential.Redor_r)
        st.plotly_chart(fig_bar)

    elif exploration_select=="Availability Analysis":
        selected_country = st.selectbox(
        "Select a Country", 
        options=df["Country"].unique(), 
        index=0  
    )

        df_country = df[df['Country'] == selected_country]


        if not df_country.empty:
        # Sunburst chart
            fig_sunburst = px.sunburst(
            df_country, 
            path=["Room_Type", "Bed_type", "Is_Location_Exact"], 
            values="Availability_365", 
            title=f"Availability of Listings in {selected_country} (365 days)", 
            color="Availability_365"
             )
        
        # Display chart
            st.plotly_chart(fig_sunburst)
        else:
            st.warning(f"No data available for {selected_country}. Please select another country.")



    elif exploration_select=="Location Analysis":
        country_price = st.multiselect("Select the Country(s)", df["Country"].unique(),default=df["Country"].unique())
        df_country_1= df[df['Country'].isin(country_price)]
        Neighborhood = st.multiselect("Select the neighborhood(s)", df_country_1["Neighborhood"].unique(), default=df_country_1["Neighborhood"].unique())

        df_Neighborhood= df_country_1[df_country_1["Neighborhood"].isin(Neighborhood)]

        st.dataframe(df_Neighborhood)


        fig_bar1 = px.bar(df_Neighborhood, x="Neighborhood", y="Price", title="Average Price by Neighborhood"
                     ,hover_data=["Street", "Location_type"], color='Price',
                        color_continuous_scale=px.colors.sequential.Redor_r)
        st.plotly_chart(fig_bar1)

#*****************************  Completed Explore Page  *********************************************************************

# writing points in about page

elif select=="About":
    st.title("About This Application")
    st.markdown("""
        ## About This Application
        
        Welcome to the **Airbnb Data Visualization and Analysis** app. This platform utilizes MongoDB Atlas and Streamlit to provide insights into Airbnb listings. Explore pricing trends, availability, and geographic distributions through interactive maps and charts.
        
        ### Key Features:
        
        - **Data Retrieval:** Connects seamlessly to MongoDB Atlas for data access.
        - **Visualization:** Interactive maps and dynamic charts for exploring Airbnb data.
        - **Analysis:** Price trends, seasonal availability, and location-based insights.
        - **User Experience:** Simple filters for customized data exploration.
        
        ### How to Use:
        
        Explore the data, analyze trends, and gain insights into Airbnb listings effortlessly with our intuitive interface.
        
        ### Acknowledgments:
        
        - **Data Source:** Provided by Airbnb.
        - **Technologies:** MongoDB Atlas, Streamlit, Python libraries (Pandas, Plotly).
    """)

#*************************************  FINISH  *****************************************************************************







            