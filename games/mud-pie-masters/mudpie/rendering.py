"""Pygame graphics and reusable interface elements.

The game uses original build-time rasterized illustration assets; pygame-ce is
its only required runtime graphics dependency.
"""
from __future__ import annotations
from math import cos, radians, sin
from pathlib import Path
import pygame
from .models import Pie, Decoration

ASSETS = Path(__file__).resolve().parents[1] / "assets"
INK = (40, 54, 48)
DARK = (47, 76, 66)
CREAM = (236, 224, 189)
PAPER = (216, 197, 155)
GOLD = (209, 173, 103)
PINK = (199, 137, 120)
MUD = (91, 61, 49)


class Painter:
    def __init__(self):
        self.images = {p.stem: pygame.image.load(str(p)).convert_alpha() for p in ASSETS.glob('*.png')}
        self.fonts = {}

    def font(self, size: int, bold: bool = False):
        key = (size, bold)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont('georgia' if bold and size >= 24 else 'consolas', size, bold=bold)
        return self.fonts[key]

    def text(self, surf, value, pos, size=24, color=INK, bold=False, center=False, max_w=None):
        font = self.font(size, bold)
        phrase = str(value)
        if max_w:
            while phrase and font.size(phrase)[0] > max_w:
                phrase = phrase[:-2]
            if phrase != str(value):
                phrase += '…'
        label = font.render(phrase, True, color)
        rect = label.get_rect(center=pos) if center else label.get_rect(topleft=pos)
        surf.blit(label, rect)
        return rect

    def wrap(self, surf, message, x, y, max_width, size=19, color=INK, line_height=None):
        line_height = line_height or size + 7
        line = ''
        for word in str(message).split():
            candidate = (line + ' ' + word).strip()
            if self.font(size).size(candidate)[0] > max_width and line:
                self.text(surf, line, (x, y), size, color)
                y += line_height
                line = word
            else:
                line = candidate
        if line:
            self.text(surf, line, (x, y), size, color)
            y += line_height
        return y

    def rect(self, surf, rect, fill=CREAM, radius=20, border=None, width=2, alpha=255):
        """Crisp carved/inked plaques, not generic floating rounded cards.

        Existing hitboxes stay identical while painting the whole game's UI in
        the same square-edged, hand-printed pixel vocabulary as the assets.
        """
        r = pygame.Rect(rect)
        if r.width <= 0 or r.height <= 0:
            return
        rad = min(radius, 3)
        if alpha == 255:
            pygame.draw.rect(surf, fill, r, border_radius=rad)
            if border:
                pygame.draw.rect(surf, border, r, max(1,width), border_radius=rad)
            if r.width > 35 and r.height > 20:
                # Short scored corners like a carved wooden noticeboard.
                accent = border or (109, 91, 69)
                pygame.draw.line(surf, accent, (r.x+6,r.y+6), (r.x+15,r.y+6), 1)
                pygame.draw.line(surf, accent, (r.right-15,r.bottom-7), (r.right-6,r.bottom-7), 1)
        else:
            lay = pygame.Surface(r.size, pygame.SRCALPHA)
            pygame.draw.rect(lay, (*fill, alpha), lay.get_rect(), border_radius=rad)
            if border:
                pygame.draw.rect(lay, (*border, alpha), lay.get_rect(), max(1,width), border_radius=rad)
            if r.width > 35 and r.height > 20:
                accent = border or (109, 91, 69)
                pygame.draw.line(lay, (*accent,alpha), (6,6), (15,6), 1)
                pygame.draw.line(lay, (*accent,alpha), (r.width-15,r.height-7), (r.width-6,r.height-7), 1)
            surf.blit(lay, r.topleft)

    def image(self, surf, name, pos, size, center=False, bounce=0):
        if name not in self.images:
            return
        source = self.images[name]
        target = pygame.transform.scale(source, (int(size[0]), int(size[1])))
        rect = target.get_rect(center=pos) if center else target.get_rect(topleft=pos)
        rect.move_ip(0, int(bounce))
        surf.blit(target, rect)
        return rect


def _ellipse(surf, color, bounds, width=0):
    r = pygame.Rect(int(bounds[0]), int(bounds[1]), max(1, int(bounds[2])), max(1, int(bounds[3])))
    pygame.draw.ellipse(surf, color, r, width)


def decoration_anchor(pie: Pie, d: Decoration, base_x: float, base_y: float, scale: float):
    h = sum(l.height for l in pie.layers[:d.layer + 1] if not l.fallen)
    layer = pie.layers[d.layer]
    x = base_x + scale * (layer.x + d.x * layer.width * .44)
    y = base_y - scale * h + scale * layer.height * d.y * .77
    return (x, y)


