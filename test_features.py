import weaviate
import pandas as pd
from weaviate.util import generate_uuid5


client = weaviate.Client('http://localhost:8080')

client.schema.delete_class('Features')
client.schema.delete_class('Distribution')
client.schema.delete_class('Distributions')

class_obj = {
    "class": "arch",
    "description": "A class to implement distribution descriptions",
    "moduleConfig": {
        "text2vec-transformers": {
            "vectorizeClassName": "false"
        }
    },
    "properties": [{
        "dataType": ["string"],
        "name": "name1",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "true"   
            }
        },
        "description": "feature of arch"
    },
    {
        "dataType": ["string"],
        "name": "name2",
        "moduleConfig": {
            "text2vec-transformers": {
                "skip": "false"  # only vectorize description so that later search is done between descriptions
            }
        },
        "description": "release date"
    }]
}

data = pd.read_json('data/arch.json')
class_name = "arch"

data_objs = []
for i,row in data.iterrows():
    obj = {"name1": data['Feature'][i],
     "name2": data['Free Download'][i]}
    data_objs.append(obj)

# client.batch.configure(batch_size=100)

with client.batch as batch:
    for data_obj in data_objs:
        try:
            batch.add_data_object(
                data_obj,
                class_name,
                uuid=generate_uuid5(data_obj)
            )
            print(f"Added object with name: {data_obj['name2']}")
        except Exception as e:
            print(f"Error adding object with name {data_obj['name2']}. Error: {e}")