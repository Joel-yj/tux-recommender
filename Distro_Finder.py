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


st.sidebar.image("assets/tux.png",caption="Find your right LINUX system")

df = pd.read_csv("Homepage.csv")
df = df.drop(columns=["Unnamed: 0"])
# Search Bar and version input
#TODO some of the user input text is not being properly shown in the searchbox
results = st_searchbox(placeholder="Search for your distribution:", key="searchbox", search_function=search_distro,)

# Can show all the features of the distribution
if results == None:
    st.write("No results found")
else: 
    st.table(df.loc[df["Name"] == results])


#TODO Enable user to filter according to package/version from distribution found

st.button("Search", on_click=weaviate_find())



    

