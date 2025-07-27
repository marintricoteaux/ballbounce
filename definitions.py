SCREEN_WIDTH = 1080 / 2
SCREEN_HEIGHT = 1920 / 2

GRAVITY = 0.1
MAX_SPEED = 15

BALL_SPEED = 3
ARC_SPEED_ROTATE = 0.01

ENERGY_LOST_COEFF = 1

def angle_in_interval(angle, start, end):
    if start <= end:
        return start <= angle <= end
    else:
        return angle >= start or angle <= end