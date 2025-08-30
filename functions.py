import os, shutil
    
def delete_frames_audio():
    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    if os.path.isdir("audios"):
        shutil.rmtree("audios")