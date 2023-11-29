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
df1 = pd.read_csv("Homepage.csv")
df1 = df1.drop(columns=["Unnamed: 0"])
feature_names = pd.read_json("Versions/features_absolute.json")
feature_names = feature_names.columns.tolist()
df2 = pd.read_csv("final_cluster9.csv")



# Sidebars
st.sidebar.image("assets/tux.png",caption="Find your right LINUX system")

# Main page
st.subheader("Find your Linux System") 

# Search Bar for distribution
distribution_names = st_searchbox(
    placeholder="Search for your distribution:", 
    key="searchbox", 
    search_function=search_distro,
    default_options=df1["Name"].values.tolist(),
    )
if distribution_names != None:
    distribution_id = df1[df1["Name"].str.contains(distribution_names, case=False)]["ID"].values[0]

    # getting the distributions from the search
    cal_distr = calista_search(distribution_id)
    chae_distr = chae_search(distribution_id)
    st.write(cal_distr)
    st.write(chae_distr)
    # Perform intersection of distribution names in cal_distr and chae_distr

    distro_dict = {item1['distro']: item1 for item1 in cal_distr}
    matching_distributions = []
    for item2 in chae_distr:
        distro_id = item2["ids"]
        if distro_id in distro_dict:
            matching_distributions.append(item2)
    


top10_distros = st.button("Recommend")
if top10_distros:
    st.write("Top 10 distros")
    st.write(matching_distributions)
# Filter by features
#TODO Enable user to filter according to package/version from distribution found
#TODO Enable user to input text to filter the attributes and return the distribution






# st.subheader("Filter by Features")
# features = st.multiselect("Features", options=feature_names, default=feature_names[0])
# col1,col2 = st.columns(2)
# for feature in features:
#     with col1:
#         st.write(feature)
#     with col2:
#         st.text_input(f"Search for {feature}:",value=None)

# search = st.text_input("Search for feature:",value=None)

# if search == None:
#     st.write("No results found")
# else:
#     response = feature_filter(search, features)
#     st.write(response)



# # Choosing a Distribution
# if results != None:
#     filtered_df = df[df["Name"].str.contains(results, case=False)]
#     # st.write(filtered_df) 
#     st.title(filtered_df["Name"].values[0])
#     st.markdown("###")
#     image_path = "assets/logos/" + filtered_df["ID"].values[0] + ".png"
#     st.image(image_path, width=200)
#     st.write("**Popularity Rank**: " + filtered_df["Popularities"].values[0].strip("[]").strip("'"))
#     st.write("**Ratings**: " + filtered_df["Ratings"].values[0][2:6])
#     description = filtered_df["Description"].values[0]
#     st.write(f'<div style="text-align: justify;">{description}</div>', unsafe_allow_html=True)
#     st.markdown("###")
#     homepage = filtered_df["Homepage"].to_string(index=False)
#     st.write("**Homepage**: "+homepage.strip("[]").strip("'"))
#     st.write("**Architectures**: "+filtered_df["Architectures"].values[0].strip("[]"))
#     st.write("**OS Types**: "+filtered_df["Os Types"].values[0].strip("[]").strip("'"))
#     st.write("**Bases**: "+filtered_df["Bases"].values[0].strip("[]").strip("'"))
    









# testing the weaviate connection
# st.button("weaviate_test", on_click=weaviate_test())
