import requests
import json

data_api = "7db6089286msh762b26fa6a12042p1a045bjsnb6f0b33d88e2"


def get_world_population(api):
    data_url = "https://world-population.p.rapidapi.com/worldpopulation"
    headers = {
        'x-rapidapi-host': "world-population.p.rapidapi.com",
        'x-rapidapi-key': api
    }
    response = requests.request("GET", data_url, headers=headers)
    raw_data = json.loads(response.text)
    data = raw_data['body']['world_population']
    return data


def get_country_population(api, country):
    data_url = "https://world-population.p.rapidapi.com/population"
    query = country.capitalize()
    querystring = {"country_name": query}
    headers = {
        'x-rapidapi-host': "world-population.p.rapidapi.com",
        'x-rapidapi-key': api
    }
    response = requests.request(
        "GET", data_url, headers=headers, params=querystring)
    raw_data = json.loads(response.text)
    data = raw_data['body']
    return data
