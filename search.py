import weaviate
import json

client = weaviate.Client('http://localhost:8080')

# to get object id from inputted distribution name
def get_object_id(input):
    response = (
        client.query.get('Distributions', ['name', 'description'])
        .with_where({"path": "name", "operator": "Equal", "valueString": input})
        .with_additional(['id'])
        .do()
    )
    # get distribution id from response
    distribution_id =  response['data']['Get']['Distributions'][0]['_additional']['id']

    return distribution_id


data_object = client.data_object.get_by_id(
            get_object_id('Rocky'),
            class_name='Distributions',
            with_vector=True
        )

response = (
    client.query.get('Distributions', ['name', 'description'])
    .with_near_vector(data_object)  # performs vector-wise semantic search (weaviate does this)
    .with_limit(5)
    .with_additional(['distance', 'id'])
    .do()

)

print(json.dumps(response, indent=2))

