"""Trim multiple video on timecode """
import os
import logging
from subprocess import run
import click
from times import yield_vf_ss_t


def _get_outfile(vfname, save_path):
    """Helper to form the save name."""
    fname = os.path.join(save_path, os.path.split(vfname)[-1])
    return fname.replace(".mov", ".mp4")


def sync_list(video_list, save_path, max_time, fs=59.94, fmt="f32le"):
    """Run ffmpeg to sync the videos in the list."""
    for v, ss, t in yield_vf_ss_t(video_list, max_time=max_time, fmt=fmt):
        out = _get_outfile(v, save_path)
        args = ["ffmpeg",
                "-r", str(fs),
                "-i", v,
                "-ss", str(ss),
                "-t", str(t),
                "-vf", "transpose=1",
                "-c:v", "libx264", "-crf", "18",
                "-pix_fmt", "yuv420p",
                out]
        run(args)


@click.argument("vfnames", nargs=-1, type=click.Path(exists=1, dir_okay=0))
@click.argument("save_path", type=click.Path(exists=1, file_okay=0))
@click.option("--max-time", "-n", type=click.STRING, default="00:03:00.000",
              help="Specify the max time to buffer audio: " +
              "hrs:mins:secs.milliseconds - " +
              "Must be enough to encompass the difference in start " +
              "time of all videos in list.")
@click.option("--fps", "-r", help="video frame rate", default=59.94)
@click.option("--audio-format", "-a", help="audio format", default="f32le")
@click.command()
def main(**kwargs):
    """CLI function."""
    fstr = "%(asctime)s : %(name)s : %(levelname)s : %(message)s"
    logging.basicConfig(level=logging.DEBUG, format=fstr)
    video_list = kwargs.get("vfnames")
    save_path = kwargs.get("save_path")
    max_time = kwargs.get("max_time")
    fmt = kwargs.get("audio_format")
    fs = kwargs.get("fps")
    sync_list(video_list, save_path, max_time, fs, fmt)


if __name__ == "__main__":
    main()
