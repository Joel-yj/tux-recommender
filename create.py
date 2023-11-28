import weaviate
import pandas as pd
from weaviate.util import generate_uuid5


client = weaviate.Client('http://localhost:8080')

client.schema.delete_class('Distributions')
# client.schema.delete_class('Distribution')

class_obj = {
    "class": "Distributions",
    "description": "A class to implement distribution descriptions",
    "moduleConfig": {
        "text2vec-transformers": {
            "vectorizeClassName": "false"
        }
    },
    "properties": [{
        "dataType": ["string"],
        "name": "name",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true"   
            }
        },
        "description": "name of distribution"
    },
    {
        "dataType": ['string'],
        "name": "ids",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true"   
            }
        },
        "description": "id of distribution"
    },
    {
        "dataType": ["string"],
        "name": "description",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "false"  # only vectorize description so that later search is done between descriptions
            }
        },
        "description": "description of distribution"
    },
    {
        "dataType": ["string"],
        "name": "homepage",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true" 
            }
        },
        "description": "homepage link of distribution"
    },
    {
        "dataType": ["string"],
        "name": "popularity",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true" 
            }
        },
        "description": "popularity of distribution"
    },
    {
        "dataType": ["string"],
        "name": "rating",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true" 
            }
        },
        "description": "rating of distribution"
    }
    ]
}

data = pd.read_csv('Homepage.csv')
class_name = "Distributions"

data_objs = []
for i,row in data.iterrows():
    obj = {"name": data['Name'][i],
    "ids": data['ID'][i],
    "description": data['Description'][i],
    "homepage": data['Homepage'][i],
    "popularity": data['Popularities'][i],
    "rating": data['Ratings'][i]}
    data_objs.append(obj)

client.batch.configure(batch_size=10)

with client.batch as batch:
    for data_obj in data_objs:
        try:
            batch.add_data_object(
                data_obj,
                class_name,
                uuid=generate_uuid5(data_obj)
            )
            print(f"Added object with name: {data_obj['name']}")
        except Exception as e:
            print(f"Error adding object with name {data_obj['name']}. Error: {e}")