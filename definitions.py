# Constantes
SCREEN_WIDTH = 1080 / 2
SCREEN_HEIGHT = 1920 / 2

FPS = 120

MAX_FRAMES = 61 * FPS

GRAVITY = 0.03
MAX_SPEED = 15

BALL_SPEED = 0
ARC_SPEED_ROTATE = 0.01

BALL_RADIUS = 30

ENERGY_LOST_COEFF = 1

N_ARCS = 5 # 28 pour la V. finale
N_BALLS = 2

BONUS_ARC_SIZE = 30
BONUS_COLOR = 10
BONUS_BALL_RADIUS = 0.00008

V_RAPPROCHEMENT = 1

# Fonctions
def angle_in_interval(angle, start, end):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end

import os, shutil
def delete_frames_audio():
    if os.path.isdir("frames"):
        shutil.rmtree("frames")
    if os.path.isdir("audios"):
        shutil.rmtree("audios")