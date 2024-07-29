import pygame

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

CHECKBOARD_WIDTH = 525
CHECKBOARD_HEIGHT = 590

Start_X = 27
Start_Y = 35
Line_Span = 64

player1Color = 1
player2Color = 2
overColor = 3

BG_COLOR = pygame.Color(255, 255, 255)
TEXT_COLOR = pygame.Color(255, 0, 0)

# Color Space might be used
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


repeat = 0

pieces_images = {
    'b_chariot': pygame.image.load("imgs/b_chariot.gif"),
    'b_elephant': pygame.image.load("imgs/b_elephant.gif"),
    'b_king': pygame.image.load("imgs/b_king.gif"),
    'b_horse': pygame.image.load("imgs/b_horse.gif"),
    'b_advisor': pygame.image.load("imgs/b_advisor.gif"),
    'b_cannon': pygame.image.load("imgs/b_cannon.gif"),
    'b_pawn': pygame.image.load("imgs/b_pawn.gif"),

    'r_chariot': pygame.image.load("imgs/r_chariot.gif"),
    'r_elephant': pygame.image.load("imgs/r_elephant.gif"),
    'r_king': pygame.image.load("imgs/r_king.gif"),
    'r_horse': pygame.image.load("imgs/r_horse.gif"),
    'r_advisor': pygame.image.load("imgs/r_advisor.gif"),
    'r_cannon': pygame.image.load("imgs/r_cannon.gif"),
    'r_pawn': pygame.image.load("imgs/r_pawn.gif"),
}

bg = r'imgs/bg.png'


my_max = True
my_min = False

# all kinds of pieces
empty = 0
king = 1
chariot = 2
horse = 3
cannon = 4
elephant = 5
advisor = 6
pawn = 7
# initial chess board
init_borad = [
    [chariot, empty, empty, pawn, empty, empty, pawn, empty, empty, chariot],
    [horse, empty, cannon, empty, empty, empty, empty, cannon, empty, horse],
    [elephant, empty, empty, pawn, empty, empty, pawn, empty, empty, elephant],
    [advisor, empty, empty, empty, empty, empty, empty, empty, empty, advisor],
    [king, empty, empty, pawn, empty, empty, pawn, empty, empty, king],
    [advisor, empty, empty, empty, empty, empty, empty, empty, empty, advisor],
    [elephant, empty, empty, pawn, empty, empty, pawn, empty, empty, elephant],
    [horse, empty, cannon, empty, empty, empty, empty, cannon, empty, horse],
    [chariot, empty, empty, pawn, empty, empty, pawn, empty, empty, chariot]
]

# MinMax boundary
max_val = 1000000
min_val = -1000000
# pieces evaluation
base_val = [0, 0, 500, 300, 300, 250, 250, 80]
mobile_val = [0, 0, 6, 12, 6, 1, 1, 15]
pos_val = [
    [  # empty
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [  # King
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        11, 2, 1, 0, 0, 0, 0, 0, 0, 0,
        15, 2, 1, 0, 0, 0, 0, 0, 0, 0,
        11, 2, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Chariot
        194, 200, 198, 204, 208, 208, 206, 206, 206, 206,
        206, 208, 208, 209, 212, 211, 213, 208, 212, 208,
        204, 206, 204, 204, 212, 211, 213, 207, 209, 207,
        212, 212, 212, 212, 214, 214, 216, 214, 216, 213,
        200, 200, 212, 214, 215, 215, 216, 216, 233, 214,
        212, 212, 212, 212, 214, 214, 216, 214, 216, 213,
        204, 206, 204, 204, 212, 211, 213, 207, 209, 207,
        206, 208, 208, 209, 212, 211, 213, 208, 212, 208,
        194, 205, 198, 204, 208, 208, 206, 206, 206, 206
    ],
    [  # Horse
        88, 85, 93, 92, 90, 90, 93, 92, 90, 90,
        85, 90, 92, 94, 98, 100, 108, 98, 96, 90,
        90, 92, 94, 98, 101, 99, 100, 99, 103, 90,
        88, 93, 95, 95, 102, 103, 107, 103, 97, 96,
        90, 78, 92, 98, 103, 104, 100, 99, 94, 90,
        88, 93, 95, 95, 102, 103, 107, 103, 97, 96,
        90, 92, 94, 98, 101, 99, 100, 99, 103, 90,
        85, 90, 92, 94, 98, 100, 108, 98, 96, 90,
        88, 85, 93, 92, 90, 90, 93, 92, 90, 90
    ],
    [  # Cannon
        96, 96, 97, 96, 95, 96, 96, 97, 98, 100,
        96, 97, 96, 96, 96, 96, 99, 97, 98, 100,
        97, 98, 100, 96, 99, 96, 99, 96, 96, 96,
        99, 98, 99, 96, 96, 96, 98, 91, 92, 91,
        99, 98, 101, 96, 100, 100, 100, 92, 89, 90,
        99, 98, 99, 96, 96, 96, 98, 91, 92, 91,
        97, 98, 100, 96, 99, 96, 99, 96, 96, 96,
        96, 97, 96, 96, 96, 96, 99, 97, 98, 100,
        96, 96, 97, 96, 95, 96, 96, 97, 98, 100
    ],
    [  # Elephant
        0, 0, 28, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        30, 0, 0, 0, 30, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 33, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        30, 0, 0, 0, 30, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 28, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Advisor
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        30, 0, 30, 0, 0, 0, 0, 0, 0, 0,
        0, 33, 0, 0, 0, 0, 0, 0, 0, 0,
        30, 0, 30, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Pawn
        0, 0, 0, 7, 7, 14, 19, 19, 19, 9,
        0, 0, 0, 0, 0, 18, 23, 24, 24, 9,
        0, 0, 0, 7, 13, 20, 27, 32, 34, 9,
        0, 0, 0, 0, 0, 27, 29, 37, 42, 11,
        0, 0, 0, 15, 16, 29, 30, 37, 44, 13,
        0, 0, 0, 0, 0, 27, 29, 37, 42, 11,
        0, 0, 0, 7, 13, 20, 27, 32, 34, 9,
        0, 0, 0, 0, 0, 18, 23, 24, 24, 9,
        0, 0, 0, 7, 7, 14, 19, 19, 19, 9
    ]
]
