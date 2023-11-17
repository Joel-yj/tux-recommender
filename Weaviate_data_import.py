import weaviate
import json
from weaviate.util import generate_uuid5

client = weaviate.Client(
    "http://localhost:8080")

class_obj = {
    "class": "Versions",
    "vectorizer": "none",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {}
}

client.schema.delete_all()
client.schema.create_class(class_obj)


f = open('data/features_absolute.json')
data_objs = json.load(f)
f.close()
client.batch.configure(batch_size=100)

class_name = "Versions"
with client.batch as batch:
    for data_obj in data_objs:
        try:
            batch.add_data_object(
                data_obj,
                class_name,
                uuid=generate_uuid5(data_obj),
            )
            print(f"Added object with name: {data_obj['distribution_name']}")
        except Exception as e:
            print(f"Error adding object with name {data_obj['distribution_name']}. Error: {e}")
