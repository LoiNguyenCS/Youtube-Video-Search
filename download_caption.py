from pytube import Playlist
from pytube import YouTube

import os


playlist_url = 'https://www.youtube.com/watch?v=kRHhZ8l9RMQ&list=PLp-wXwmbv3z9Xj172jZPPPoYeTS0eanty&pp=iAQB'
playlist = Playlist(playlist_url)


output_directory = 'captions/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

count = 0
for video in playlist.video_urls:
    if count > 50:
      break;
    yt = YouTube(video)
    try:
      yt.bypass_age_gate()
      en_caption = yt.captions.get("a.en")
      video_title = yt.title
      caption_filename = os.path.join(output_directory, f"{video_title}.xml")
      with open(caption_filename, 'w', encoding='utf-8') as caption_file:
          caption_file.write(en_caption.xml_captions)
      count = count + 1

    except:
      # The current video has an age restriction. The program will skip it
      print("Skip one video due to age restriction!")

print("Caption download completed.")
