import requests
import os


def giphy_api(limit=200):

    GIPHY_KEY = os.getenv('GIPHY_API_KEY')

    url = f'http://api.giphy.com/v1/gifs/trending?api_key={GIPHY_KEY}&limit={limit}'
    response = requests.get(url).json()

    GIPHY_STORE = {}
    for gif in response["data"]:
        GIPHY_STORE[gif['id']] = gif['embed_url']

    return GIPHY_STORE
