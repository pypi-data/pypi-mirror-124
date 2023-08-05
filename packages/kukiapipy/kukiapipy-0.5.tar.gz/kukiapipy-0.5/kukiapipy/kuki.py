from requests.exceptions import HTTPError
import requests

url = "https://kukiapi.xyz/api"


def chatbot(key, name, owner, msg):
    base = f'{url}/apikey={key}/{name}/{owner}/message={msg}'
    response = requests.get(base)
    response.raise_for_status()
    jsonResponse = response.json()
    reply = (jsonResponse["reply"])
    return reply


