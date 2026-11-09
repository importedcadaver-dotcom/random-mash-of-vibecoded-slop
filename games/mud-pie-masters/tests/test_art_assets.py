"""Asset-pack invariants without requiring Pillow or a graphical display."""
from pathlib import Path
from struct import unpack
import hashlib

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'

def png_size(name):
    data = (ASSETS / name).read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n'
    assert data[12:16] == b'IHDR'
    return unpack('>II',data[16:24])


def test_six_distinct_character_sprites_have_expected_dimensions():
    characters = ('player','bruno','daisy','petal','boulder','fern')
    assert all(png_size(f'{n}.png') == (300,360) for n in characters)
    hashes = [hashlib.sha256((ASSETS / (name+'.png')).read_bytes()).hexdigest()
              for name in characters]
    assert len(set(hashes)) == 6


def test_both_game_backdrops_match_logical_resolution():
    assert png_size('forest.png') == (1280,720)
    assert png_size('table.png') == (1280,720)


def test_new_pixel_art_source_and_style_guide_shipped():
    assert (ROOT / 'tools/generate_pixel_art.py').is_file()
    assert (ROOT / 'ART_DIRECTION.md').is_file()
    assert (ROOT / 'docs/title_art_preview.png').is_file()
    assert (ROOT / 'docs/craft_layout_preview.png').is_file()


def test_v04_cubs_have_readable_animated_emotions():
    """Three personalities × four authored face/pose frames, correct size."""
    for who in ('player', 'bruno', 'daisy'):
        frames = [f'{who}.png'] + [f'{who}_{emotion}.png' for emotion in ('blink','cheer','sad')]
        assert all(png_size(name) == (300, 360) for name in frames)
        assert len({hashlib.sha256((ASSETS / name).read_bytes()).digest() for name in frames}) == 4


def test_v04_main_cubs_are_not_identical_across_personalities():
    for emotion in ('idle','blink','cheer','sad'):
        names=[who + ('' if emotion=='idle' else f'_{emotion}') + '.png'
               for who in ('player','bruno','daisy')]
        assert len({hashlib.sha256((ASSETS / name).read_bytes()).digest() for name in names}) == 3


def test_v04_reproducible_generator_and_preview_are_included():
    assert (ROOT / 'tools/generate_cute_cubs.py').is_file()
    assert (ROOT / 'docs/v04_cub_reveal.png').is_file()
    assert (ROOT / 'docs/v04_before_after.png').is_file()
    text=(ROOT/'tools/generate_art.py').read_text(encoding='utf-8')
    assert 'generate_cute_cubs' in text


def test_v04_art_does_not_require_pillow_at_runtime():
    # Only tools may depend on Pillow. The game uses PNGs directly via pygame.
    for path in (ROOT/'mudpie').glob('*.py'):
        content=path.read_text(encoding='utf-8')
        assert 'from PIL import ' not in content
        assert 'import PIL' not in content
