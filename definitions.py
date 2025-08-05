SCREEN_WIDTH = 1080 / 2
SCREEN_HEIGHT = 1920 / 2

MAX_FRAMES = 61 * 60

GRAVITY = 0.15
MAX_SPEED = 100

BALL_SPEED = 3
ARC_SPEED_ROTATE = 0.008

ENERGY_LOST_COEFF = 0.99

N_ARCS = 10

BONUS_ARC_SIZE = 30
MALUS_ARC_SPEED = 0.06

def angle_in_interval(angle, start, end):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end