import os, shutil

def angle_in_interval(angle, start, end):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end
    
def delete_frames_audio():
    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    if os.path.isdir("audios"):
        shutil.rmtree("audios")