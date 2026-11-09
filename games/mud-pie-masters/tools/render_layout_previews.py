"""Generate truthful *static layout previews* based on game assets/source, not runtime screenshots."""
from pathlib import Path
from math import cos,sin,radians
from PIL import Image,ImageDraw,ImageFont
from mudpie.models import Pie,evaluate_stability
from mudpie.judging import judge
from mudpie.rivals import make_entry,make_rivals
from mudpie.campaign import STORY,CHAPTERS,goal_progress

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'; OUT.mkdir(exist_ok=True)
W,H=1280,720
CREAM=(236,224,189); PAPER=(216,197,155); DARK=(47,76,66); INK=(40,54,48); BORDER=(75,59,48); GOLD=(209,173,103)

def f(sz,b=False):
 path='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if b and sz>=24 else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf' if b else '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
 return ImageFont.truetype(path,sz)

class Draw:
 def __init__(self,bg):
  self.img=Image.open(ROOT/f'assets/{bg}.png').convert('RGBA')
  self.d=ImageDraw.Draw(self.img,'RGBA')
 def box(self,x,y,w,h,fill=CREAM,r=20,border=BORDER,alpha=240,bw=2):
  self.d.rounded_rectangle((x,y,x+w,y+h),radius=min(3,r),fill=tuple(fill)+(alpha,),outline=tuple(border)+(255,) if border else None,width=bw)
  if w>35 and h>20 and border:
   self.d.line((x+6,y+6,x+15,y+6),fill=border,width=1)
   self.d.line((x+w-15,y+h-7,x+w-6,y+h-7),fill=border,width=1)
 def text(self,t,x,y,size=18,color=INK,b=False,maxwidth=None,anchor=None):
  t=str(t)
  if maxwidth and self.d.textbbox((0,0),t,font=f(size,b))[2]>maxwidth:
   while t and self.d.textbbox((0,0),t+'…',font=f(size,b))[2]>maxwidth:t=t[:-1]
   t+='…'
  self.d.text((x,y),t,font=f(size,b),fill=color,anchor=anchor)
 def center(self,t,x,y,size=18,color=INK,b=False): self.text(t,x,y,size,color,b,anchor='mm')
 def button(self,x,y,w,h,label,primary=False,active=False,small=False):
  self.box(x+2,y+3,w,h,(47,52,42),2,None,255,1)
  self.box(x,y,w,h,(198,154,93) if primary else (178,191,138) if active else PAPER,2,fillborder(),255,2)
  self.center(label,x+w/2,y+h/2,16 if small else 19,INK,True)
 def sprite(self,n,x,y,w,h):
  im=Image.open(ROOT/f'assets/{n}.png').convert('RGBA').resize((int(w),int(h)),Image.Resampling.NEAREST)
  self.img.alpha_composite(im,(int(x-w/2),int(y-h/2)))
 def heading(self,title,sub):
  self.d.rectangle((0,0,1280,94),fill=(31,52,46,251))
  self.text(title,38,12,36,CREAM,True,maxwidth=1130)
  self.text(sub,41,61,17,(212,198,160),maxwidth=1200)
 def stamp(self):
  self.box(364,684,550,28,(31,52,46),2,None,238,1)
  self.center('STATIC LAYOUT PREVIEW  •  NOT CAPTURED GAMEPLAY',639,697,12,(255,251,222),True)
 def save(self,name):
  self.stamp()
  p=OUT/name
  self.img.convert('RGB').save(p,optimize=True)
  print(p)

def fillborder():return BORDER

def ellipse(d, rect, c, outline=None):d.ellipse(tuple(map(int,rect)),fill=c,outline=outline)

