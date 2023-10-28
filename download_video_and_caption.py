import os
from pytube import Playlist
from pytube import YouTube

url = 'https://www.youtube.com/watch?v=ENjhn4joTIc&list=PLp-wXwmbv3z9Xj172jZPPPoYeTS0eanty&pp=iAQB'
parent_path =  'D:/NJIT Courses\CS482 Data Mining\Data-Mining-Milestone-1'
os.makedirs(parent_path, exist_ok=True)

p = Playlist(url)
for video_url in p.video_urls[:51]:
	yt = YouTube(video_url)
	if yt.age_restricted:
		print(f"Skipping age-restricted video: {video.title}")
		continue
	# Create a folder
	# -- ensure Windows filename format style
	video_title = yt.title[:-14].strip()
	video_title = yt.title.replace("|", "").replace(":", "").replace("?", "").strip()
	download_path = os.path.join(parent_path, video_title)
	os.makedirs(download_path, exist_ok=True)
	# Download video
	print(f'Downloading: {yt.title}')
	video = yt.streams.get_highest_resolution()
	video.download(output_path=download_path)
	print('Done! Video downloaded to {download_path}')
	# Download caption and store in the same folder
	en_caption = yt.captions.get("a.en")
	caption_filename = os.path.join(download_path, f'{video_title}.xml')
	with open(caption_filename, 'w', encoding='utf-8') as caption_file:
		caption_file.write(en_caption.xml_captions)
	print('Done! Caption downloaded to {download_path}')
print(f"All videos downloaded to {download_path}")
