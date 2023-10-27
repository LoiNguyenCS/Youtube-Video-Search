from pytube import Playlist
from pytube import YouTube

import os

# Define the URL of the YouTube playlist
playlist_url = 'https://www.youtube.com/watch?v=kRHhZ8l9RMQ&list=PLp-wXwmbv3z9Xj172jZPPPoYeTS0eanty&pp=iAQB'

# Create a Pytube Playlist object
playlist = Playlist(playlist_url)

# Set the directory where you want to save the caption files
output_directory = 'captions/'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

count = 0
# Iterate through the videos in the playlist and download captions
for video in playlist.video_urls:
    if count > 50:
      break;
    yt = YouTube(video)
    try:
      yt.bypass_age_gate()
      print('Captions Available: ', yt.captions)
      print()

      en_caption = yt.captions.get("a.en")
      video_title = yt.title
      caption_filename = os.path.join(output_directory, f"{video_title}.xml")
      with open(caption_filename, 'w', encoding='utf-8') as caption_file:
          caption_file.write(en_caption.xml_captions)
      count = count + 1

    except:
      print("You're too young")

print("Caption download completed.")
