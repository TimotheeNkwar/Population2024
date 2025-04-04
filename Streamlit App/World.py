# Import useful libraries
import plotly.express as px
import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(layout="wide")
st.title("World Data")

# Load data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("World Population by country 2024.csv")  # path to your CSV file
    except FileNotFoundError:
        st.error("Fichier CSV introuvable. Vérifiez qu'il est bien dans votre repo GitHub.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found

data = load_data()

if data.empty:
    st.stop()  # Stop execution if data is not loaded

st.write("Overview of data:", data.head())

# --- Sidebar: Top 5 Most Populous Countries ---
st.sidebar.subheader("Top 5 Most Populous Countries")
top_Country = ["INDIA", "CHINA", "USA", "INDONESIA", "PAKISTAN"]

if "Country_choose" not in st.session_state:
    st.session_state["Country_choose"] = "INDIA"  # defaut value

for i, country in enumerate(top_Country):
    if st.sidebar.button(f"{i+1}. {country}"):
        st.session_state["Country_choose"] = country  # Mupdate the selection

# --- BODY ---
col_left, col_center, col_right = st.columns([1, 2, 1])

# Country selection

with col_left:
    st.subheader("Select a Country")
    Country_choose = st.selectbox("Select a country:", data["Country"])

    # Update session state with selected country
    st.session_state["Country_choose"] = Country_choose

    # Get the index of the selected country in the dataframe
    index = data.index[data["Country"] == st.session_state["Country_choose"]].tolist()[0]

# Country statistics
with col_right:
    st.subheader(f"Statistics of {Country_choose}")
    Country_data = data[data["Country"] == Country_choose]
    
    if not Country_data.empty:
        st.metric("Population 2024", f"{Country_data['Population 2024'].values[0]:,}")
        st.metric("Density (hab/km²)", f"{Country_data['Density (/km2)'].values[0]:,}")
     
        st.metric("Growth Rate", f"{Country_data['Growth Rate'].values[0]}%")
        st.metric("World %", f"{Country_data['World %'].values[0]}%")
        st.metric("World Rank", f"{Country_data['World Rank'].values[0]}")

# --- MAP Highlighting Selected Country ---
with col_center:
    data["highlight"] = data["Country"].apply(lambda x: 1 if x == Country_choose else 0)

    fig = px.choropleth(
        data,                     
        locations="Country",            
        locationmode="country names",
        color="highlight",
        hover_name="Country",
        hover_data={
            "Population 2024": True,
            "Population 2023": True,
            "Area (km2)": True,
            "Density (/km2)": True,
            "Growth Rate": True,
            "World %": True
        },
        title="Selected Country Highlighted",
        color_continuous_scale=["lightgray", "yellow"]
    )

    fig.update_geos(projection_type="orthographic")
    fig.update_layout(width=1200, height=1000)
    st.plotly_chart(fig, use_container_width=True)

# --- WORLD POPULATION MAP ---
with col_center:
    fig = px.choropleth(
        data,                     
        locations="Country",            
        locationmode="country names",
        color="Population 2024",
        hover_name="Country",
        hover_data={"Population 2024": True},
        title="Population of the World (2024)",
        color_continuous_scale="inferno_r"
    )

    fig.update_geos(projection_type="orthographic")
    fig.update_layout(width=1200, height=1000)
    st.plotly_chart(fig, use_container_width=False)