def draw_ingredient(surf, kind: str, x: float, y: float, scale: float = 1,
                    angle: float = 0, color_variant: int = 0):
    x, y = int(x), int(y)
    radius = max(2, int(10 * scale))
    rad = radians(angle)
    if kind == 'mud':
        _ellipse(surf, (86, 55, 35), (x-17*scale, y-9*scale, 34*scale, 19*scale))
        _ellipse(surf, (143, 91, 56), (x-15*scale, y-10*scale, 30*scale, 14*scale))
        _ellipse(surf, (196, 134, 89), (x-9*scale, y-6*scale, 9*scale, 3*scale))
    elif kind == 'leaves':
        c = [(70, 121, 68), (101, 150, 81), (137, 160, 89),
             (62, 127, 114), (172, 147, 75), (94, 107, 157)][color_variant % 6]
        pts = [(x+cos(rad)*25*scale, y+sin(rad)*25*scale),
               (x+cos(rad+1.15)*14*scale, y+sin(rad+1.15)*14*scale),
               (x-cos(rad)*20*scale, y-sin(rad)*20*scale),
               (x+cos(rad-1.15)*14*scale, y+sin(rad-1.15)*14*scale)]
        pygame.draw.polygon(surf, c, pts)
        pygame.draw.line(surf, (216, 223, 154), pts[0], pts[2], max(1, int(scale*2)))
    elif kind == 'petals':
        cols = [(235, 152, 169), (250, 215, 151), (220, 194, 224),
                (250, 234, 214), (167, 215, 235), (239, 134, 94)]
        for a in range(0, 360, 72):
            rr = radians(a + angle)
            cx = x + cos(rr)*radius*.9
            cy = y + sin(rr)*radius*.9
            _ellipse(surf, cols[color_variant % 6], (cx-radius*.66,cy-radius*.66,radius*1.32,radius*1.32))
        pygame.draw.circle(surf, (250, 209, 113), (x,y), max(2, int(4*scale)))
    elif kind == 'pebbles':
        rock_palette = [(160,171,160),(186,164,140),(148,165,182),
                        (180,147,166),(146,178,150),(213,186,134)]
        stone=rock_palette[color_variant%6]
        _ellipse(surf, (98, 105, 105), (x-11*scale,y-7*scale,24*scale,18*scale))
        _ellipse(surf, stone, (x-11*scale,y-9*scale,22*scale,15*scale))
        _ellipse(surf, (217, 223, 211), (x-7*scale,y-7*scale,7*scale,3*scale))
    elif kind == 'sticks':
        ex, ey = cos(rad) * 21*scale, sin(rad) * 21*scale
        pygame.draw.line(surf, (84, 53, 39), (x-ex,y-ey), (x+ex,y+ey), max(3, int(scale*8)))
        bark=[(178,128,83),(125,117,90),(199,149,101),(137,103,130),
              (159,159,116),(100,138,139)][color_variant%6]
        pygame.draw.line(surf, bark, (x-ex,y-ey-2*scale), (x+ex,y+ey-2*scale), max(1,int(scale*3)))
    elif kind == 'berries':
        berry_palette=[((97,43,77),(180,72,103)),((88,87,130),(147,139,204)),
                       ((154,76,52),(225,132,82)),((76,122,79),(140,191,103)),
                       ((159,75,119),(229,142,173)),((107,88,43),(204,169,86))]
        dark, light=berry_palette[color_variant%6]
        for dx, dy in ((-8,2),(6,3),(0,-6)):
            pygame.draw.circle(surf, dark, (int(x+dx*scale),int(y+dy*scale)), max(2,int(8*scale)))
            pygame.draw.circle(surf, light, (int(x+dx*scale),int(y+dy*scale)), max(2,int(6*scale)))
            pygame.draw.circle(surf, (245, 168, 179), (int(x+(dx-2)*scale),int(y+(dy-3)*scale)), max(1,int(2*scale)))


