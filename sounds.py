import pygame
import os

# Initialize the mixer
pygame.mixer.init()

# Sound effects dictionary
sounds = {}

def load_sounds():
    """Load all sound effects"""
    global sounds
    try:
        # Create empty sounds if sound files don't exist (to prevent errors)
        sounds['catch'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))  # 0.1 second of silence
        sounds['life'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))
        sounds['bomb'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))
        sounds['level_up'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))
        sounds['game_over'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))
        sounds['pause'] = pygame.mixer.Sound(buffer=bytearray([128] * 4410))
    except:
        # If there's any issue, create silent sounds
        sounds = {
            'catch': pygame.mixer.Sound(buffer=bytearray([128] * 4410)),
            'life': pygame.mixer.Sound(buffer=bytearray([128] * 4410)),
            'bomb': pygame.mixer.Sound(buffer=bytearray([128] * 4410)),
            'level_up': pygame.mixer.Sound(buffer=bytearray([128] * 4410)),
            'game_over': pygame.mixer.Sound(buffer=bytearray([128] * 4410)),
            'pause': pygame.mixer.Sound(buffer=bytearray([128] * 4410))
        }

def play_sound(sound_name):
    """Play a sound effect"""
    if sound_name in sounds:
        try:
            sounds[sound_name].play()
        except:
            pass  # Silent fail if sound can't be played

# Load sounds when module is imported
load_sounds()