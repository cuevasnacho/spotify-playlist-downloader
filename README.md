# Spotify Downloader

This Python project is designed to make it easy to download songs from a Spotify playlist. By utilizing the Spotify API to retrieve the list of songs, it then searches for them on YouTube and downloads the corresponding MP3 files to a specified directory.

## Installation

Ensure you have Python 3 installed on your system.

```bash
# Check Python version
python3 --version

# Download if needed
sudo apt update
sudo apt install python3
```

Clone this repository to your local machine:

```bash
git clone https://github.com/cuevasnacho/spotify-playlist-downloader.git
```

Navigate into the project directory:

```bash
cd spotify-playlist-downloader
```

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

To use the Spotify Downloader, run the following command in your terminal:

```bash
python3 spotify_downloader.py [SPOTIFY_PLAYLIST_LINK] [DOWNLOAD_DIRECTORY]
```

Replace `[SPOTIFY_PLAYLIST_LINK]` with the link to the Spotify playlist you want to download from, and `[DOWNLOAD_DIRECTORY]` with the directory where you want to save the downloaded MP3 files.

To get `SPOTIFY_PLAYLIST_LINK`:
1. Navigate to the playlist you want to download
2. Press share and copy link to playlist

For example:

```bash
python3 spotify_downloader.py https://open.spotify.com/playlist/your_playlist_id /path/to/download/directory
```

## Authentication

To utilize the Spotify API, you need to obtain client credentials by creating an application on the [Spotify Developer Documentation](https://developer.spotify.com/documentation/web-api). Once you have obtained your client ID and client secret, you can set them in your spotify-playlist-downloader/config.py file:

```bash
cd spotify-playlist-downloader
echo "SPOTIFY_CLIENT_ID='your_client_id'" > config.py
echo "SPOTIFY_CLIENT_SECRET='your_client_secret'" >> config.py
```

You also need a YouTube API key to search for songs on YouTube. To get it follow the steps detailed on the [next guide](https://developers.google.com/youtube/registering_an_application). Once you have obtained your YouTube API key, add it as a constant in the `config.py` file:

```bash
echo "YOUTUBE_API_KEY='your_youtube_api_key'" >> config.py
```

## Disclaimer

Please note that downloading copyrighted material may infringe upon the rights of the content owner. Make sure to use this tool responsibly and only download content that you have the legal right to access.
