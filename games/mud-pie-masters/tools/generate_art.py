"""Canonical reproducible original asset build, including v0.4 infant cubs.

Requires Pillow at build time only; running the game still requires pygame-ce.
The cub generator runs AFTER the base pixel art generator and replaces its old
character sprites with the current 12 expression frames.
"""
from generate_pixel_art import main as base_art
from generate_cute_cubs import main as baby_cubs

if __name__ == '__main__':
    base_art()
    baby_cubs()
