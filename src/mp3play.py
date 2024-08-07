import pygame

def alert(type):
    if type == 1:
        path = "assets/Speech On.wav"
    elif type == 2:
        path = "assets/Speech Off.wav"
    else:
        path = "assets/Speech Disambiguation.wav"

    pygame.init()
    pygame.mixer.init()

    pygame.mixer.music.load(path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)