"""Hand-authored, deterministic pixel art for MUD PIE MASTERS.

No AI-generated images, photo filters, gradients, or downloaded assets.
Everything is constructed from a shared small palette with pixel-level marks.
The PNGs are build-time assets: pygame-ce remains the only runtime dependency.
"""
from __future__ import annotations
from pathlib import Path
from random import Random
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets'
P={
 'night':'#192b28','ink':'#283630','pine':'#2f4c42','pine2':'#3b604b',
 'sage':'#638167','moss':'#77916b','leaf':'#a7ac6b','gold':'#d1ad67',
 'light':'#e2d4a5','paper':'#d8c59b','darkpaper':'#b5a077','wood':'#825c44',
 'woodlight':'#ab7953','wooddark':'#503d35','sienna':'#aa6847','rust':'#c48651',
 'sand':'#dab38a','fur':'#98633f','fur2':'#b77d4f','shadow':'#503b34',
 'warm':'#f0d6a3','flower':'#c78978','flower2':'#d8b185','blue':'#69858a',
 'berry':'#88515a','cream':'#ece0bd','white':'#faf0d2'
}

def col(key):return P.get(key,key)

def rect(d, xy, c): d.rectangle(xy,fill=col(c))
def poly(d, points, c): d.polygon(points, fill=col(c))
def ell(d, xy, c): d.ellipse(xy,fill=col(c))

def leaf(d,x,y,base='pine2',s=1):
    poly(d,[(x,y+4*s),(x+2*s,y),(x+6*s,y-3*s),(x+7*s,y+1*s),(x+5*s,y+6*s)],base)
    d.line((x+1*s,y+4*s,x+7*s,y-2*s),fill=col('leaf'),width=max(1,s))

