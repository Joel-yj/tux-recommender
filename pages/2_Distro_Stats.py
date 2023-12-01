import streamlit as st
import pandas as pd
import json
import geopandas as gpd
import plotly.express as px
import ast
import plotly.graph_objects as go
import networkx as nx
from collections import defaultdict

st.set_page_config(page_title="Distro Stats", layout="wide")
st.sidebar.image("assets/tux.png",caption="Find your right LINUX system")

st.title("📊Distro Stats - openSUSE")
st.image("assets/logos/opensuse.png", width=100)
geodf = pd.read_csv("Homepage.csv")
geodf['Origins'] = geodf['Origins'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
geodf['Bases'] = geodf['Bases'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


############################# POPULARITY GRAPH ########################################
# Load the data from the provided files
file_paths = {
    "1 Week Ago": 'distro_timeline/top_distros_1_week_ago.json',
    "1 Month Ago": 'distro_timeline/top_distros_1_month_ago.json',
    "3 Months Ago": 'distro_timeline/top_distros_3_months_ago.json',
    "6 Months Ago": 'distro_timeline/top_distros_6_months_ago.json',
    "12 Months Ago": 'distro_timeline/top_distros_12_months_ago.json',
    "2022": 'distro_timeline/top_distros_2022.json',
    "2021": 'distro_timeline/top_distros_2021.json',
    "2020": 'distro_timeline/top_distros_2020.json',
    "2019": 'distro_timeline/top_distros_2019.json',
    "2018": 'distro_timeline/top_distros_2018.json',
    "2017": 'distro_timeline/top_distros_2017.json',
    "2016": 'distro_timeline/top_distros_2016.json',
    "2015": 'distro_timeline/top_distros_2015.json',
    "2014": 'distro_timeline/top_distros_2014.json',
    "2013": 'distro_timeline/top_distros_2013.json',
    "2012": 'distro_timeline/top_distros_2012.json',
    "2011": 'distro_timeline/top_distros_2011.json',
    "2010": 'distro_timeline/top_distros_2010.json',
    "2009": 'distro_timeline/top_distros_2009.json',
    "2008": 'distro_timeline/top_distros_2008.json',
    "2007": 'distro_timeline/top_distros_2007.json',
    "2006": 'distro_timeline/top_distros_2006.json',
    "2005": 'distro_timeline/top_distros_2005.json',
    "2004": 'distro_timeline/top_distros_2004.json',
    "2003": 'distro_timeline/top_distros_2003.json',
    "2002": 'distro_timeline/top_distros_2002.json',
}

# Read and parse the JSON data from each file
data = {}
for time_period, path in file_paths.items():
    with open(path, 'r') as file:
        data[time_period] = json.load(file)

# Convert the data to a more usable format
# Creating a DataFrame for each time period
df_list = []
for time_period, distros in data.items():
    df = pd.DataFrame(distros)
    df.set_index('distribution', inplace=True)
    df.drop(columns=['id'], inplace=True)
    df.rename(columns={'page hit(s)': time_period}, inplace=True)
    df_list.append(df)

# Merging the dataframes into a single one for analysis
merged_df = pd.concat(df_list, axis=1, sort=False)
top_distributions = merged_df['1 Month Ago'].sort_values(ascending=False).head(15).index

# Filtering data for only top distributions
filtered_df = merged_df.loc[top_distributions]

# Reversing the columns to have the oldest data first
filtered_df = filtered_df.iloc[:, ::-1]

# Assuming 'filtered_df_revised' is the DataFrame you have prepared
# Transpose the DataFrame for easier plotting with Plotly
plotly_df = filtered_df.transpose()

# Creating a Plotly line chart
fig = px.line(plotly_df, x=plotly_df.index, y=plotly_df.columns,
              labels={'value': 'Page Hits', 'variable': 'Distribution'},
              title='Popularity Timeline of Top 15 Current Linux Distributions from 2002 - 1 week ago')

# Adding hover data
fig.update_traces(mode='lines+markers', hoverinfo='all')
fig.update_traces(line=dict(width=4, color='lightgreen'), selector=dict(name='openSUSE'))
for column in plotly_df.columns[0:]:
    if column != 'openSUSE':
        fig.update_traces(opacity=0.4, selector=dict(name=column))

# Updating layout for better readability
fig.update_layout(xaxis_title='Time Period',
                  yaxis_title='Page Hits',
                  legend_title='Distribution',
                  xaxis_tickangle=-45)

st.plotly_chart(fig,use_container_width=True)

############################# GEOMAP ########################################

# Flatten the list of origins and count the number of distributions per origin
origin_counts = pd.Series([origin for sublist in geodf['Origins'].dropna() for origin in sublist]).value_counts()

origin_counts.head()
# Load the world map data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Mapping each country name to its central coordinates
country_coords = world.set_index('name')['geometry'].centroid
country_coords = country_coords.to_crs(epsg=4326)  # Convert to latitude/longitude

# Create a dataframe for the geospatial data
geo_data = pd.DataFrame([{'Country': country, 'Count': origin_counts[country], 
                          'Latitude': country_coords.loc[country].y, 
                          'Longitude': country_coords.loc[country].x} 
                         for country in origin_counts.index if country in country_coords.index])

geo_data['Color'] = geo_data['Country'].apply(lambda x: 'green' if x == 'Germany' else 'blue')

geofig = px.scatter_geo(geo_data,
                     lat='Latitude',
                     lon='Longitude',
                     size='Count',  # Adjusts the size of the point based on the count
                     hover_name='Country',  # Shows the country name on hover
                     color='Color',     
                     projection='natural earth',
                     title='Geospatial Distribution of Linux Distributions',
                     color_discrete_map={'green': 'green', 'blue': 'blue'})
                     

geofig.update_coloraxes(colorbar_title='Color')
st.plotly_chart(geofig,use_container_width=True)



############################# NODE GRAPH ########################################


# Create a dictionary to hold the tree structure
tree = defaultdict(list)

# Populate the tree with parent-child relationships
for index, row in geodf.iterrows():
    child = row['Name']
    bases = row['Bases']
    if not bases:  # If no base, it's a root
        tree[None].append(child)
    else:
        for base in bases:
            tree[base].append(child)

def add_nodes(graph, parent, children):
    for child in children:
        graph.add_node(child)
        if parent is not None:
            graph.add_edge(parent, child)
        add_nodes(graph, child, tree[child])

# Create a networkx graph from the tree
G = nx.DiGraph()
add_nodes(G, None, tree[None])

# Get positions for the nodes in G
pos = nx.spring_layout(G, seed=42)

# Create Edges
edge_x = []
edge_y = []
annotations = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

    # Create an annotation with an arrow
    annotations.append(dict(
        ax=x0, ay=y0, axref='x', ayref='y',
        x=x1, y=y1, xref='x', yref='y',
        showarrow=True,
        arrowhead=3, arrowsize=2, arrowwidth=1, arrowcolor='grey'))

# Create Nodes
node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

# Create figure
gofig = go.Figure()

node_of_interest = 'openSUSE'  # Replace with the node you're interested in

# Find the adjacent nodes to the node of interest
adjacent_nodes = list(G.neighbors(node_of_interest))
node_colors = ['green' if node == 'openSUSE' else 'yellow' if node in adjacent_nodes else 'blue' for node in G.nodes()]

# Add edges as scatter trace
gofig.add_trace(go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='green'),
    hoverinfo='none',
    mode='lines'))

