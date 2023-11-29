import pandas as pd
import streamlit as st
import weaviate 
import json

client = weaviate.Client('http://localhost:8080')

def search_distro(searchterm:str):
    df = pd.read_csv("Homepage.csv")
    df = df[df['Name'].str.contains(searchterm,case=False)]

    
def weaviate_test():
    response = (
    client.query.get('Versions', ['version', 'distribution_name'])
    # .with_near_vector(data_object)  # performs vector-wise semantic search (weaviate does this)
    .with_limit(5)
    # .with_additional(['distance', 'id'])
    .do()
    )
    print(json.dumps(response, indent=2))

def feature_filter(search:str, feature:list):
    outputs = feature + ["distribution_name"]
    response = (
    client.query
    .get("Versions", outputs)
    .with_where({
        "path": feature,
        "operator": "Like",
        "valueText": f"*{search}*"
    })
    .with_limit(3)
    .do()
    )
    return response
    
def calista_search(distro_key:str):
    if distro_key == None:
        return None
    else:
        try:
            res = (
            client.query
            .get("Cluster", "cluster_label")
            .with_where({
                "path": ["distro"],
                "operator": "Equal",
                "valueString": distro_key
            })
            .with_limit(1)
            .do()
            )
            cluster_num = res["data"]["Get"]["Cluster"][0]["cluster_label"]
            where_filter = {
                "operator": "And",
                "operands":[{
                    "path": ["cluster_label"],
                    "operator": "Equal",
                    "valueNumber": cluster_num
                    }, {
                    "path": ["distro"],
                    "operator": "NotEqual",
                    "valueString": distro_key
                }]
            }
            response =  (client.query
                .get("Cluster", ["distro", "rating", "cluster_label"])
                .with_where(where_filter)
                .with_limit(10)
                .with_sort({
                    'path': ['rating'],
                    'order': 'desc',
                })
                .do())
            return response['data']['Get']['Cluster'][:10]
        except:
            return "No results found"
        
def chae_search(distr_name):

    data_object = client.data_object.get_by_id(
                get_object_id(distr_name),
                class_name='Distributions',
                with_vector=True
            )

    response = (
        client.query.get('Distributions', ['name', 'description', 'ids', 'homepage', 'popularity', 'rating'])
        .with_near_vector(data_object)  # performs vector-wise semantic search (weaviate does this)
        .with_limit(10)
        .with_additional(['distance', 'id'])
        .do()
    )
    return response['data']['Get']['Distributions'][:10]

def get_object_id(input):
    response = (
        client.query.get('Distributions', ['name', 'description', 'ids', 'homepage', 'popularity', 'rating'])
        .with_where({"path": "name", "operator": "Equal", "valueString": input})
        .with_additional(['id'])
        .do()
    )
    # get distribution id from response
    distribution_id =  response['data']['Get']['Distributions'][0]['_additional']['id']

    return distribution_id