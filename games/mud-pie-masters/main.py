"""Mud Pie Masters launcher. Requires Python 3.12+ and pygame-ce."""
import os
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT','1')
import pygame
from mudpie.game import Game


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.display.set_caption('Mud Pie Masters — a tiny forest contest')
    pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    Game(pygame.display.get_surface()).run()


if __name__=='__main__':
    main()
