"""Static title layout preview, not a Pygame runtime screenshot.

Requires Pillow only for asset-generation. The game does not require Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
BG=Image.open(ROOT/'assets/forest.png').convert('RGBA')
D=ImageDraw.Draw(BG,'RGBA')


def font(sz,bold=False):
    location=('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if bold and sz>=24
              else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if bold
              else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
    try:return ImageFont.truetype(location,sz)
    except OSError:return ImageFont.load_default()


def panel(x,y,w,h,radius=24):
    D.rounded_rectangle([x,y,x+w,y+h],radius=3,fill=(236,224,189,247),outline=(75,59,48,255),width=3)


def button(x,y,w,h,label,bg,size=19):
    D.rounded_rectangle([x,y,x+w,y+h],radius=2,fill=bg,outline=(75,59,48),width=3)
    D.text((x+w/2,y+h/2),label,font=font(size,True),fill=(40,54,48),anchor='mm')


def sprite(name,cx,cy,w,h):
    img=Image.open(ROOT/f'assets/{name}.png').convert('RGBA').resize((w,h),Image.Resampling.NEAREST)
    BG.alpha_composite(img,(int(cx-w/2),int(cy-h/2)))

panel(44,72,745,579,29)
D.text((94,105),'MUD PIE',font=font(77,True),fill=(47,76,66))
D.text((94,188),'MASTERS',font=font(77,True),fill=(47,76,66))
D.text((97,303),'A very serious contest about dirt.',font=font(26,True),fill=(40,54,48))
D.text((96,355),'36 story contests, 12 woodland commissions, six chapters,',font=font(17),fill=(40,54,48))
D.text((96,379),'and two very competitive siblings.',font=font(17),fill=(40,54,48))
D.text((96,415),'Story 0/36  ·  Commissions 0/12  ·  0 stars',font=font(18,True),fill=(47,76,66))
button(96,451,332,57,'CONTINUE THE STORY',(198,154,93))
button(443,451,284,57,'CHAPTER MAP',(216,197,155))
button(96,521,332,54,'FREE-BUILD MEADOW',(216,197,155))
button(443,521,284,54,'MY SCRAPBOOK',(216,197,155))
button(96,593,235,42,'SETTINGS',(216,197,155))
D.text((349,604),'Round 1 · 0 min in game',font=font(16),fill=(40,54,48))
sprite('player',956,400,330,396)
sprite('bruno',844,538,170,206)
sprite('daisy',1127,517,190,226)
D.rounded_rectangle((837,77,1198,130),radius=3,fill=(216,197,155),outline=(126,99,73),width=2)
D.text((852,95),'No eating the entries, cubs!',font=font(19,True),fill=(40,54,48))
D.rounded_rectangle((298,670,1003,702),radius=2,fill=(31,52,46,244))
D.text((650,685),'STATIC ART / LAYOUT PREVIEW — NOT A LIVE GAME SCREENSHOT',
       font=font(13,True),fill=(255,251,222),anchor='mm')
target=ROOT/'docs/title_art_preview.png'
BG.convert('RGB').save(target,optimize=True)
print(target)
