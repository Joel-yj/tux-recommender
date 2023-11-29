import weaviate
from weaviate.util import generate_uuid5
import pandas as pd
import json
import numpy as np

client = weaviate.Client(
    url = "http://localhost:8080",  # Replace with your endpoint
    # additional_headers = {
    #     "X-OpenAI-Api-Key": "YOUR-OPENAI-API-KEY"  # Replace with your inference API key
    # }
)

client.schema.delete_class('Cluster')
class_obj = {
    "class": "Cluster",
    "vectorizer": "none",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {}
}

client.schema.create_class(class_obj)

data = pd.read_csv('final_cluster9.csv')
data_objs = []
for i,row in data.iterrows():
    obj = {"distro": str(data['distro'][i]),
           "rating": float(data['rating'][i]),
           "votes": float(data["votes"][i]),
           "cluster_label":int(data["cluster_label"][i])
        }  
    data_objs.append(obj)

client.batch.configure(batch_size=100)

class_name = "Cluster"
with client.batch as batch:
    for data_obj in data_objs:
        try:
            batch.add_data_object(
                data_obj,
                class_name,
                uuid=generate_uuid5(data_obj),
            )
            print(f"Added object with name: {data_obj['distro']}")
        except Exception as e:
            print(f"Error adding object with name {data_obj['distro']}. Error: {e}")


# query to return a response with a list of distros in the same cluster
distro_key = "mabox"
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
# print(json.dumps(res, indent=2))
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

response = (
    client.query
    .get("Cluster", ["distro", "rating", "cluster_label"])
    .with_where(where_filter)
    .with_limit(10)
    .with_sort({
        'path': ['rating'],
        'order': 'desc',
    })
    .do()
)

print(json.dumps(response, indent=2))
if len(response["data"]["Get"]["Cluster"]) == 0:
    print("No results returned.")

# with open('sample_output.json', 'w') as fp:
#     json.dump(response, fp)