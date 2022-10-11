#!/usr/bin/env python3
from aubio import tempo, source
from numpy import median, diff
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from natsort import natsorted
import glob
import sys

def get_file_bpm(path, params=None):
    if params is None:
        params = {}
    samplerate, win_s, hop_s = 44100, 1024, 512

    s = source(path, samplerate, hop_s)

    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    beats = []
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break

    bpms = 60. / diff(beats)        
    return round(median(bpms))

print("\n")
print("##############################################################\n")
print("Welcome to AutoEditor!\n")
print("Make sure your JPEGS are in the current directory!\n")
print("Also make sure your audio is a .wav file\n")
print("Enter q if you would like to quit or any other key to progress\n")
print("##############################################################\n")

x = input()
if x == "q":
    sys.exit()

audio_file = input("Please give the path of your audio file:\n")
bpm = get_file_bpm(audio_file, None)

duration = round(60/bpm, 3)

gif_name = 'pic'
fps = 24

file_list = glob.glob('*.JPEG')  # Get all the pngs in the current directory
print(file_list)
file_list_sorted = natsorted(file_list,reverse=False)  # Sort the images

time = int(input("How fast would you like your clips?\n" + "i.e 1 => normal speed, 2 => double speed, etc.\n"))

duration = duration/time

print(duration)
print("Compiling your video now...")

clips = [ImageClip(m).set_duration(duration)
         for m in file_list_sorted]

concat_clip = concatenate_videoclips(clips, method="compose")
audio = AudioFileClip(audio_file)
concat_clip.audio = audio
concat_clip.write_videofile("video.mp4", temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac",fps=fps)

                     