def ingredient(dr,kind,x,y,sz=1,angle=0,color=0):
 d=dr.d;r=10*sz
 if kind=='mud':
  ellipse(d,(x-17*sz,y-9*sz,x+17*sz,y+10*sz),(86,55,35))
  ellipse(d,(x-15*sz,y-10*sz,x+15*sz,y+4*sz),(143,91,56))
  ellipse(d,(x-9*sz,y-6*sz,x,y-3*sz),(196,134,89))
 elif kind=='leaves':
  a=radians(angle);c=(70,121,68)
  pts=[(x+cos(a)*25*sz,y+sin(a)*25*sz),(x+cos(a+1.15)*14*sz,y+sin(a+1.15)*14*sz),(x-cos(a)*20*sz,y-sin(a)*20*sz),(x+cos(a-1.15)*14*sz,y+sin(a-1.15)*14*sz)]
  d.polygon(pts,fill=c);d.line((pts[0],pts[2]),fill=(216,223,154),width=max(1,int(sz*2)))
 elif kind=='petals':
  cs=[(235,152,169),(250,215,151),(220,194,224),(250,234,214),(167,215,235),(239,134,94)]
  for deg in range(0,360,72):
   rr=radians(deg+angle);cx=x+cos(rr)*r*.9;cy=y+sin(rr)*r*.9
   ellipse(d,(cx-r*.66,cy-r*.66,cx+r*.66,cy+r*.66),cs[color%6])
  ellipse(d,(x-4*sz,y-4*sz,x+4*sz,y+4*sz),(250,209,113))
 elif kind=='pebbles':
  ellipse(d,(x-11*sz,y-7*sz,x+13*sz,y+11*sz),(98,105,105));ellipse(d,(x-11*sz,y-9*sz,x+11*sz,y+6*sz),(160,171,160))
  ellipse(d,(x-7*sz,y-7*sz,x,y-4*sz),(217,223,211))
 elif kind=='sticks':
  ex=cos(radians(angle))*21*sz;ey=sin(radians(angle))*21*sz
  d.line((x-ex,y-ey,x+ex,y+ey),fill=(84,53,39),width=max(3,int(sz*8)))
  d.line((x-ex,y-ey-2*sz,x+ex,y+ey-2*sz),fill=(178,128,83),width=max(1,int(sz*3)))
 elif kind=='berries':
  for dx,dy in ((-8,2),(6,3),(0,-6)):
   ellipse(d,(x+(dx-8)*sz,y+(dy-8)*sz,x+(dx+8)*sz,y+(dy+8)*sz),(97,43,77))
   ellipse(d,(x+(dx-6)*sz,y+(dy-6)*sz,x+(dx+6)*sz,y+(dy+6)*sz),(180,72,103))

