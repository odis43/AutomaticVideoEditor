#!/usr/bin/env python3
from webbrowser import get
from aubio import tempo, source
from numpy import median, diff
from moviepy.editor import * 
from natsort import natsorted
import glob

def get_file_bpm(path, params=None):
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512

    s = source(path, samplerate, hop_s)

    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    bpms = 60. / diff(beats)        
    return round(median(bpms))

audio_file = input("Please give the path of your audio file:\n")
bpm = get_file_bpm(audio_file, None)

duration = round(60/bpm, 3)

gif_name = 'pic'
fps = 24

file_list = glob.glob('*.JPEG')  # Get all the pngs in the current directory
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

                     