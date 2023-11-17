import weaviate
import json

client = weaviate.Client("http://localhost:8080")


response = (
    client.query.get('Versions', ['version', 'distribution_name'])
    # .with_near_vector(data_object)  # performs vector-wise semantic search (weaviate does this)
    .with_limit(5)
    # .with_additional(['distance', 'id'])
    .do()

)

print(json.dumps(response, indent=2))

