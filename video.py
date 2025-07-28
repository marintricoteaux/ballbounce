import os
import subprocess
import shutil
from datetime import datetime

def create_video_from_frames(frame_folder = "frames",
                             framerate = 60,
                             video_folder = "videos"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(video_folder, f"video_{timestamp}.mp4")

    cmd = [
        "ffmpeg",
        "-y",  # overwrite output file if exists
        "-framerate", str(framerate),
        "-i", f"{frame_folder}/frame_%04d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_file
    ]
    subprocess.run(cmd)

def delete_frames():
    shutil.rmtree("frames")