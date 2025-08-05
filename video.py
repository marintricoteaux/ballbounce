import os

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from datetime import datetime

from pydub import AudioSegment

import shutil

def create_music_from_sounds(hit_times, out_circle_times, duration_ms = 61 * 1000):
    os.makedirs("audios", exist_ok=True)

    out_circle_sound_video = AudioSegment.from_file("sounds/pet.wav")
    hit_sound_video = AudioSegment.from_file("sounds/pop.mp3")
    track = AudioSegment.silent(duration_ms)
    for t in out_circle_times:
        if 0 <= t <= duration_ms:
            track = track.overlay(out_circle_sound_video, t)
    for t in hit_times:
        if 0 <= t <= duration_ms:
            track = track.overlay(hit_sound_video, t)
    track.export("audios/audio.mp3", "mp3")
    
def create_video():
    os.makedirs("videos", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    output_path = os.path.join("videos", f"video_{timestamp}.mp4")

    frames_folder = "frames"

    frame_files = sorted([
        os.path.join(frames_folder, f)
        for f in os.listdir(frames_folder)
        if f.endswith(".png") or f.endswith(".jpg")
    ])

    clip = ImageSequenceClip(frame_files, fps=60)

    audio = AudioFileClip("audios/audio.mp3")
    audio = audio.subclipped(0, clip.duration)

    clip = clip.with_audio(audio)

    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

def delete_frames_audio():
    shutil.rmtree("frames")
    shutil.rmtree("audios")