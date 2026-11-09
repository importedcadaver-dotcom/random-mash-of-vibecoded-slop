"""Static proof sheets made from the exact pixel PNGs shipped in the game.

The old comparator is read from the previous source archive when available.
These sheets are not live Pygame captures.
"""
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
DOCS.mkdir(exist_ok=True)
PALETTE={'ink':'#203d34','bg':'#eaddbe','panel':'#fff3d4','border':'#66513e','light':'#f8da91','muted':'#746550'}

def font(size,bold=False):
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'] if bold else ['/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf']
    for p in paths:
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def paste(im, src, x,y,w,h):
    pic=src.convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
    im.paste(pic,(x,y),pic)

def sheet():
    im=Image.new('RGB',(1340,810),PALETTE['bg']);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1340,102),fill=PALETTE['ink'])
    d.text((42,23),'MUD PIE MASTERS  /  CUB REVISION 04',font=font(33,True),fill='#f7eac6')
    d.text((42,71),'ORIGINAL PIXEL ASSETS   ·   150 × 180 BASE DRAWINGS   ·   NO AI-PAINTED SPRITES',font=font(15),fill='#d6cba5')
    entries=[('player','YOU','The eager little mud artist','red dotted kerchief'),
             ('bruno','BRUNO','The overconfident big brother','folded ear & blue bandana'),
             ('daisy','DAISY','The giggly little sister','flower and clasped paws')]
    for i,(key,label,desc,accent) in enumerate(entries):
        x=35+i*441
        d.rounded_rectangle((x,127,x+404,754),radius=8,fill=PALETTE['panel'],outline=PALETTE['border'],width=3)
        d.text((x+25,143),label,font=font(29,True),fill=PALETTE['ink'])
        d.text((x+25,186),desc,font=font(17),fill=PALETTE['muted'])
        paste(im,Image.open(ROOT/'assets'/f'{key}.png'),x+42,225,313,370)
        d.line((x+35,599,x+367,599),fill=PALETTE['border'],width=2)
        d.text((x+26,624),accent,font=font(16),fill=PALETTE['ink'])
        # 2 readable emotion miniatures per cub.
        for j,emotion in enumerate(('cheer','sad')):
            paste(im,Image.open(ROOT/'assets'/f'{key}_{emotion}.png'),x+24+j*198,656,75,89)
            d.text((x+103+j*198,692),emotion.upper(),font=font(14,True),fill=PALETTE['muted'])
    im.save(DOCS/'v04_cub_reveal.png',optimize=True)


def before_after():
    old=ROOT.parent/'MudPieMasters-v0.3.0.zip'
    if not old.exists():return
    w=1440;h=690
    im=Image.new('RGB',(w,h),PALETTE['bg']);d=ImageDraw.Draw(im)
    d.rectangle((0,0,w,82),fill=PALETTE['ink'])
    d.text((29,18),'BABY-CUB DESIGN COMPARISON',fill='#fff1cc',font=font(33,True))
    d.text((30,99),'BEFORE  ·  v0.3  —  flat, tiny-eyed bear symbols',fill='#775c4d',font=font(19,True))
    d.text((746,99),'AFTER  ·  v0.4  —  baby proportions, emotions, little paws',fill='#775c4d',font=font(19,True))
    for i,key in enumerate(('player','bruno','daisy')):
        x=16+i*236
        z=ZipFile(old)
        with z.open(f'assets/{key}.png') as f: o=Image.open(BytesIO(f.read())).convert('RGBA')
        paste(im,o,x+10,198,209,255)
        paste(im,Image.open(ROOT/'assets'/f'{key}.png'),738+i*233,198,209,255)
        d.text((x+25,490),key.upper(),font=font(19,True),fill=PALETTE['ink'])
        d.text((738+i*233+20,490),key.upper(),font=font(19,True),fill=PALETTE['ink'])
    d.line((727,83,727,644),fill=PALETTE['border'],width=3)
    d.rectangle((140,584,1300,650),fill='#ead3a3',outline=PALETTE['border'],width=2)
    d.text((165,601),'STATIC ART COMPARISON — BOTH SIDES FROM SOURCE PNGS, NOT LIVE GAMEPLAY',
           font=font(19,True),fill=PALETTE['ink'])
    im.save(DOCS/'v04_before_after.png',optimize=True)

if __name__=='__main__':
    sheet();before_after();print('Rendered v0.4 cub reveal and previous-vs-current sheets')
