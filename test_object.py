import weaviate

client = weaviate.Client("http://localhost:8080")

response = (
    client.query
    .get("Debian", ["price"])
    .with_limit(1)
    .do()
)
print(response)

