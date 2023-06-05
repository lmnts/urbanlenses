import requests
import json

# Replace this with the identifier for the dataset you're interested in
dataset_identifier = 'your-dataset-identifier'

url = f'https://data.seattle.gov/resource/{dataset_identifier}.json'

# If the dataset is large, you might want to include a `$limit` parameter in your request
# Here's how you can query for the first 1000 records
params = {
    '$limit': 1000
}

response = requests.get(url, params=params)

# Make sure the request was successful
response.raise_for_status()

# Parse the data from the response
data = response.json()

# Now you can work with the data...
for record in data:
    print(record)