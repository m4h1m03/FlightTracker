# Fetches a snapshot of current flights from the OpenSky Network API.
import requests
import json

response = requests.get('https://opensky-network.org/api/states/all')
response_dict = response.json()
# print(response_dict.keys())
# print(response_dict['states'][0])

# The first 5 flights

flights = response_dict['states'][0:5]
for flight in flights:
    if flight[1] is not None:
        flight[1] = flight[1].strip()
    print(flight)
        
    
