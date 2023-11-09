from pytube import YouTube

url = 'https://www.youtube.com/watch?v=ENjhn4joTIc'
video = YouTube(url)
download_path = 'D:\NJIT Courses\CS482 Data Mining\Data-Mining-Milestone-1'
video = video.streams.get_highest_resolution()
video.download(output_path=download_path)
print('Done!')
