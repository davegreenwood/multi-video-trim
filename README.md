# Trim multiple video files

Trim multiple video files using a common Timecode start time, to a common end time.

Developed for a particular purpose, but fundmentaly should be useful for trimming
and aligning multiple videos that have been shot gen-locked with sync sound.

## Install

From the directory containing `setup.py`:

    pip install -e .

## Usage

Help is available with `trim --help`, and a complete example is:

    trim  --max-time  "00:03:00.000" \
        "/Volumes/data3/AJ-R/scene-01/" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/001_0002.mov" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/002_0002.mov" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/003_0002.mov" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/004_0002.mov" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/005_0002.mov" \
        "/Volumes/data1/aj_emo/emo_video/scene-01/006_0002.mov"