# Add nodes as scatter trace
gofig.add_trace(go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    text=[node for node in G.nodes()],  # Node names as hover text
    hovertext=[node for node in G.nodes()],  # Node names as hover text
    marker=dict(
        showscale=False,
        color=node_colors,
        size=20,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2)))

# Update plot layout with annotations
gofig.update_layout(
    title='Interactive Network of Linux Distributions',
    titlefont_size=16,
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20,l=5,r=5,t=40),
    annotations=annotations,
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

st.plotly_chart(gofig,use_container_width=True)



############################# BAR GRAPH ########################################
if geodf['Ratings'].dtype == object:
    geodf['Ratings'] = geodf['Ratings'].str.replace('[\[\]\']', '', regex=True).astype(float)
elif geodf['Ratings'].dtype in [float, int]:
    # Ratings are already in numeric format
    pass
else:
    raise ValueError("The 'Ratings' column is not in a recognized format.")


# Calculate average ratings for Linux Mint and other distributions
openSUSE_rating_avg = geodf[geodf['Name'] == 'openSUSE']['Ratings'].mean()
other_ratings_avg = geodf[geodf['Name'] != 'openSUSE']['Ratings'].mean()

# Data for plotting
ratings_data = {
    'Distribution': ['openSUSE', 'Other Distributions'],
    'Average Rating': [openSUSE_rating_avg, other_ratings_avg]
}

# Create the bar plot
barfig = px.bar(
    ratings_data, 
    x='Distribution', 
    y='Average Rating', 
    color='Distribution',
    color_discrete_map={'openSUSE': 'green', 'Other Distributions': 'red'},
    title='Average Ratings: openSUSE vs Other Distributions'
)

# Display the plot
st.plotly_chart(barfig,use_container_width=True)



# Load your JSON data (already done in your case)
data = pd.read_json("Versions/features_opensuse.json")


# Convert the data to a DataFrame
df = pd.DataFrame(data)

# Select the columns to display
columns_to_display = ['version', 'release_date', 'price','processor_architecture','package_management', 'download_link']
df_display = df[columns_to_display]

# Display the table
st.dataframe(df_display)
