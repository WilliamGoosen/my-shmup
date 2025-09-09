# Game options/settings
TITLE = "My Shmup!"
BASE_WIDTH = 576
BASE_HEIGHT = 720
FPS = 60
FONT_NAME = 'arial'
HS_FILE = 'highscore.txt'
CONFIG_FILE = "config.ini"
MESSAGE_DISPLAY_TIME = 2000

BAR_LENGTH = 100
BAR_HEIGHT = 20


# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
PAUSE_OVERLAY = (0, 0, 0, 128)
CONFIRM_OVERLAY = (0, 0, 0, 192)

BG_COLOUR = BLACK

# player attributes
PLAYER_START_Y_OFFSET = 10
PLAYER_SPEED = 8
PLAYER_SHOOT_DELAY = 250
PLAYER_START_POWER = 1
PLAYER_MAX_SHIELD = 100
PLAYER_START_LIVES = 3
PLAYER_RESPAWN_TIME = 1000

# star attributes
STAR_MAX_SPEED = 2
STAR_MAX_RADIUS = 2
NUMBER_OF_STARS = 120

# Meteroid attributes
METEOROID_MIN_SPEED_X = -2
METEOROID_MAX_SPEED_X = 2
METEOROID_MIN_SPEED_Y = 1
METEOROID_MAX_SPEED_Y = 7
METEOROID_MIN_ROTATE_SPEED = -8
METEOROID_MAX_ROTATE_SPEED = 8
NUMBER_OF_METEOROIDS = 10

# Meteoroid image filename
ALL_METEOROID_FILES = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png',
    'meteorBrown_big3.png',
    'meteorBrown_big4.png',
    'meteorBrown_mid1.png',
    'meteorBrown_mid2.png',
    'meteorBrown_mid3.png',
    'meteorBrown_mid4.png',
    'meteorBrown_med1.png',
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png',
    'meteorBrown_tiny2.png'
    ]

MEDIUM_METEOROID_FILES = [
    'meteorBrown_mid1.png',
    'meteorBrown_mid2.png',
    'meteorBrown_mid3.png',
    'meteorBrown_mid4.png'
    ]
# Sound Files
SOUND_CONFIG = {
    "shoot": ("Laser_Shoot2.wav", 0.1),
    "shield": ("pow4.wav", 0.2),
    "power": ("pow5.wav", 0.2),
    "explosion": (["Explosion1.wav", "Explosion2.wav"], 0.1),
    "player_die": ("rumble1.ogg", 0.2)
}

MUSIC_CONFIG = {
    "gameplay": {"file":"tgfcoder-FrozenJam-SeamlessLoop.ogg", "volume": 0.2, "loops": -1}
}

# Explosion attributes
EXPLOSION_FRAME_RATE = 35

# UI attributes
PLAYER_LIVES_ICON_SPACING = 30

# Powerup attributes
POWERUP_TIME = 5000
POWERUP_SPEED = 4
POWERUP_DROP_CHANCE = 0.08