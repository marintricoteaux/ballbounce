SCREEN_WIDTH = 1080 / 2
SCREEN_HEIGHT = 1920 / 2

FPS = 120

MAX_FRAMES = 61 * FPS

GRAVITY = 0.1
MAX_SPEED = 10

BALL_SPEED = 0
ARC_SPEED_ROTATE = 0.01

ENERGY_LOST_COEFF = 0.99

N_ARCS = 15

BONUS_ARC_SIZE = 30
MALUS_ARC_SPEED = 0.06
BONUS_COLOR = -10
BONUS_BALL_RADIUS = 0.00008

def angle_in_interval(angle, start, end):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end