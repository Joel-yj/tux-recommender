import plotly.express as px

# Assuming 'filtered_df_revised' is the DataFrame you have prepared
# Transpose the DataFrame for easier plotting with Plotly
plotly_df = filtered_df.transpose()

# Creating a Plotly line chart
fig = px.line(plotly_df, x=plotly_df.index, y=plotly_df.columns,
              labels={'value': 'Page Hits', 'variable': 'Distribution'},
              title='Popularity Timeline of Top Linux Distributions')

# Adding hover data
fig.update_traces(mode='lines+markers', hoverinfo='all')

# Updating layout for better readability
fig.update_layout(xaxis_title='Time Period',
                  yaxis_title='Page Hits',
                  legend_title='Distribution',
                  xaxis_tickangle=-45)

fig.show()