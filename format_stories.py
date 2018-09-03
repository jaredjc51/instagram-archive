# -*- coding: utf-8 -*-
"""
Python script for reading downloaded instagram story data.
Parses 'media.json' to determine upload date and time.
Converts images to video, adds upload date and time to
vidoes and pictures, and saves a copy of the video.

v. 1.0 Last modified 2018-09-03
"""
from __future__ import print_function
import sys
import os
import json
import pandas as pd
import ffmpeg

# Get current directory
my_path = sys.path[0]
# Make 'output' folder directory
out_directory = os.path.join(my_path, 'output')
# If the directory doesn't currently exist, then make it
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

def add_text(stream, text):
    '''
    Put text on the video stream
    '''
    return ffmpeg.drawtext(stream, text=text, x=50, y=50,
                             fontfile=r'C:/Windows/Fonts/arial.ttf',
                             fontsize=36, fontcolor='white', borderw=4)

# Read json file
with open('media.json') as json_data:
    data = json.load(json_data)

# Convert json info of stories to dataframe
s = pd.DataFrame(data['stories'])
s['taken_at'] = pd.to_datetime(s['taken_at'])
# Save to .csv for reference
s.to_csv('stories.csv', index=False, encoding='utf-8')

# For every story file
for i in range(s.shape[0]):
    # Print current file number
    print("Processing {} of {}".format(i+1, s.shape[0]))
    # Get filepath of current file
    infile = s['path'][i]
    # Get date and time of current file
    ts = s['taken_at'][i]
    # Format filename of output
    outfile = ts.strftime('%Y-%m-%d_%H-%M-%S')
    # Format date string to overlay on video
    date = ts.strftime('%b. %d, %Y')
    # When the file is a picture
    if 'jpg' in infile:
        # Loop the input picture to make a video
        stream = ffmpeg.input(infile, loop=1, r=30)
        a = ffmpeg.input('anullsrc=cl=mono', f='lavfi')
        # Resize to dimensions of video
        stream = ffmpeg.filter(stream, 'scale', size='640:1136')
        # Overlay date on video file
        stream = add_text(stream, date)
        # Prepare for output
        out = ffmpeg.output(stream, a, 'output/{}.mp4'.format(outfile),
                            **{'t': 5, 'c:v': 'libx264', 'pix_fmt': 'yuv420p'})
    # When the file is a video
    elif 'mp4' in infile:
        no_audio = False
        # Get the input video file
        stream = ffmpeg.input(infile)
        # Get the metadata of the input file
        info = ffmpeg.probe(infile)
        # Overlay date on the video
        stream = add_text(stream, date)
        # Does the video have an audio track
        try:
            info['streams'][1]
        except IndexError:
            no_audio = True
        
        if no_audio is True:
            # Add a silent audio track if no audio track exists
            a = ffmpeg.input('anullsrc=cl=mono', f='lavfi', t=info['streams'][0]['duration'])
            out = ffmpeg.output(stream, a,  'output/{}.mp4'.format(outfile), map='1:a')
        elif no_audio is False:
            out = ffmpeg.output(stream, 'output/{}.mp4'.format(outfile), map='0:a')

    # Save the current video
    ffmpeg.run(out, quiet=True, overwrite_output=True)
