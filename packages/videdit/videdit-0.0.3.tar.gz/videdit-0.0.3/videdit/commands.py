import os
import subprocess
import uuid

from typing import List

from videdit.checks import requires_ffmpeg


WORKDIR = "/tmp"


@requires_ffmpeg
def cut_video(*, file: str, output: str, intervals: List[str]):
    ffmpeg_logs = open("ffmpeg_logs.txt", "a")

    # no need to perform split/merge if only one segment
    if len(intervals) == 1:
        print(f"[INFO] Directly creating output into {output}")
        subprocess.call(["ffmpeg", "-y", "-i", file, "-vcodec", "copy", "-acodec", "copy", "-avoid_negative_ts", "make_zero", "-ss", intervals[0][0], "-to", intervals[0][1], "-sn", output])
        return

    partials = []
    extension = file.split(".")[-1]

    # create a temporary video file for each segment
    for interval in intervals:
        print(f"[INFO] Cutting interval {' - '.join(interval)}")
        filename = f"{WORKDIR}/{uuid.uuid4()}.{extension}"
        subprocess.call(["ffmpeg", "-y", "-i", file, "-vcodec", "copy", "-acodec", "copy", "-ss", interval[0], "-to", interval[1], "-sn", filename], stdout=ffmpeg_logs, stderr=ffmpeg_logs)
        partials.append(filename)

    # concatenate each temporary file in output
    with open(f"{WORKDIR}/mkv_index.txt", "w") as mkvindex:
        print(f"[INFO] Merging all intervals into {output}")
        for partial in partials:
            mkvindex.write(f"file '{partial}'\n")

    subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORKDIR}/mkv_index.txt", "-c", "copy", output], stdout=ffmpeg_logs, stderr=ffmpeg_logs)

    # remove temporary video files
    for partial in partials:
        os.remove(partial)

    ffmpeg_logs.close()
