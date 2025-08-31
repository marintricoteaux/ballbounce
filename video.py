from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from datetime import datetime
from pydub import AudioSegment

from definitions import *
from functions import *

def create_music_from_sounds(hit_times, out_circle_times_yes, out_circle_times_no, duration_ms = 61 * 1000):
    os.makedirs("audios", exist_ok=True)

    out_circle_sound_yes = AudioSegment.from_file("sounds/yes.mp3")
    out_circle_sound_no = AudioSegment.from_file("sounds/no.mp3")
    hit_sound_video = AudioSegment.from_file("sounds/pop.mp3")
    out_all_circles_sound_video = AudioSegment.from_file("sounds/victory_ring.mp3")
    track = AudioSegment.silent(duration_ms)
    for t in out_circle_times_yes:
        if 0 <= t <= duration_ms:
            track = track.overlay(out_circle_sound_yes, t)
    for t in out_circle_times_no:
        if 0 <= t <= duration_ms:
            track = track.overlay(out_circle_sound_no, t)
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

    clip = ImageSequenceClip(frame_files, fps=FPS)

    audio = AudioFileClip("audios/audio.mp3")

    duration = min(clip.duration, audio.duration)
    clip = clip.subclipped(0, duration)
    audio = audio.subclipped(0, duration)

    clip = clip.with_audio(audio)

    clip.write_videofile(output_path,
                         codec="libx264",
                         audio_codec="aac",
                         fps=FPS,
                         ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"])