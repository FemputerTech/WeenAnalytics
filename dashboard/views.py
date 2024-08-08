from flask import Blueprint, jsonify
import requests
import base64
import os


views = Blueprint("views", __name__)


SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=headers, data=data)
    response_data = response.json()
    return response_data['access_token']


def search_band(access_token, band_name='Ween'):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'q': band_name,
        'type': 'artist',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()


@views.route("/", methods=["GET"])
def index():
    token = get_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    data = search_band(token)
    return jsonify(data)