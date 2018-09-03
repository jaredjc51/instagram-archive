# Instagram Archive
The scripts in this repository can be used to create one long video from your downloaded instagram stories.
You need a few things installed on your computer to make this happen:
  - Python
  - ffmpeg

First, run `format_stories.py` to parse the `media.json` file to determine the upload date of the Instagram stories, convert pictures to 5 second videos if applicable, add the upload date to the video, and save a copy of the video.
Second, run `join.bat` to combine the videos into one long video.
Make sure the first video has an audio track or else no videos will have sound.
