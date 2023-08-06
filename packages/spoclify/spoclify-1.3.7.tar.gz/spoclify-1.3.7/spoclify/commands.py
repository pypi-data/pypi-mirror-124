from spotipy import Spotify

from . import get_current_device, get_instance, formatting

sp: Spotify = get_instance()

assert sp is not None, "Couldn't get the Spotipy instance"

def play(artist_name, song_name):

    result = sp.search(q=f"artist:{artist_name} track:{song_name}", type='track', limit=1)

    assert len(songs := result['tracks']['items']) > 0, "No song matches the search terms!"

    uri = songs[0]['uri']

    formatting.info(f"Playing {song_name} by {artist_name}")

    sp.start_playback(uris=[uri], device_id=get_current_device())

def volume(new_vol):
    assert 0 <= new_vol <= 100, "Volume outside bounds"

    formatting.info(f"New volume: {new_vol}")

    sp.volume(volume_percent=new_vol, device_id=get_current_device())

def pause():
    
    formatting.info("Pausing playback")

    sp.pause_playback(device_id=get_current_device())

def resume():
    
    formatting.info("Resuming playback")

    sp.start_playback(device_id=get_current_device())

def skip():

    formatting.info("Skipping current track")

    sp.next_track(device_id=get_current_device())

def prev():

    formatting.info("Playing previous track")

    sp.previous_track(device_id=get_current_device())

def shuffle():

    shuffle_state = sp.current_playback()["shuffle_state"]

    formatting.info(f"Toggling shuffle {'on' if not shuffle_state else 'off'}")

    sp.shuffle(not shuffle_state, device_id=get_current_device())

def repeat(repeat_state):

    formatting.info(f"Setting repeat-state to {repeat_state}")

    sp.repeat(repeat, device_id=get_current_device())

def queue(artist_name, song_name):

    result = sp.search(q=f"artist:{artist_name} track:{song_name}", type='track', limit=1)

    assert len(songs := result['tracks']['items']) > 0, "No song matches the search terms!"
    
    uri = songs[0]['uri']

    track = sp.track(uri)

    artists_l = [artist['name'] for artist in track['artists']]

    artists = artists_l[0] if len(artists_l) == 1 else (' and '.join(artists_l) if len(artists_l) == 2 else (', '.join(artists_l[:-1]) + f" and {artists_l[-1]}"))

    formatting.info(f"Queueing {track['name']} by {artists}")

    sp.add_to_queue(uri=uri, device_id=get_current_device())

def fill_queue(count):

    recomendations = sp.recommendations(seed_tracks=[sp.currently_playing()['item']['uri']], limit=count)

    recomendations = list(map(lambda track: track['uri'], recomendations['tracks']))

    formatting.info("Filling queue")

    for uri in recomendations:
        track = sp.track(uri)

        artists_l = [artist['name'] for artist in track['artists']]

        artists = artists_l[0] if len(artists_l) == 1 else (' and '.join(artists_l) if len(artists_l) == 2 else (', '.join(artists_l[:-1]) + f" and {artists_l[-1]}"))

        formatting.attention(f"Queueing {track['name']} by {artists}")

        sp.add_to_queue(uri=uri, device_id=get_current_device())

    formatting.info("Finished filling queue")

def current():

    current = sp.currently_playing()

    assert current is not None, "Spotify must be playing something"

    current_song = current['item']['name']

    current_artist = ", ".join([artist['name'] for artist in current['item']['artists']])

    current_progress = str(round(current['progress_ms'] / current['item']['duration_ms'] * 100, 2)) + "%"

    devices = sp.devices()['devices']

    for device in devices:
        if device['is_active']:
            current_device = device['name']
            device_type = device['type']
            volume = device['volume_percent']

    formatting.info(f"""Current device: {device_type} - {current_device}
{current_artist} - {current_song}
Progress: {current_progress}
Current volume: {volume}%""")

def seek(new_ms):

    current = sp.currently_playing()

    assert current is not None, "Spotify must be playing something"

    current_song = current['item']

    assert 0 <= new_ms <= current_song['duration_ms'], "Can't seek to time outside song duration"

    formatting.info(f"Seeking to {new_ms}ms")

    sp.seek_track(new_ms, device_id=get_current_device())

def devices():

    devices = sp.devices()['devices']

    formatting.fprint("User devices:")

    for device in devices:
        name, is_active, type, volume = device['name'], device['is_active'], device['type'], device['volume_percent']

        text = f"""    {name}: 
        Type: {type}
        Volume: {volume}     
"""

        if (is_active): formatting.attention(text)
        else: formatting.fprint(text)

def like_current():

    current = sp.currently_playing()

    current_song_id = current.get("item", {'id': None})['id']

    sp.current_user_saved_tracks_add([current_song_id])

    formatting.info("Saving current song to liked songs")

def toggle_like():
    current = sp.currently_playing()

    current_song_id = current.get("item", {'id': None})['id']

    if sp.current_user_saved_tracks_contains([current_song_id])[0]:
        sp.current_user_saved_tracks_delete([current_song_id])
        return "♡"
    else:
        sp.current_user_saved_tracks_add([current_song_id])
        return "♥"