def draw_bear(name,body,belly,outline,personality):
    im=Image.new('RGBA',(150,180),(0,0,0,0));d=ImageDraw.Draw(im)
    rng=Random(sum(map(ord,name))*71)
    # Realistically broad, low cub silhouette with asymmetric ears, no giant glassy eyes.
    left=20 if personality=='bruno' else 26
    right=126 if personality=='bruno' else 124
    ell(d,(37,149,117,166),'night')
    ell(d,(32,130,68,167),outline);ell(d,(91,133,131,167),outline)
    ell(d,(38,135,70,160),body);ell(d,(94,136,125,160),body)
    # Left/back arm visible, slight asymmetry.
    ell(d,(21,93,63,145),outline);ell(d,(25,95,61,139),body)
    ell(d,(87,100,137,150),outline);ell(d,(89,102,131,143),body)
    ell(d,(41,84,114,153),outline);ell(d,(45,87,111,149),body)
    ell(d,(59,106,99,142),belly)
    # Ears have squared silhouettes and two-tone inset centers.
    ell(d,(left,27,left+41,72),outline);ell(d,(left+4,31,left+37,65),body)
    ell(d,(right-29,23,right+13,70),outline);ell(d,(right-25,28,right+7,63),body)
    ell(d,(left+11,40,left+26,56),'sienna');ell(d,(right-17,37,right-1,53),'sienna')
    # Head is a lopsided organic polygon, rather than perfect circle.
    poly(d,[(31,64),(36,50),(46,39),(60,33),(80,31),(100,37),(116,47),(125,64),(128,87),
            (122,104),(110,117),(89,122),(67,121),(45,112),(33,100),(27,82)],outline)
    poly(d,[(35,64),(40,53),(53,44),(67,38),(86,37),(104,42),(117,55),(121,67),
            (123,86),(116,100),(104,110),(85,115),(67,113),(48,105),(38,94),(34,79)],body)
    # Fur edges: sparse jagged pixels imply coat texture instead of airbrushed gradients.
    for k in range(57):
        x=rng.randrange(37,120); y=rng.randrange(46,110)
        if rng.random() < .35:
            d.line((x,y,x+1,y+2), fill=col('fur2' if k%3 else 'shadow'),width=1)
    for x,y in [(32,61),(28,73),(29,93),(42,104),(54,116),(104,110),(121,99),(125,75),(110,49)]:
        poly(d,[(x,y),(x-3,y-3),(x+2,y-2),(x+3,y+3)],body)
    # Three-dimensional short snout, intentionally small dark eyes.
    ell(d,(58,78,101,111),belly)
    ell(d,(66,87,96,110),'sand')
    ell(d,(65,70,72,77),'ink');ell(d,(99,69,106,76),'ink')
    rect(d,(67,71,68,72),'white');rect(d,(101,70,102,71),'white')
    ell(d,(79,82,91,89),outline);ell(d,(83,83,88,85),'shadow')
    d.line((85,90,85,96),fill=col('ink'),width=2)
    d.line([(85,96),(79,99),(74,96)],fill=col('ink'),width=2)
    d.line([(85,96),(90,98),(94,95)],fill=col('ink'),width=2)
    # Some emotion-specific brows/eye shapes; subtle not emoji expressions.
    if personality=='bruno':
        d.line((60,66,75,71),fill=col(outline),width=3)
        d.line((95,71,111,65),fill=col(outline),width=3)
    elif personality=='daisy':
        d.arc((62,71,72,82),180,345,fill=col(outline),width=1)
        d.arc((98,70,109,81),190,350,fill=col(outline),width=1)
    # Visible paws and 3 small claws each; fixed articulation matches all screens.
    ell(d,(26,118,57,144),outline);ell(d,(29,118,56,140),body)
    ell(d,(112,118,138,144),outline);ell(d,(113,119,134,140),body)
    for bx in (37,48):
        for j in range(2):rect(d,(bx+j*3,131,bx+j*3+1,134),'shadow')
    for bx in (117,125):rect(d,(bx,131,bx+1,134),'shadow')
    if personality=='player':
        # Brick-red woven neckerchief with low-res stitched border.
        poly(d,[(54,113),(83,118),(108,109),(105,124),(86,134),(71,126),(62,141)],'sienna')
        d.line([(58,117),(87,126),(103,115)],fill=col('flower2'),width=2)
        poly(d,[(75,128),(82,130),(77,144),(68,141)],'rust')
        rect(d,(44,85,49,87),'shadow');rect(d,(53,91,57,92),'shadow')
    elif personality=='bruno':
        poly(d,[(42,115),(77,120),(119,109),(111,130),(89,129),(82,143),(68,132)],'blue')
        d.line([(45,117),(78,124),(111,116)],fill=col('light'),width=1)
        # Distinctively messier fur and mud stain.
        for x,y in ((48,91),(53,95),(57,91),(104,139),(108,135)):
            rect(d,(x,y,x+5,y+2),'shadow')
    elif personality=='daisy':
        # Tiny wildflower behind one ear, dark purple scarf clasp.
        ell(d,(112,32,124,44),'flower');ell(d,(107,38,119,48),'flower2')
        ell(d,(119,40,131,50),'flower');ell(d,(118,29,131,40),'flower2')
        ell(d,(117,38,122,43),'gold')
        poly(d,[(49,113),(77,120),(114,113),(105,126),(75,128),(58,126)],'moss')
        poly(d,[(79,124),(94,134),(82,140)],'leaf')
    elif personality=='petal':
        for x,y in [(63,36),(73,33),(84,32),(97,34)]:
            ell(d,(x-3,y-3,x+4,y+4),'flower')
            rect(d,(x,y,x+1,y+1),'gold')
    elif personality=='boulder':
        # Distinct dark muzzle and heavy brow.
        d.line((55,65,75,67),fill=col(outline),width=4)
        d.line((96,67,113,65),fill=col(outline),width=4)
    elif personality=='fern':
        # Monocle and leaf badge suggest meticulousness.
        d.ellipse((92,63,113,83),outline=col('wooddark'),width=2)
        d.line((113,79,120,91),fill=col('wooddark'),width=2)
        leaf(d,112,46,'sage',1)
    # Tiny fur stitches break mass of flat fill.
    for x,y in ((46,58),(113,56),(38,88),(119,85),(55,137),(98,142)):
        d.line((x,y,x+2,y+1),fill=col('fur2'),width=1)
    # Pixel snap scaling: nearest neighbor, no smooth color interpolation.
    im.resize((300,360),Image.Resampling.NEAREST).save(ASSETS/(name+'.png'))


def hill(d, pts, fill):poly(d,pts,fill)

