"""v0.4 authored plush-cub pixel sprites, including actual animation expressions.

Build-time dependency: Pillow. Each sprite is drawn on a 150x180 pixel
canvas, then nearest-neighbor scaled to the existing 300x360 asset size.
No AI images, external artwork, smoothing, or downloaded font files.
"""
from __future__ import annotations
from pathlib import Path
from random import Random
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / 'assets'
OUT.mkdir(exist_ok=True)

# Very restrained, shared warm inks + material-specific fur palettes.
INK = '#322a2a'
DEEPEST = '#201f20'
SPARK = '#fff8e0'

CUBS = {
    'player': dict(body='#b9784a', light='#de9c68', shade='#8a5339', face='#efbf87', belly='#edc99a',
                   inside='#b86d73', scarf='#a94c42', scarf_light='#e19375', blush='#d58a79',
                   muzzle='#f8d8a6', nose='#463031', eyes='#332326', eyesize=10, head=0, bow='scarf'),
    'bruno': dict(body='#925b3b', light='#c28a5b', shade='#69422e', face='#d6a071', belly='#d9ad7d',
                  inside='#a96967', scarf='#466b76', scarf_light='#a1c5c0', blush='#a86e5c',
                  muzzle='#edc89a', nose='#35262b', eyes='#302329', eyesize=9, head=3, bow='bandana'),
    'daisy': dict(body='#cb955f', light='#f0ba80', shade='#9c6646', face='#ffe0a8', belly='#fbe1b2',
                  inside='#ce8584', scarf='#9b77a7', scarf_light='#e6c6df', blush='#f0a2a0',
                  muzzle='#fff0c7', nose='#604147', eyes='#3c2830', eyesize=11, head=-3, bow='ribbon'),
}


def ellipse(d, xy, fill, out=None, w=1):
    d.ellipse(xy, fill=fill, outline=out, width=w)


def poly(d, xy, fill):
    d.polygon(xy, fill=fill)


def line(d, xy, c, w=1):
    d.line(xy, fill=c, width=w, joint='curve')


def fur_highlights(im, cfg, seed):
    """Scatter short, fixed coat tufts ONLY inside alpha region, avoiding face."""
    rng = Random(seed)
    d = ImageDraw.Draw(im)
    # Visible warm thread-like marks, rather than arbitrary noise across the face.
    for _ in range(95):
        x = rng.randrange(30, 129)
        y = rng.choice([rng.randrange(34, 55), rng.randrange(116, 169)])
        if im.getpixel((x,y))[3] and im.getpixel((x,y))[:3] in {
            tuple(bytes.fromhex(cfg['body'][1:])),tuple(bytes.fromhex(cfg['light'][1:])),
        }:
            c = cfg['light'] if rng.random()>.5 else cfg['shade']
            line(d, [(x,y),(x+rng.choice((-2,-1,1,2)),y+1)], c)


