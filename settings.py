# Game options/settings
TITLE = "My Shmup!"
BASE_WIDTH = 576
BASE_HEIGHT = 720
FPS = 60
MENU_FPS = 60
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
PLAYER_SPEED = 480
PLAYER_SHOOT_DELAY = 250 # Seconds
PLAYER_START_POWER = 1
PLAYER_MAX_SHIELD = 100
PLAYER_START_LIVES = 3
PLAYER_RESPAWN_TIME = 1000

# star attributes
STAR_MIN_SPEED = 6
STAR_MAX_SPEED = 120
STAR_MAX_RADIUS = 2
NUMBER_OF_STARS = 120

# Meteroid attributes
METEOROID_MIN_SPEED_X = -120
METEOROID_MAX_SPEED_X = 120
METEOROID_SPLIT_SPEED_BOOST = 120
METEOROID_MIN_SPEED_Y = 60
METEOROID_MAX_SPEED_Y = 420
METEOROID_MIN_ROTATE_SPEED = -160
METEOROID_MAX_ROTATE_SPEED = 160
METEOROID_SPAWN_Y_MIN = 10
METEOROID_SPAWN_Y_MAX = 150
NUMBER_OF_METEOROIDS = 15

# Bullet attributes
BULLET_SPEED = -600

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

# Icon Files
ICON_LIST = [
        "enter_icon.png",
        "spacebar_icon.png",
        "spacebar_icon_2.png",
        "esc_icon.png",
        "minus_icon.png",
        "plus_icon.png",
        "m_icon.png",
        "q_icon.png",
        "r_icon.png",
        "s_icon.png",
        "y_icon.png",
        "n_icon.png",
        "up_icon.png",
        "down_icon.png",
        "left_icon.png",
        "right_icon.png"
    ]

ARROW_LIST = [
        "up_icon.png",
        "right_icon.png",
        "down_icon.png",
        "left_icon.png"
    ]

POWERUP_LIST = [
    "health_up.png",
    "bolt_gold.png"
]


# Sound Files
SOUND_CONFIG = {
    "shoot": ("Laser_Shoot2.wav", 0.1),
    "health_up": ("pow4.wav", 0.2),
    "bolt_gold": ("pow5.wav", 0.2),
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
POWERUP_SPEED = 240
POWERUP_DROP_CHANCE = 0.08