def pine_tree(d,x,y,height,color,seed):
    rng=Random(seed); h=height; trunk=int(h*.095)
    rect(d,(x-trunk//2,y-h//2,x+trunk//2,y+7),'wooddark')
    for k in range(3):
        yy=int(y-h*.95+k*h*.22); width=int(h*.38+k*h*.035)
        poly(d,[(x,yy-8),(x-width,yy+int(h*.45)),(x+width,yy+int(h*.45))],color)
        for q in range(10):
            px=x+rng.randrange(-width+4,width-4);py=yy+rng.randrange(10,int(h*.35)+10)
            rect(d,(px,py,px+rng.randrange(2,5),py+1),'sage' if k%2 else 'pine')


def forest():
    im=Image.new('RGB',(640,360),col('paper'));d=ImageDraw.Draw(im)
    rect(d,(0,0,639,203),'darkpaper')
    rect(d,(0,0,639,108),'sage')
    rect(d,(0,109,639,169),'moss')
    hill(d,[(0,155),(63,127),(135,144),(194,115),(295,160),(389,128),(468,139),(559,111),(640,146),(640,260),(0,260)],'sage')
    hill(d,[(0,170),(59,150),(125,159),(208,135),(315,182),(405,145),(493,172),(576,140),(640,167),(640,288),(0,288)],'pine2')
    rng=Random(124)
    # Patches of atmosphere in bounded color fields (never airbrushed gradients).
    for i in range(18):
        x=rng.randrange(-20,670);y=rng.randrange(140,223)
        pine_tree(d,x,y,rng.randrange(60,112),'pine',i+40)
    hill(d,[(0,222),(73,198),(142,217),(226,205),(301,224),(376,211),(468,219),(546,206),(640,222),(640,359),(0,359)],'moss')
    # Stage clearing with deliberate rough pixels, not ellipse blur.
    hill(d,[(102,296),(149,270),(235,254),(344,249),(475,262),(542,282),(560,309),(540,346),(124,356),(89,329)],'wooddark')
    hill(d,[(110,295),(158,274),(246,262),(363,259),(465,268),(531,284),(545,304),(523,338),(134,343),(105,324)],'darkpaper')
    for _ in range(180):
        x=rng.randrange(80,550);y=rng.randrange(258,353)
        # Tiny pixel flecks on the clearing rather than continuous noise.
        if ((x-318)/238)**2+((y-304)/55)**2<1:
            rect(d,(x,y,x+rng.randrange(1,4),y+1),rng.choice(['paper','woodlight','wood','light']))
    # Framing foreground fern fronds and woodland mushrooms.
    for side in (0,1):
        for k in range(23):
            x=(rng.randrange(0,110) if side==0 else rng.randrange(525,640))
            y=rng.randrange(225,360);leaf(d,x,y,rng.choice(['pine','pine2','leaf','sage']),rng.randrange(1,3))
    for x,y in ((90,296),(566,300),(587,263),(71,259)):
        rect(d,(x,y,x+3,y+9),'light')
        poly(d,[(x-5,y),(x+8,y),(x+5,y-5),(x-2,y-6)],'rust')
    for _ in range(120):
        x=rng.randrange(0,640);y=rng.randrange(211,360)
        if 120<x<520 and y>265:continue
        rect(d,(x,y,x+1,y+1),rng.choice(['sage','leaf','pine','gold']))
    im.resize((1280,720),Image.Resampling.NEAREST).save(ASSETS/'forest.png', optimize=True)


def table():
    im=Image.new('RGB',(640,360),col('paper'));d=ImageDraw.Draw(im)
    rect(d,(0,0,639,151),'sage');rect(d,(0,140,639,189),'pine2')
    rng=Random(97)
    for i in range(16):
        x=i*45+rng.randrange(-20,20)
        pine_tree(d,x,193,rng.randrange(95,180),rng.choice(['pine','pine2']),i*7+4)
    # Raw plank table, chunky board edges, exposed joinery, raised craft surface.
    poly(d,[(19,178),(612,178),(637,344),(0,344)],'wooddark')
    poly(d,[(22,180),(614,180),(622,337),(15,337)],'wood')
    poly(d,[(24,180),(611,180),(616,200),(19,201)],'woodlight')
    for i in range(5):
        y=205+i*27
        d.line([(20,y),(614,y+3)],fill=col('wooddark'),width=3)
        d.line([(24,y+3),(609,y+5)],fill=col('rust'),width=1)
        for j in range(31):
            x=rng.randrange(24,609); yy=y+rng.randrange(6,26)
            d.line((x,yy,x+rng.randrange(2,20),yy),fill=col('woodlight'),width=1)
    # Platter leaves and a broad working disc (visual center exactly where physics places pie).
    ell(d,(193,260,470,333),'wooddark')
    ell(d,(199,258,465,326),'darkpaper')
    ell(d,(209,264,453,320),'woodlight')
    ell(d,(219,266,441,314),'paper')
    for k in range(22):
        x=rng.randrange(230,435);y=rng.randrange(275,315)
        rect(d,(x,y,x+2,y+1),'darkpaper')
    # Frayed stitched burlap strip at rear, bottle of mud, loose leaves.
    rect(d,(149,176,501,185),'darkpaper');rect(d,(153,179,497,181),'gold')
    for x,y in ((180,197),(505,218),(521,201)):
        leaf(d,x,y,'pine2',2)
    im.resize((1280,720),Image.Resampling.NEAREST).save(ASSETS/'table.png',optimize=True)


def main():
    forest();table()
    presets={
      'player':('fur','sand','shadow','player'),
      'bruno':('wood','sand','wooddark','bruno'),
      'daisy':('fur2','warm','shadow','daisy'),
      'petal':('rust','light','shadow','petal'),
      'boulder':('wooddark','fur','night','boulder'),
      'fern':('fur','light','night','fern')}
    for n,p in presets.items():draw_bear(n,*p)
    print('Created pixel-art backgrounds and 6 matching character sprites.')

if __name__=='__main__':main()
