import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Streamlit App title
st.title("Tennis Data Explorer")

# Database connection parameters
DB_USER = "postgres"
DB_PASSWORD = "Daxra369"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "Tennisdata"

# Connect to PostgreSQL
@st.cache_resource
def get_connection():
    return create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Fetch data using a query
@st.cache_data
def fetch_data(query):
    with get_connection().connect() as connection:
        return pd.read_sql_query(query, connection)

# Add image to page
def add_image(image_path, caption=None):
    st.image(image_path, caption=caption, use_container_width=True)


# Filter data based on user selection
def apply_filter(df, column_name, filter_options, filter_label):
    selected_value = st.sidebar.selectbox(f"Select {filter_label}", ['All'] + list(filter_options))
    if selected_value != 'All':
        df = df[df[column_name] == selected_value]
    return df

# Display image at the top of the sidebar
image_path = r"C:\Users\Admin\OneDrive\Desktop\Analysis.jpg"  
st.sidebar.image(image_path, width=300)  # Adjust width as needed

# Sidebar navigation
page = st.sidebar.radio("Select a Page to Explore", [
    "Homepage", "Filter Competitors", "Competitor Details", "Country-Wise Analysis", 
    "Leaderboards", "Competitions Filter", "Venues Filter"
])

# Homepage
if page == "Homepage":
    add_image("C:/Users/Admin/OneDrive/Desktop/Tenniimage.jpg", "Welcome to Tennis Data Explorer")

    st.header("Homepage Dashboard Summary")
    competitors_df = fetch_data("SELECT competitor_id, competitor_country FROM competitors")
    highest_points_df = fetch_data("SELECT points FROM competitor_rankings")
    
    total_competitors = len(competitors_df)
    total_countries = competitors_df['competitor_country'].nunique()
    highest_points = highest_points_df['points'].max()

    st.subheader("Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Competitors", total_competitors)
    col2.metric("Countries Represented", total_countries)
    col3.metric("Highest Points", highest_points)

# Filter Competitors
elif page == "Filter Competitors":
    st.header("Filter Competitors")
    data_df = fetch_data("""
        SELECT c.competitor_id, c.competitor_name, c.competitor_country, cr.points, cr.rank, cr.year, cr.week, cr.gender
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
    """)

    # Apply filters
    data_df = apply_filter(data_df, 'competitor_name', data_df['competitor_name'].unique(), 'Competitor')
    data_df = apply_filter(data_df, 'rank', range(1, 101), 'Rank')
    data_df = apply_filter(data_df, 'competitor_country', data_df['competitor_country'].unique(), 'Country')
    data_df = apply_filter(data_df, 'points', range(int(data_df['points'].min()), int(data_df['points'].max()) + 1), 'Points')
    data_df = apply_filter(data_df, 'year', data_df['year'].unique(), 'Year')
    data_df = apply_filter(data_df, 'week', data_df['week'].unique(), 'Week')
    data_df = apply_filter(data_df, 'gender', data_df['gender'].unique(), 'Gender')

    st.write(data_df)

# Competitor Details
elif page == "Competitor Details":
    st.header("Competitor Details")
    competitor_names = fetch_data("""
        SELECT competitor_name FROM competitors
    """)['competitor_name'].unique()
    selected_competitor = st.sidebar.selectbox("Select a Competitor", competitor_names)
    
    details_df = fetch_data(f"""
        SELECT c.competitor_name, cr.rank, cr.movement, cr.competitions_played, c.competitor_country
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
        WHERE c.competitor_name = '{selected_competitor}'
    """).iloc[0]
    
    st.subheader(f"Details for {selected_competitor}")
    st.write(f"**Rank**: {details_df['rank']}")
    st.write(f"**Movement**: {details_df['movement']}")
    st.write(f"**Competitions Played**: {details_df['competitions_played']}")
    st.write(f"**Country**: {details_df['competitor_country']}")

