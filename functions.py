import pandas as pd
import streamlit as st
import weaviate 
import json

# client = weaviate.Client('http://localhost:8080')

def search_distro(searchterm:str):
    df = pd.read_csv("Homepage.csv")
    if searchterm:
        df = df[df['Name'].str.contains(searchterm,case=False)]
        return df["Name"]
    else:
        return []
    
# def weaviate_test():
#     response = (
#     client.query.get('Versions', ['version', 'distribution_name'])
#     # .with_near_vector(data_object)  # performs vector-wise semantic search (weaviate does this)
#     .with_limit(5)
#     # .with_additional(['distance', 'id'])
#     .do()
#     )
#     print(json.dumps(response, indent=2))


def feature_filter(search:str, feature:list):
    outputs = feature + ["distribution_name"]
    response = (
    # client.query
    # .get("Versions", outputs)
    # .with_where({
    #     "path": feature,
    #     "operator": "Like",
    #     "valueText": f"*{search}*"
    # })
    # .with_limit(3)
    # .do()
    )
    
    return response
    