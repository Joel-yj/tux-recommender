import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_searchbox import st_searchbox
import pandas as pd
from PIL import Image
from functions import *


# App title and logo
st.set_page_config(page_title="DistroFinder", page_icon="🏠", layout="wide")
st.title("🔍 DistroFinder ")
st.markdown("##")

# Load data
df = pd.read_csv("Homepage.csv")
df = df.drop(columns=["Unnamed: 0"])
feature_names = pd.read_json("Versions/features_absolute.json")
feature_names = feature_names.columns.tolist()


# Sidebars
st.sidebar.image("assets/tux.png",caption="Find your right LINUX system")

# Main page
st.subheader("Find your Linux System")



# Search Bar for distribution
results = st_searchbox(placeholder="Search for your distribution:", key="searchbox", search_function=search_distro,)

# Can show all the features of the distribution
if results == None:
    st.write("No results found")
else: 
    st.table(df.loc[df["Name"] == results])

# Filter by features
#TODO Enable user to filter according to package/version from distribution found
st.subheader("Filter by Features")
features = st.multiselect("Features", options=feature_names, default=feature_names[0])
col1,col2 = st.columns(2)
for feature in features:
    with col1:
        st.write(feature)
    with col2:
        st.text_input(f"Search for {feature}:",value=None)

search = st.text_input("Search for feature:",value=None)

if search == None:
    st.write("No results found")
else:
    response = feature_filter(search, features)
    st.write(response)

#TODO Enable user to input text to filter the attributes and return the distribution

#TODO UI mockup for the distribution homepage


# testing the weaviate connection
st.button("weaviate_test", on_click=weaviate_test())