def _rough_outline(w, h, phase):
    """Organic crumbling top edge, stable across frames and frame rates."""
    count = max(7, int(w // 13))
    upper=[]
    for k in range(count+1):
        xx=w*k/count
        jitter=((k*7+phase*13)%9-4)*min(1.0,h/35)
        upper.append((xx, jitter))
    return upper


def draw_pie(surf, pie: Pie, base_x: float, base_y: float, scale: float = 1.0,
             wobble: float = 0.0, show_structure: bool = False,
             hidden_fallen: set[int] | None = None,
             draw_shadow: bool = True):
    """Irregular earth-sculpted tiers with stratified texture; no cake cylinders.

    Geometry, centering and tier order are unchanged from the simulation so
    hit-testing and judging still refer to the same constructed pie model.
    """
    if not pie.layers:
        return
    base_x,base_y=int(base_x),int(base_y)
    if draw_shadow:
        _ellipse(surf,(61,49,42),(base_x-140*scale,base_y-14*scale,280*scale,29*scale))
        _ellipse(surf,(157,121,81),(base_x-131*scale,base_y-12*scale,262*scale,19*scale))
    upward=0
    for i,layer in enumerate(pie.layers):
        if layer.fallen:
            if hidden_fallen and i in hidden_fallen:
                # A real falling animation is passing through the air.
                # Do not also draw its landed debris before contact.
                continue
            fx=base_x+layer.x*scale+((i%2)*70-35)*scale
            fy=base_y+(i%3*7)*scale
            pts=[(fx-51*scale,fy),(fx-38*scale,fy-16*scale),
                 (fx+17*scale,fy-19*scale),(fx+53*scale,fy-3*scale),
                 (fx+41*scale,fy+9*scale),(fx-46*scale,fy+8*scale)]
            pygame.draw.polygon(surf,(73,48,39),pts)
            for j in range(9):
                px=fx+((j*19)%71-38)*scale
                py=fy-((j*11)%13)*scale
                pygame.draw.rect(surf,(151,104,69),(int(px),int(py),max(1,int(5*scale)),max(1,int(3*scale))))
            continue
        w,h=layer.width*scale,layer.height*scale
        upward+=h
        x=base_x+layer.x*scale-w/2+wobble*(i+1)/max(1,len(pie.layers))
        top=base_y-upward
        outline=_rough_outline(w,h,i+int(layer.width*.1))
        bump=min(8*scale,h*.23)
        # Sediment is hand-packed: silhouette is ragged and asymmetric.
        upper=[(int(x+xx),int(top+yy)) for xx,yy in outline]
        left=[(int(x+5*scale),int(top+h*.4)),(int(x-3*scale),int(top+h*.77))]
        right=[(int(x+w+3*scale),int(top+h*.82)),(int(x+w-5*scale),int(top+h*.35))]
        side=upper+right+[(int(x+w*.91),int(top+h)),(int(x+w*.17),int(top+h+3*scale))]+left
        pygame.draw.polygon(surf,(62,46,39),side)
        wall=(104,68,50) if layer.wetness<.75 else (83,57,46)
        pygame.draw.polygon(surf,wall,
            [(int(x+4*scale),int(top+9*scale)),(int(x+w-5*scale),int(top+10*scale)),
             (int(x+w-9*scale),int(top+h-5*scale)),(int(x+8*scale),int(top+h-6*scale))])
        # Three uneven soil strata show the object's volume and moisture.
        for j in range(3):
            yy=top+(h*.3+j*h*.16)
            pygame.draw.lines(surf,(76,51,41),False,
                [(int(x+11*scale),int(yy+2*scale)),(int(x+w*.35),int(yy-3*scale)),
                 (int(x+w*.7),int(yy+2*scale)),(int(x+w-8*scale),int(yy-2*scale))],
                max(1,int(2*scale)))
        # Top is an uneven flat-packed surface rather than a precise ellipse.
        top_points=upper+[(int(x+w-7*scale),int(top+13*scale)),
                          (int(x+w*.66),int(top+17*scale)),
                          (int(x+w*.27),int(top+15*scale)),
                          (int(x+6*scale),int(top+11*scale))]
        pygame.draw.polygon(surf,(158,110,72),top_points)
        pygame.draw.lines(surf,(190,143,91),False,upper[2:-2],max(1,int(2*scale)))
        # Purposeful grit in the wet clay: same pattern every frame.
        for k in range(28):
            u=((k*47+i*31)%101)/101
            v=((k*17+i*13)%89)/89
            px=x+11*scale+(w-22*scale)*u
            py=top+15*scale+(h-27*scale)*v
            c=((161,115,78) if k%4 else (55,43,35))
            size=max(1,int((2+k%3)*scale))
            pygame.draw.rect(surf,c,(int(px),int(py),size,max(1,size//2)))
        if layer.shape=='craggy':
            for j in range(4):
                px=x+w*(j+1)/5
                pygame.draw.polygon(surf,(74,49,40),[(px,top+7*scale),
                    (px+10*scale,top+14*scale),(px+4*scale,top+20*scale)])
        if show_structure:
            pygame.draw.rect(surf,(222,193,121),(int(x),int(top),int(w),int(h)),1)
    for d in pie.decorations:
        if pie.layers[d.layer].fallen:
            if hidden_fallen and d.layer in hidden_fallen:
                continue
            # Fallen decorations remain visible as scattered keepsakes on the
            # tabletop instead of silently vanishing with the collapsed tier.
            layer=pie.layers[d.layer]
            px=base_x+(layer.x+d.x*layer.width*.34)*scale
            py=base_y-(9+d.y*12)*scale
        else:
            px,py=decoration_anchor(pie,d,base_x,base_y,scale)
        draw_ingredient(surf,d.kind,px,py,scale*min(1.15,max(.6,scale**-.15)),d.angle,d.color)
    for i,layer in enumerate(pie.layers):
        if not layer.fallen and layer.damage>.3:
            h=sum(l.height for l in pie.layers[:i+1] if not l.fallen)
            x=base_x+layer.x*scale
            y=base_y-h*scale+layer.height*.48*scale
            pygame.draw.lines(surf,(42,35,30),False,[(x,y-11*scale),(x+7*scale,y),(x-2*scale,y+13*scale)],max(1,int(3*scale)))
