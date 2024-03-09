"""
spotify_downloader.py

This module provides functionality to download songs from a Spotify
playlist by searching for them on YouTube and saving them to the local computer.

Usage:
    python3 spotify_downloader.py [SPOTIFY_PLAYLIST_LINK] [DOWNLOAD_DIRECTORY]

Args:
    - SPOTIFY_PLAYLIST_LINK: The link to the Spotify playlist you want to download
    - DOWNLOAD_DIRECTORY: The directory where songs will be storaged
"""
import os
import re
import requests
import sys
from datetime import datetime, timedelta

import googleapiclient.discovery
from pytube import YouTube

import config


def is_spotify_playlist_link(link):
    """
    Check if Spotify playlist link is valid
    """
    spotify_pattern = r'^https://open\.spotify\.com/playlist/\w+$'
    return re.match(spotify_pattern, link) is not None


def search_youtube(song_name):
    """
    Search on YouTube for song_name and returns the first appearance
    """
    youtube = googleapiclient.discovery.build(
            'youtube', 'v3', developerKey=config.APIKEY_YT)
    request = youtube.search().list(
        part='snippet',
        q=song_name,
        type='video',
        maxResults=1
    )
    response = request.execute()
    return response['items'][0]


def format_song_name(song):
    """
    Append the song name with the artists involved
    """
    song_name = f'{song[0]} - '
    for artist in song[1]:
        song_name += f'{artist} '
    return song_name


def create_youtube_url(video_id):
    """
    Create YouTube video url given video ID
    """
    return 'https://www.youtube.com/watch?v=' + video_id


def get_spotify_credentials(client_id, client_secret):
    """
    Request a new Spotify token access
    """
    url = "https://accounts.spotify.com/api/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        response_dict = response.json()
        api_headers = {
            "Authorization": f"{response_dict['token_type']} {response_dict['access_token']}"
        }
        return api_headers
    else:
        print('Could not get Spotify token:', response.status_code)
        sys.exit()


class SpotifyAPI():
    """
    A class that facilitates interaction with the Spotify Web API.

    SpotifyAPI provides methods for making authenticated requests to the Spotify API,
    simplifying the process of accessing and managing data from Spotify's platform.
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.expiration = None
        self.credentials = None
        self.set_credentials()

    def is_token_expirated(self):
        """
        Check if token already has expired
        """
        return self.expiration is None or datetime.now() >= self.expiration
    
    def set_credentials(self):
        """
        Set a new token if necessary
        """
        if self.is_token_expirated():
            self.credentials = get_spotify_credentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
            self.expiration = datetime.now() + timedelta(seconds=3600)

    def get_playlist_info(self, playlist_id):
        """
        Get info about a playlist
        """
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        
        self.set_credentials()
        response = requests.get(url, headers=self.credentials)
        if response.status_code == 200:
            playlist_data = response.json()
            return playlist_data
        else:
            print(f"Failed to retrieve playlist information. Status code: {response.status_code}")
            sys.exit()

    def get_songs(self, playlist_info):
        """
        Get song names and artists
        """
        tracks = playlist_info['tracks']
        songs = tracks['items']
        tracks_info = [i['track'] for i in songs]
        return [(i['name'], [j['name'] for j in i['artists']]) for i in tracks_info]

    def playlist_id_extractor(self, url):
        """
        Extract playlist ID from url
        """
        return url.split('/')[-1]


def main(spotify_playlist_link, output_dir):
    if not is_spotify_playlist_link(spotify_playlist_link):
        print('Error: Invalid Spotify playlist link')
        sys.exit()

    import ipdb; ipdb.set_trace()
    spotify = SpotifyAPI(config.CLIENT_ID, config.CLIENT_SECRET)

    playlist_id = spotify.playlist_id_extractor(spotify_playlist_link)
    playlist_info = spotify.get_playlist_info(playlist_id)
    songs = spotify.get_songs(playlist_info)

    for song in songs:
        song_name = format_song_name(song)
        video_info = search_youtube(song_name)
        video_link = create_youtube_url(video_info['id']['videoId'])

        yt = YouTube(video_link)

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=output_dir)

        base, _ = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python program.py arg1 arg2")
    else:
        spotify_playlist_link = sys.argv[1]
        output_dir = sys.argv[2]
        main(spotify_playlist_link, output_dir)
