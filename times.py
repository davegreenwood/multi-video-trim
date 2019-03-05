""" Get the start offsets and duration of videos with a sound track. """
import warnings
import logging
import ffmpeg
import numpy as np
from scipy.signal import fftconvolve


warnings.filterwarnings("ignore", category=FutureWarning)
LOG = logging.getLogger(__name__)


def buffer_audio(fname, max_time="00:01:00.000", fmt='f32le'):
    """Buffer the audio, up to max_time."""
    out, err = (ffmpeg.input(fname, t=max_time)
                .output('pipe:', format=fmt)
                .run(capture_stdout=True, capture_stderr=True))
    _ = err
    return np.frombuffer(out, dtype=np.float32)


def get_lag(y1, y2, audiofs=None):
    """
    Using convolution - get the offset between y1 and y2.
    If audiofs is supplied the offset is in seconds, otherwise in samples.
    returns t secs (if audiofs supplied) that, if added to start of y2,
    will align y2 with y1.
    """
    LOG.info("Calculating lag.")
    z = fftconvolve(y1, y2[::-1])
    lags = np.arange(z.size) - (y2.size - 1)
    t = lags[np.argmax(np.abs(z))]
    if audiofs:
        return t / audiofs
    return t


def get_duration(video_list, times):
    """Using ffmpeg probe, return the movie duration in seconds. """
    def _dur(v):
        return float(ffmpeg.probe(v)["format"]["duration"])
    durs = np.array([_dur(v) for v in video_list])
    return round(min(durs-times) - 1)


def starts(video_list, max_time="00:02:00.000", fmt="f32le"):
    """Get all the time offsets for the list of videos.
    Uses cross correlation, so could take a while for large max_times.
    Simply assume that the audio fs is 48000. Hz"""
    times = [0]
    w0 = buffer_audio(video_list[0], max_time, fmt)
    for v in video_list[1:]:
        LOG.info("buffering %s", v)
        w1 = buffer_audio(v, max_time, fmt)
        t = get_lag(w0, w1, 48000.)
        times.append(t)
    times = np.array(times)
    times = (times - times.max()) * -1
    return times


def yield_vf_ss_t(video_list, max_time="00:02:00.000", fmt="f32le"):
    """Convenience function to yield data to sync and crop a list of videos """
    vlist = sorted(video_list)
    times = starts(vlist, max_time=max_time, fmt=fmt)
    d = get_duration(vlist, times)
    LOG.info("Sync finished.")
    for v, t in zip(vlist, times):
        LOG.info("File: %s, Seek time: %s", v, t)
        yield v, t, d
