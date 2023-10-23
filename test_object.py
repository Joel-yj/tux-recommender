import weaviate

client = weaviate.Client("http://localhost:8080")

response = (
    client.query
    .get("arch",["name"])
    .do()
)

print(response)

