import weaviate
import json
from weaviate.util import generate_uuid5

client = weaviate.Client("http://localhost:8080")

distribution_class_schema = {
    # name of class
    "class" : "Distribution",
    # description
    "description" : "Distribution and their versions",
    # class properties
    "properties": [
        {
            "name": "distributionName",
            "dataType" : ["string"],
            "description" : "Name of distribution",
        },
        {
            "name" : "versions",
            "dataType" : ["Versions"],
            "description" : "Versions of distribution",
        }
    ]
}

version_class_schema = {
    "class" : "Versions",
    "description" : "Versions of distribution",
    "properties" : [
        {
            "name" : "version",
            "dataType" : ["string"],
            "description" : "Version of distribution",
        },
        {
            "name" : "releaseDate",
            "dataType" : ["string"],
            "description" : "Release date of distribution",
        },
        {
            "name" : "endOfLifeDate",
            "dataType" : ["string"],
            "description" : "End of life date of distribution",
        },
        {
            "name" : "price",
            "dataType" : ["string"],
            "description" : "Price of distribution",
        },
        {
            "name": "imageSize",
            "dataType": ["string"],
            "description": "Image Size in MB"
        },
        {
            "name": "freeDownload",
            "dataType": ["string"],
            "description": "Link to Free Download"
        },
        {
            "name": "installation",
            "dataType": ["string"],
            "description": "Installation Method"
        },
        {
            "name": "defaultDesktop",
            "dataType": ["string"],
            "description": "Default Desktop Environment"
        },
        {
            "name": "packageManagement",
            "dataType": ["string"],
            "description": "Package Management System"
        },
        {
            "name": "releaseModel",
            "dataType": ["string"],
            "description": "Release Model"
        },
        {
            "name": "officeSuite",
            "dataType": ["string"],
            "description": "Office Suite Software"
        },
        {
            "name": "processorArchitecture",
            "dataType": ["string"],
            "description": "Processor Architecture"
        },
        {
            "name": "initSoftware",
            "dataType": ["string"],
            "description": "Init Software"
        },
        {
            "name": "journaledFileSystems",
            "dataType": ["string"],
            "description": "Journaled File Systems"
        },
        {
            "name": "multilingual",
            "dataType": ["string"],
            "description": "Multilingual Support"
        },
        {
            "name": "asianLanguageSupport",
            "dataType": ["string"],
            "description": "Asian Language Support"
        },
        {
            "name": "numberOfPackages",
            "dataType": ["string"],
            "description": "Number of Packages"
        }
    ]
}

client.schema.delete_all()
client.schema.create_class(version_class_schema)
client.schema.create_class(distribution_class_schema)
# print(client.schema.get())


def add_distribution(batch, distribution_data):
    distribution_obj = {
        'distributionName' : distribution_data['Distribution Name'],
        'versions' : distribution_data['Versions']
    }
    distr_id = generate_uuid5(distribution_obj)
    batch.add_data_object(
        data_object= distribution_obj,
        class_name= "Distribution",
        uuid = distr_id,
    )
    return distr_id

def add_version(batch,distr_name,version_data):
    version_obj = {
        'version' : version_data['Version'],
        'releaseDate' : version_data['Release Date'],
        'endOfLifeDate' : version_data['End of Life Date'],
        'price' : version_data['Price'],
        'imageSize' : version_data['Image Size'],
        'freeDownload' : version_data['Free Download'],
        'installation' : version_data['Installation'],
        'defaultDesktop' : version_data['Default Desktop'],
        'packageManagement' : version_data['Package Management'],
        'releaseModel' : version_data['Release Model'],
        'officeSuite' : version_data['Office Suite'],
        'processorArchitecture' : version_data['Processor Architecture'],
        'initSoftware' : version_data['Init Software'],
        'journaledFileSystems' : version_data['Journaled File Systems'],
        'multilingual' : version_data['Multilingual'],
        'asianLanguageSupport' : version_data['Asian Language Support'],
        'numberOfPackages' : version_data['Number of Packages']
    }
    batch.add_data_object(
        data_object= version_obj,
        class_name= "Versions",
        uuid = generate_uuid5(version_obj),
        reference = distr_name
    )

with open('data/debian_plus_arch.json','rb') as f:
    data = json.load(f)

client.batch.configure(batch_size=100)

with client.batch as batch:
    for i,d in enumerate(data):
        distr_id = add_distribution(batch,d)
        print(distr_id)
        for v in d['Versions']:
            add_version(batch,distr_id,v)
        if i % 100 == 0:
            print(f'Processed {i} distributions')
            