# Country-Wise Analysis
elif page == "Country-Wise Analysis":
    st.header("Country-Wise Analysis")

    # Fetch country-wise analysis data directly using SQL
    country_analysis_query = """
    SELECT c.competitor_country, COUNT(c.competitor_id) AS total_competitors, AVG(cr.points) AS average_points
    FROM competitors c
    JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
    GROUP BY c.competitor_country
    """
    
    # Fetch the data
    country_analysis = fetch_data(country_analysis_query)

    # Add dropdown to select a country or view all
    selected_country = st.sidebar.selectbox("Select a Country to View or 'All' for All Countries", ['All'] + list(country_analysis['competitor_country'].unique()))

    # If 'All' is selected, show the entire table
    if selected_country == 'All':
        st.write(country_analysis)
    else:
        # Otherwise, filter the table by the selected country
        selected_country_analysis = country_analysis[country_analysis['competitor_country'] == selected_country]
        st.write(selected_country_analysis)

# Leaderboards
elif page == "Leaderboards":
    st.header("Leaderboards")
    leaderboard_type = st.sidebar.radio("Select Leaderboard Type", ["Top Ranked Competitors", "Competitors with Highest Points"])
    num_competitors = st.sidebar.slider("Select Number of Competitors to Display", 5, 50, 10, 5)
    
    if leaderboard_type == "Top Ranked Competitors":
        leaderboard_query = f"""
            SELECT c.competitor_name, cr.rank, cr.points
            FROM competitors c
            JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
            ORDER BY cr.rank ASC
            LIMIT {num_competitors}
        """
    else:
        leaderboard_query = f"""
            SELECT c.competitor_name, cr.rank, cr.points
            FROM competitors c
            JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
            ORDER BY cr.points DESC
            LIMIT {num_competitors}
        """
    
    leaderboard_df = fetch_data(leaderboard_query)
    st.write(leaderboard_df)

# Competitions Filter
elif page == "Competitions Filter":
    st.header("Competitions Filter")
    categories_df = fetch_data("SELECT category_id, category_name FROM categories")
    competitions_df = fetch_data("SELECT competition_name, type, gender, category_id, level FROM competitions")

    selected_category = st.sidebar.selectbox("Select Category", ['All'] + list(categories_df['category_name'].unique()))
    if selected_category != 'All':
        category_id = categories_df[categories_df['category_name'] == selected_category]['category_id'].values[0]
        competitions_df = competitions_df[competitions_df['category_id'] == category_id]
    
    selected_type = st.sidebar.selectbox("Select Type", ['All'] + list(competitions_df['type'].unique()))
    if selected_type != 'All':
        competitions_df = competitions_df[competitions_df['type'] == selected_type]
    
    selected_gender = st.sidebar.selectbox("Select Gender", ['All'] + list(competitions_df['gender'].unique()))
    if selected_gender != 'All':
        competitions_df = competitions_df[competitions_df['gender'] == selected_gender]

    selected_level = st.sidebar.selectbox("Select Level", ['All'] + list(competitions_df['level'].unique()))
    if selected_level != 'All':
        competitions_df = competitions_df[competitions_df['level'] == selected_level]
    
    st.write(competitions_df)

# Venues Filter
elif page == "Venues Filter":
    st.header("Venues Filter")
    
    # Fetch complex and venue data
    complexes_df = fetch_data("SELECT complex_id, complex_name FROM complexes")
    venues_df = fetch_data("SELECT venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id FROM venues")
    
    # Filter by complex
    selected_complex = st.sidebar.selectbox("Select Complex", ['All'] + list(complexes_df['complex_name'].unique()))
    if selected_complex != 'All':
        complex_id = complexes_df[complexes_df['complex_name'] == selected_complex]['complex_id'].values[0]
        venues_df = venues_df[venues_df['complex_id'] == complex_id]
    
    # Filter by city
    selected_city = st.sidebar.selectbox("Select City", ['All'] + list(venues_df['city_name'].unique()))
    if selected_city != 'All':
        venues_df = venues_df[venues_df['city_name'] == selected_city]
    
    # Filter by country
    selected_country = st.sidebar.selectbox("Select Country", ['All'] + list(venues_df['country_name'].unique()))
    if selected_country != 'All':
        venues_df = venues_df[venues_df['country_name'] == selected_country]
    
    # Filter by venue
    selected_venue = st.sidebar.selectbox("Select Venue", ['All'] + list(venues_df['venue_name'].unique()))
    if selected_venue != 'All':
        venues_df = venues_df[venues_df['venue_name'] == selected_venue]
    
    # Show filtered data
    st.write(venues_df)
