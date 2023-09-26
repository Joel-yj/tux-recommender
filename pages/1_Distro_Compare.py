import streamlit as st
import pandas as pd


st.set_page_config(page_title="Distro Compare", layout="wide")
st.sidebar.image("assets/tux.png",caption="Find your right LINUX system")
st.title("Distro Compare ")
st.markdown("##")

df = pd.read_csv("Homepage.csv")
df = df.drop(columns=["Unnamed: 0"])

# Filters to allow user to choose what fields to compare

st.sidebar.header("Please filter")

location=st.sidebar.multiselect(
    "Select Bases",
     options=df["Bases"].unique(),
     default=df["Bases"].unique(),
)
construction=st.sidebar.multiselect(
    "Select Desktops",
     options=df["Desktops"].unique(),
     default=df["Desktops"].unique(),
)

df_selection=df.query(
    "Bases==@location & Desktops ==@construction"
)

showData=st.multiselect('Filter: ',df_selection.columns,default=[])
st.dataframe(df_selection[showData],use_container_width=True)

# Use columns to display two distributions side by side
table1,table2 = st.columns(2, gap = "large")


with table1:
    st.table(df.loc[df["Name"] == "Ubuntu"][["Name","Desktops","Popularities"]])

with table2:
    st.table(df.loc[df["Name"] == "MX Linux"][["Name","Desktops","Popularities"]])