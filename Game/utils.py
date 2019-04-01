import pygame;
import sys


def load():

    #Convert alpha is used to convert surfaces to the same pixel format as used by the screen.

    CHOSEN_PLAYER_PATH = (
        'GameAssets/Sprites/redbird-upflap.png',
        'GameAssets/Sprites/redbird-midflap.png',
        'GameAssets/Sprites/redbird-downflap.png'
    )

    GAME_BACKGROUND = 'GameAssets/Sprites/background-black.png'

    GAME_PIPE = 'GameAssets/Sprites/pipe-green.png'

    IMAGES, GAME_SOUND, HITMASKS = {}, {}, {}

    IMAGES['numbers'] = (
        pygame.image.load('GameAssets/Sprites/0.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/1.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/2.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/3.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/4.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/5.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/6.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/7.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/8.png').convert_alpha(),
        pygame.image.load('GameAssets/Sprites/9.png').convert_alpha()
    )

    IMAGES['base'] = pygame.image.load('GameAssets/Sprites/base.png').convert_alpha()
    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    GAME_SOUND['die'] = pygame.mixer.Sound('GameAssets/Game_Audio/die' + soundExt)
    GAME_SOUND['hit'] = pygame.mixer.Sound('GameAssets/Game_Audio/hit' + soundExt)
    GAME_SOUND['point'] = pygame.mixer.Sound('GameAssets/Game_Audio/point' + soundExt)
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('GameAssets/Game_Audio/swoosh' + soundExt)
    GAME_SOUND['wing'] = pygame.mixer.Sound('GameAssets/Game_Audio/wing' + soundExt)

    IMAGES['background'] = pygame.image.load(GAME_BACKGROUND).convert()

    # select random player sprites
    IMAGES['Player'] = (
        pygame.image.load(CHOSEN_PLAYER_PATH[0]).convert_alpha(),
        pygame.image.load(CHOSEN_PLAYER_PATH[1]).convert_alpha(),
        pygame.image.load(CHOSEN_PLAYER_PATH[2]).convert_alpha(),
    )

    IMAGES['pipe'] = (
        pygame.transform.rotate(
            pygame.image.load(GAME_PIPE).convert_alpha(), 180),
        pygame.image.load(GAME_PIPE).convert_alpha(),
    )
    # hismask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
    )

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
    )
    return IMAGES, GAME_SOUND, HITMASKS


def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    # 'alpha' attribute of a picture
    # if alpha is 1 means image opaque otherwise transparent
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask


