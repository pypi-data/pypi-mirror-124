import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from requests.exceptions import ConnectionError

from . import scopes as sc, utils
from .formatting import fprint, warning, fatal

try:
    scopes = sc.get_scope(sc.SCOPES)
except AssertionError:
    fatal("Invalid scopes given")
    exit(1)

os.makedirs(f"{os.environ['HOME']}/.spoclify", exist_ok=True)

try:
    spo = SpotifyOAuth(scope=scopes, redirect_uri="http://localhost", cache_path=f"{os.environ['HOME']}/.spoclify/.cache")
    sp = spotipy.Spotify(client_credentials_manager=spo)
except ConnectionError as error:
    fatal(f"No connection could be established: {str(error)}")
    exit(1)

utils.add_var("instance", sp)

def get_instance() -> spotipy.Spotify: return utils.get("instance", None)

def get_current_device(default_current = False):
    devices = sp.devices()

    if 'devices' in devices:
        for device in devices['devices']:
            if device['is_active']:
                id = device['id']
                if utils.get("current", "this will always be different") != id:
                    utils.add_var("current", id)
                return None if default_current else id
    warning("No devices currently active")
    return None

def refresh_access_token():
    cached_token = spo.get_cached_token()
    refreshed_token = cached_token['refresh_token']
    new_token = spo.refresh_access_token(refreshed_token)
    utils.add_var("instance", spotipy.Spotify(auth=new_token['access_token']))
    # also we need to specifically pass `auth=new_token['access_token']`
    # sp = spotipy.Spotify(auth=new_token['access_token'])
    return new_token