def pie_draw(dr,pie,bx,by,s=1):
 d=dr.d
 if not pie.layers:return
 ellipse(d,(bx-140*s,by-14*s,bx+140*s,by+15*s),(61,49,42))
 ellipse(d,(bx-131*s,by-12*s,bx+131*s,by+7*s),(157,121,81))
 height=0
 for i,l in enumerate(pie.layers):
  if l.fallen:continue
  w,h=l.width*s,l.height*s;height+=h;x=bx+l.x*s-w/2;y=by-height
  n=max(7,int(w//13))
  up=[(x+w*k/n,y+((k*7+(i+int(l.width*.1))*13)%9-4)*min(1,h/35)) for k in range(n+1)]
  lower=[(x+w-5*s,y+h*.35),(x+w+3*s,y+h*.82),(x+w*.91,y+h),(x+w*.17,y+h+3*s),(x-3*s,y+h*.77),(x+5*s,y+h*.4)]
  d.polygon(up+lower,fill=(62,46,39))
  d.polygon([(x+4*s,y+9*s),(x+w-5*s,y+10*s),(x+w-9*s,y+h-5*s),(x+8*s,y+h-6*s)],
            fill=(104,68,50) if l.wetness<.75 else (83,57,46))
  for j in range(3):
   yy=y+h*.3+j*h*.16
   d.line([(x+11*s,yy+2*s),(x+w*.35,yy-3*s),(x+w*.7,yy+2*s),(x+w-8*s,yy-2*s)],fill=(76,51,41),width=max(1,int(2*s)))
  d.polygon(up+[(x+w-7*s,y+13*s),(x+w*.66,y+17*s),(x+w*.27,y+15*s),(x+6*s,y+11*s)],fill=(158,110,72))
  d.line(up[2:-2],fill=(190,143,91),width=max(1,int(2*s)))
  for k in range(28):
   u=((k*47+i*31)%101)/101;v=((k*17+i*13)%89)/89
   px=x+11*s+(w-22*s)*u;py=y+15*s+(h-27*s)*v
   sz=max(1,int((2+k%3)*s))
   d.rectangle((px,py,px+sz,py+max(1,sz//2)),fill=(161,115,78) if k%4 else (55,43,35))
 for q in pie.decorations:
  if q.layer>=len(pie.layers) or pie.layers[q.layer].fallen:continue
  h=sum(l.height for l in pie.layers[:q.layer+1] if not l.fallen);l=pie.layers[q.layer]
  px=bx+s*(l.x+q.x*l.width*.44);py=by-s*h+s*l.height*q.y*.77
  ingredient(dr,q.kind,px,py,s*.9,q.angle,q.color)

def player_pie():
 pie=Pie(title='My flower-topped masterpiece')
 pie.add_layer(0,258,60,.48);pie.add_layer(-5,204,57,.51);pie.add_layer(0,140,53,.46)
 for k,x,y,li in [('petals',-.65,.3,0),('petals',.65,.3,0),('petals',-.55,.3,1),('petals',.55,.3,1),('petals',-.55,.2,2),('petals',.55,.2,2),('petals',0,.1,2),('leaves',-.7,.65,0),('leaves',.7,.65,0),('berries',-.3,.54,1),('berries',.3,.54,1),('sticks',-.9,.45,0),('pebbles',.9,.5,0)]:pie.add_deco(k,li,x,y)
 return pie

def craft():
 a=Draw('table');a.heading('Your workbench · First Squish','Tiny paws. Serious masterpieces.  •  No time limit')
 a.button(1059,17,201,56,'SUBMIT PIE',True)
 a.box(20,105,263,587);a.text('YOUR TOOLS',40,115,21,DARK,True)
 for i,t in enumerate(('Scoop / Mix','Shape / Flatten','Stack','Decorate')):a.button(35,145+47*i,233,41,f'{i+1}. {t}',active=i==3,small=True)
 a.text('INGREDIENTS',40,351,20,DARK,True)
 for i,k in enumerate(('mud','leaves','petals','pebbles','sticks','berries')):
  x,y=35,386+i*46;a.box(x,y,233,40,(178,191,138) if k=='petals' else PAPER,10)
  ingredient(a,k,x+26,y+20,.78)
  a.text(k.title(),x+60,y+7,18,INK,k=='petals')
  if k=='mud':a.text('drag to add tier',x+135,y+10,12,(130,106,84))
 a.box(1039,107,221,579);a.text('PIE REPORT',1054,117,20,DARK,True)
 pie=player_pie(); stab=evaluate_stability(pie)
 a.text(f'{len(pie.layers)} muddy tiers',1055,159,18)
 a.text(f'{len(pie.decorations)} decorations',1055,187,18)
 a.text('Stability',1055,229,15,INK,True);a.text(str(int(stab.score)),1215,229,15)
 a.box(1055,251,180,9,(150,140,108),5,None)
 a.box(1055,251,180*stab.score/100,9,(98,133,99),5,None)
 a.text(stab.notes[-1],1055,271,13,maxwidth=180)
 a.text("TODAY'S CHALLENGE",1055,333,17,DARK,True)
 for i,g in enumerate(STORY[0].goals):
  v,ok=goal_progress(pie,g)
  a.text(('✓' if ok else '○')+' '+g.label,1054,356+i*25,12,(54,130,72) if ok else INK,maxwidth=133)
  a.text(f'{v:g}/{g.target:g}',1197,356+i*25,11,(54,130,72) if ok else INK)
 a.button(1054,431,190,34,'COLOR 1/1 (C)',small=True)
 a.button(1054,465,91,40,'UNDO',small=True)
 a.button(1152,465,92,40,'REDO',small=True)
 for y,label in ((513,'START OVER'),(563,'HELP / ?'),(611,'PAUSE / ESC')):a.button(1054,y,190,42,label,small=True)
 a.box(321,111,702,45,(228,213,173),15,(157,126,85),232,1)
 a.text('DRAG PETALS from the tray onto a tier. Right-click to remove.',339,123,17,maxwidth=660)
 pie_draw(a,pie,660,584,1.0)
 a.box(844,359,170,44,(244,222,178),2,(115,83,62),244,2)
 a.center('I DID THAT!',929,381,16,(84,65,53),True)
 a.sprite('player_cheer',926,528,190,228)
 a.box(314,647,714,58,(222,204,161),15)
 a.text('Decorate: choose color (C), mirror pairs (M), drag items. R rotates latest.',329,664,15,maxwidth=680)
 a.save('craft_layout_preview.png')

def campaign():
 a=Draw('forest');a.heading('THE FOREST FAIR · CHAPTER MAP','0/36 story contests · 0/12 commissions · 0 stars')
 a.button(1055,19,188,54,'TITLE SCREEN',small=True)
 for i,txt in enumerate(('FIRST PUDDLE','PETAL PICNIC','ROCKY RIDGE','STORM','MOONLIGHT','GOLDEN CUP')):
  x=20+i*209;a.box(x,106,198,54,(178,191,138) if i==0 else (170,167,142),13)
  a.center(str(i+1)+'. '+txt,x+99,133,13,(39,63,50) if i==0 else (119,118,107),True)
 a.box(22,176,1236,414,CREAM,19)
 a.text('CHAPTER 1: THE FIRST PUDDLE',46,190,27,DARK,True)
 a.text(CHAPTERS[0].introduction,47,234,16,maxwidth=1150)
 for i,m in enumerate(STORY[:6]):
  x=41+(i%2)*613;y=271+(i//2)*100
  a.box(x,y,587,85,(226,209,173) if i==0 else (174,167,144),14)
  a.text(f'{i+1:02d}. {m.title}',x+12,y+8,19,DARK,True,maxwidth=390)
  a.text('NEXT' if i==0 else 'LOCKED',x+490,y+10,17,(153,106,42),True)
  a.text(m.description,x+12,y+34,14,maxwidth=552)
  if i==0:a.button(x+400,y+53,165,26,'PLAY CONTEST',small=True)
 a.box(23,598,1233,108)
 a.text('WOODLAND COMMISSIONS · OPTIONAL',41,608,18,DARK,True)
 for i in range(2):a.box(41+i*608,640,582,48,(174,167,144),13)
 a.save('campaign_layout_preview.png')

def results():
 a=Draw('forest')
 user=player_pie(); bruno,daisy=[make_entry(r,1,7393) for r in make_rivals()]
 pies=[user,bruno,daisy];names=['You','Bruno','Daisy'];jud=[judge(p,'Decoration') for p in pies]
 scores=[j.total for j in jud];winner=names[max(range(3),key=lambda i:scores[i])]
 a.heading(f'And the winner is… {winner.upper()}!','First Squish · Round 1 results')
 for i,(p,name,j) in enumerate(zip(pies,names,jud)):
  x=42+i*415;win=name==winner
  a.box(x,117,385,270,(227,195,131) if win else CREAM,22,(170,119,65) if win else BORDER,246,3)
  a.sprite(('player' if name=='You' else name.lower())+('_cheer' if win else '_sad'),x+66,172,84,102)
  scale=min(.58,143/max(1,p.height))
  pie_draw(a,p,x+190,277,scale)
  a.text(name,x+22,302,24,DARK,True)
  a.text(f'{j.total:.1f} pts',x+190,304,24,DARK,True)
  if win:a.text('FOREST CHAMPION ★',x+24,345,19,(137,100,43),True)
  a.button(x+270,341,97,37,'INSPECT',active=i==0,small=True)
 ev=jud[0];a.box(42,404,777,265);a.text('You · Score breakdown',65,421,28,DARK,True)
 for i,(k,v) in enumerate(ev.features.items()):
  y=469+i*36;a.text(k,70,y,17,INK,True)
  a.box(225,y+3,435,17,(161,152,119),8,None)
  a.box(225,y+3,435*v/100,17,(99,136,91),8,None)
  a.text(f'{v:.0f} / 100',676,y,17)
 a.box(840,405,397,265)
 a.text('WHAT THE JUDGES SAID',858,422,20,DARK,True)
 for i,v in enumerate(ev.verdicts):
  y=468+i*51;a.text(f'{v.name} · {v.score:.1f}',861,y,17,INK,True)
  a.text(v.comment,861,y+22,14,(94,88,70),maxwidth=350)
 a.button(840,671,392,44,'NEXT STORY CONTEST',primary=True,small=True)
 a.button(45,672,300,42,'BACK TO TITLE',small=True)
 a.button(355,672,455,42,'CHALLENGE REPORT',small=True)
 a.save('results_layout_preview.png')

if __name__=='__main__':craft();campaign();results()
