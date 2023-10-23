import weaviate
import json


client = weaviate.Client("http://localhost:8080")

# Settings for displaying the import progress
counter = 0
interval = 20  # print progress every this many records; should be bigger than the batch_size

def add_debian_release(release_name, release_data):
    properties = {
        'Release_Date': release_data['Release Date'],
        'End_Of_Life': release_data['End Of Life'],
        'Price': release_data['Price (US$)'],
        'Image_Size': release_data['Image Size (MB)'],
        'Free_Download': release_data['Free Download'],
        'Installation': release_data['Installation'],
        'Default_Desktop': release_data['Default Desktop'],
        'Package_Management': release_data['Package Management'],
        'Release_Model': release_data['Release Model'],
        'Office_Suite': release_data['Office Suite'],
        'Processor_Architecture': release_data['Processor Architecture'],
        'Init_Software': release_data['Init Software'],
        'Journaled_File_Systems': release_data['Journaled File Systems'],
        'Multilingual': release_data['Multilingual'],
        'Asian_Language_Support': release_data['Asian Language Support'],
        'Number_of_Packages': release_data['Number of Packages'],
    }

    client.batch.configure(batch_size=100)  # Configure batch
    with client.batch as batch:
        # Add the object to the batch
        batch.add_data_object(
            data_object=properties,
            class_name='Debian',
            # If you Bring Your Own Vectors, add the `vector` parameter here
            # vector=obj.vector
        )


with open('data/debian.json', 'r') as json_file:
    data = json.load(json_file)
    for release_name, release_data in data.items():
        add_debian_release(release_name, release_data)

print('Importing Debian releases into Weaviate...')
client.batch.flush()
print('Finished importing Debian releases.')


response = (
    client.query
    .get("Debian", ["Release Date"])
    .with_limit(1)
    .do()
)
print(response)