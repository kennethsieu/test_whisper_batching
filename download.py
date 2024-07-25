from pytube import YouTube 
import os 

link = "https://www.youtube.com/watch?v=aFBCIpF9kHc"

yt = YouTube(link, use_oauth=True,allow_oauth_cache=True)
video = yt.streams.filter(only_audio=True).first() 

out_file = video.download() 
base, ext = os.path.splitext(out_file) 
new_file = 'test.mp3'
os.rename(out_file, new_file) 