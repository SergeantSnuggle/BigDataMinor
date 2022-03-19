
## https://www.dataquest.io/blog/python-api-tutorial/
import requests
# Make a get request to get the latest position of the international space station from the opennotify api.
response = requests.get("http://api.open-notify.org/iss-now.json")
# Print the status code of the response.
print(response.status_code)


response = requests.get("http://api.open-notify.org/iss-pass")
print(response.status_code)

# Set up the parameters we want to pass to the API.
# This is the latitude and longitude of New York City.
parameters = {"lat": 40.71, "lon": -74}

response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)
# Print the content of the response (the data the server returned)
print(response.content)
# This gets the same data as the command aboveresponse = requests.get("http://api.open-notify.org/iss-pass.json?lat=40.71&lon=-74")
print(response.content)
response.content.decode("utf-8")

import json
data = response.json()
print(type(data))
print(data)

# Headers is a dictionary
print(response.headers)
# Get the content-type from the dictionary.
print(response.headers["content-type"])


# Get the response from the API endpoint.
response = requests.get("http://api.open-notify.org/astros.json")
data = response.json()
# 9 people are currently in space.
print(data["number"])
print(data)