def flower(d, x, y, color, center='#f6d68b', size=5):
    for dx,dy in [(-size,0),(size,0),(0,-size),(0,size),(-size//2,-size//2)]:
        ellipse(d,(x+dx-3,y+dy-3,x+dx+4,y+dy+4),INK)
        ellipse(d,(x+dx-2,y+dy-2,x+dx+3,y+dy+3),color)
    ellipse(d,(x-3,y-3,x+4,y+4),INK)
    ellipse(d,(x-2,y-2,x+3,y+3),center)


def eyes_and_mouth(d,cfg,who,emotion):
    # Our heads are broad with eyes lower than the skull's midline: infant proportions.
    xoffset = cfg['head']
    eyes = [(57+xoffset,79),(101+xoffset,77)]
    for cx,cy in eyes:
        if emotion in ('blink','cheer'):
            # Tiny joyful upturned crescent; not an emoji or a human eyebrow.
            d.arc((cx-7,cy-2,cx+7,cy+10),2,177,fill=INK,width=3)
            if emotion == 'cheer':
                line(d,[(cx-8,cy+2),(cx-11,cy)],cfg['shade'],2)
        else:
            # Glossy but NOT oversized anime eyes: narrow dark pupil, restrained glints.
            rx = cfg['eyesize']//2
            ellipse(d,(cx-rx-2,cy-7,cx+rx+2,cy+9),cfg['shade'])
            ellipse(d,(cx-rx,cy-7,cx+rx,cy+8),cfg['eyes'])
            d.rectangle((cx-rx+1,cy-5,cx-rx+3,cy-3),fill=SPARK)
            d.rectangle((cx+rx-1,cy+3,cx+rx,cy+4),fill=cfg['light'])
    if who == 'bruno':
        line(d,[(48,68),(58,71),(66,70)],cfg['shade'],2)
        line(d,[(93,69),(103,70),(113,65)],cfg['shade'],2)
    elif who == 'daisy':
        d.arc((45,65,62,73),190,335,fill=cfg['shade'],width=1)
    else:
        line(d,[(52,67),(62,65)],cfg['shade'],1)
        line(d,[(97,64),(107,66)],cfg['shade'],1)

    # Squishy cream cheek pads are the dominant expression feature.
    ellipse(d,(51,89,85,113),cfg['muzzle'])
    ellipse(d,(82,87,116,111),cfg['muzzle'])
    ellipse(d,(64,91,101,119),cfg['muzzle'])
    # Blush stays subtle, below the eyes but outside cream pads.
    ellipse(d,(43,94,54,100),cfg['blush'])
    ellipse(d,(112,92,123,98),cfg['blush'])
    for x in (47,51,115,119):
        d.point((x,101 if x<75 else 99),fill=cfg['shade'])
    if emotion=='sad':
        line(d,[(74,111),(80,108),(87,110),(92,114)],cfg['nose'],2)
        d.rectangle((53,85,56,88),fill='#b8cee0')
    elif emotion in ('cheer','idle'):
        # Open happy bear-cub mouth: nose and dark rounded oval, pink tongue.
        ellipse(d,(77,106,99,123),cfg['nose'])
        ellipse(d,(82,114,94,122),'#cd817c')
        d.rectangle((79,106,95,108),fill=cfg['muzzle'])
        if who=='bruno':
            poly(d,[(94,108),(99,109),(95,115)],SPARK)
    else:
        line(d,[(78,111),(85,115),(91,115),(97,110)],cfg['nose'],2)
    # Small low nose with a little highlighted bridge.
    ellipse(d,(81,97,95,105),INK)
    ellipse(d,(83,98,93,102),cfg['nose'])
    d.point((86,99),fill='#d2afa0')


def base_cub(who: str, emotion: str) -> Image.Image:
    c=CUBS[who]; im=Image.new('RGBA',(150,180),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Feet planted wide; broad soft paws have very short legs.
    ellipse(d,(33,151,76,177),INK)
    ellipse(d,(80,149,125,177),INK)
    ellipse(d,(38,149,76,171),c['shade'])
    ellipse(d,(82,149,122,171),c['shade'])
    ellipse(d,(41,152,72,167),c['body'])
    ellipse(d,(84,152,118,168),c['body'])
    # Tiny three toes with shadows: paw readability when rendered at 190px tall.
    for fx in [45,54,63,88,98,108]:
        line(d,[(fx,162),(fx+1,165)],c['shade'])

    # Small cuddly pear body, cheekily wider toward the bottom.
    ellipse(d,(36,102,125,169),INK)
    ellipse(d,(40,107,121,166),c['shade'])
    ellipse(d,(44,108,116,160),c['body'])
    ellipse(d,(59,116,104,160),c['belly'])
    ellipse(d,(65,120,98,151),c['face'])

    # Side arms peek out from behind head; paw poses vary by cub + animation.
    if emotion=='cheer':
        ellipse(d,(14,94,54,139),INK);ellipse(d,(17,96,50,136),c['body'])
        ellipse(d,(104,93,144,137),INK);ellipse(d,(107,96,141,133),c['body'])
        ellipse(d,(10,87,48,116),INK);ellipse(d,(13,90,45,113),c['light'])
        ellipse(d,(115,85,149,113),INK);ellipse(d,(117,88,145,110),c['light'])
    elif who=='bruno':
        ellipse(d,(17,104,58,151),INK);ellipse(d,(21,108,54,147),c['body'])
        ellipse(d,(105,105,147,150),INK);ellipse(d,(108,108,144,146),c['body'])
    elif who=='daisy':
        ellipse(d,(25,105,65,147),INK);ellipse(d,(28,107,62,143),c['body'])
        ellipse(d,(91,105,132,150),INK);ellipse(d,(94,107,129,145),c['body'])
    else:
        ellipse(d,(19,111,61,153),INK);ellipse(d,(22,112,58,149),c['body'])
        ellipse(d,(98,111,143,153),INK);ellipse(d,(103,113,139,149),c['body'])

    # Ear shape, including an asymmetric floppy Bruno ear and petal-like inner texture.
    ears = [(24,19,65,64),(100,18,141,64)]
    if who=='bruno': ears=[(20,20,63,62),(104,14,147,64)]
    if who=='daisy': ears=[(22,18,67,67),(98,17,143,62)]
    for i,b in enumerate(ears):
        ellipse(d,b,INK)
        ellipse(d,(b[0]+4,b[1]+3,b[2]-3,b[3]-3),c['shade'])
        ellipse(d,(b[0]+7,b[1]+5,b[2]-6,b[3]-6),c['body'])
        ellipse(d,(b[0]+12,b[1]+13,b[2]-12,b[3]-11),c['inside'])
        ellipse(d,(b[0]+16,b[1]+17,b[2]-14,b[3]-16),'#e7a69b' if who=='daisy' else c['blush'])
    if who=='bruno':
        poly(d,[(104,22),(117,16),(139,24),(146,30),(137,38),(127,31),(115,35)],c['shade'])

    # Enormous chubby head with little chin and tufts, leaving body very small.
    pts=[(21,80),(21,67),(27,48),(39,36),(52,31),(64,28),(88,27),(112,34),
         (126,44),(135,61),(136,84),(132,104),(124,117),(110,127),
         (95,132),(61,132),(44,126),(28,113)]
    poly(d,pts,INK)
    # Side cheek tufts create an irregular plush silhouette, not a disc.
    poly(d,[(22,85),(15,87),(21,94),(16,101),(29,108),(27,117),(42,123)],INK)
    poly(d,[(134,84),(143,90),(137,96),(143,104),(130,113),(127,121),(113,126)],INK)
    pts2=[(26,79),(26,66),(32,51),(43,41),(58,34),(72,32),(89,32),(109,38),
          (122,47),(129,62),(131,82),(127,100),(121,112),(107,121),(92,125),
          (63,125),(47,120),(33,110)]
    poly(d,pts2,c['shade'])
    pts3=[(30,78),(31,65),(37,53),(49,45),(64,38),(87,37),(109,43),
          (121,53),(125,64),(126,82),(121,102),(111,115),(92,122),
          (65,122),(49,115),(36,106)]
    poly(d,pts3,c['body'])
    # Large face mask softens harsh head brown; asymmetrical patch (very plush).
    poly(d,[(44,74),(49,55),(63,45),(82,44),(106,52),(118,69),(119,91),
            (107,109),(94,116),(66,115),(49,106),(42,91)],c['light'])
    ellipse(d,(45,53,116,118),c['face'])
    # Forehead brow follows eye line and is capped with fuzz.
    ellipse(d,(49,47,109,65),c['light'])
    # Short, rounded fur nibs instead of tall cartoon hair spikes.
    for tri in [[(33,53),(30,49),(31,58)],[(47,39),(45,34),(51,39)],
                [(70,33),(68,28),(74,33)],[(96,36),(98,31),(100,38)],
                [(121,50),(126,47),(124,56)],[(28,100),(24,98),(31,107)],
                [(124,101),(131,104),(125,109)]]:
        poly(d,tri,c['body'])
    # Highlighted forehead down: a few hand placed strands.
    for x,y in [(57,45),(62,42),(70,39),(85,40),(97,43),(105,46)]:
        line(d,[(x,y),(x+2,y+1)],c['light'])

    eyes_and_mouth(d,c,who,emotion)
    # Scarves have actual silhouette folds and an individual pattern.
    if who=='player':
        poly(d,[(42,120),(65,130),(88,132),(116,121),(109,144),(83,141),
                (71,163),(62,141),(47,140)],INK)
        poly(d,[(46,122),(68,132),(87,135),(113,125),(105,139),(82,137),
                (70,158),(65,138),(49,137)],c['scarf'])
        line(d,[(52,125),(75,137),(106,130)],c['scarf_light'],2)
        for x,y in ((59,131),(76,140),(89,134),(97,131),(69,149)):
            d.rectangle((x,y,x+2,y+2),fill='#f3c894')
        ellipse(d,(79,133,89,143),c['shade'])
    elif who=='bruno':
        poly(d,[(42,121),(68,131),(88,129),(118,119),(113,139),(91,141),
                 (82,160),(72,140),(55,144)],INK)
        poly(d,[(47,122),(69,133),(88,133),(115,124),(109,136),(88,138),
                 (81,154),(74,136),(58,140)],c['scarf'])
        line(d,[(52,126),(75,137),(105,130)],c['scarf_light'],2)
        d.rectangle((50,112,55,117),fill='#655144')
        d.rectangle((54,117,60,119),fill='#705344')
        d.rectangle((113,115,119,120),fill='#675246')
    else:
        poly(d,[(47,121),(72,131),(91,131),(111,122),(107,140),
                 (92,141),(82,157),(74,141),(52,140)],INK)
        poly(d,[(50,123),(75,134),(91,134),(108,126),(104,137),
                 (90,137),(83,151),(75,138),(55,137)],c['scarf'])
        line(d,[(58,127),(79,138),(101,131)],c['scarf_light'],2)
        poly(d,[(71,133),(79,137),(73,145),(65,139)],'#d8b5d9')
        poly(d,[(80,137),(89,133),(95,140),(86,145)],'#d8b5d9')
        flower(d,114,41,'#f2c0cf',size=4)
        d.line((107,42,101,39),fill='#6d955c',width=3)
    # Forepaws in front of scarves: Daisy's are clasped, player's one paw is lifted.
    if emotion!='cheer':
        if who=='daisy':
            ellipse(d,(58,136,88,164),INK);ellipse(d,(61,138,86,161),c['body'])
            ellipse(d,(78,136,107,163),INK);ellipse(d,(81,138,105,160),c['light'])
            line(d,[(81,140),(78,146)],c['shade'],2)
        elif who=='bruno':
            ellipse(d,(18,130,53,163),INK);ellipse(d,(21,132,50,160),c['light'])
            ellipse(d,(110,129,146,163),INK);ellipse(d,(112,132,143,159),c['light'])
            for x in (26,35,116,126): d.line((x,147,x,151),fill=c['shade'],width=2)
        else:
            ellipse(d,(22,126,57,163),INK);ellipse(d,(25,128,54,160),c['light'])
            ellipse(d,(109,125,144,160),INK);ellipse(d,(111,128,141,157),c['light'])
            # Little mud smudge on the player's paw, a character not clipart.
            ellipse(d,(117,142,125,146),'#855a47')
        # Small paw separations
        for x,y in ([(30,147),(40,146),(117,148),(127,147)] if who!='daisy' else [(69,150),(91,148)]):
            d.line((x,y,x+2,y+4),fill=c['shade'],width=1)
    else:
        # Oversized excited paw pads overlap the cheek edges for readable joy.
        ellipse(d,(5,96,39,130),INK); ellipse(d,(8,98,36,127),c['body'])
        ellipse(d,(116,93,149,126),INK); ellipse(d,(119,96,145,124),c['light'])
        for x,y in [(17,111),(27,109),(126,108),(136,106)]:
            d.line((x,y,x+1,y+4),fill=c['shade'],width=2)
    # Small deliberate fur nibs, never procedural cheek stubble.
    for x,y in [(31,105),(43,46),(123,106),(56,118),(109,117)]:
        d.line((x,y,x+2,y+2),fill=c['shade'],width=1)
    return im


def main():
    for who in CUBS:
        for emotion in ('idle','blink','cheer','sad'):
            im = base_cub(who,emotion).resize((300,360),Image.Resampling.NEAREST)
            name = who if emotion=='idle' else f'{who}_{emotion}'
            im.save(OUT/f'{name}.png', optimize=True)
    print('12 authored expression sprites written (3 cubs × 4 emotions).')

if __name__=='__main__':main()
