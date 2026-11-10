"""Mud Pie Masters -- complete single-player Pygame competition loop."""
from __future__ import annotations
import math
from typing import Callable

import pygame

from .judging import FEATURES, JUDGES, THEMES, effective_weights, fingerprint, judge
from .campaign import (CHAPTERS, CHALLENGES, SIDES, STORY, BY_ID, available_side,
                       available_story, campaign_statistics, goal_progress, medals_for,
                       record_result, unlocked_colors, normalized_campaign)
from .models import DECORATIONS, INGREDIENTS, SHAPES, TOOLS, Pie, clamp, collapse_if_needed, evaluate_stability
from .rendering import ASSETS, CREAM, DARK, INK, PAPER, Painter, decoration_anchor, draw_ingredient, draw_pie
from .rivals import make_entry, update_relationships, respond_to_player
from .save import default_path, load_game, save_game

W, H = 1280, 720
TABLE_X, TABLE_Y = 660, 584
WORKSPACE = pygame.Rect(315, 153, 721, 486)


class Game:
    def __init__(self, display: pygame.Surface):
        self.display = display
        self.canvas = pygame.Surface((W, H)).convert()
        self.paint = Painter()
        data = load_game()
        self.round_no = data['round']
        self.rivals = data['rivals']
        self.gallery = data['gallery']
        self.history = data['history']
        self.settings = data['settings']
        self.campaign = normalized_campaign(data.get('campaign'))
        self.mission = None
        self.mode = 'story'
        self.chapter_view = min(5, self.campaign['next_story'] // 6)
        self.color_variant = 0
        self.mirror_mode = False
        self.mission_medals = 0
        self.mission_checks = []
        self.gallery_page = 0
        self.last_play_seconds = 0.0
        self.fullscreen = False
        self.scene = 'title'
        self.overlay = None
        self.timer = 0.0
        self.toast = ''
        self.toast_time = 0.0
        self.buttons: list[tuple[pygame.Rect, Callable]] = []
        self.mouse = (0, 0)
        self.running = True
        self.pie = Pie()
        self.tool = 0
        self.selected = 'petals'
        self.drag = None
        self.undos: list[dict] = []
        self.redos: list[dict] = []
        self.presentation_step = 0
        self.presentation_since = 0.0
        self.collapse_sound_played = False
        self.inspected = 0
        self.finished = False
        self.theme = THEMES[0]
        self.rival_pies = []
        self.sibling_actions = set()
        self.mud_flecks = []
        self.last_fleck_time = -1.0
        self.sound = {}
        self.sound_enabled = False
        self.music_enabled = False
        self._init_audio()

    def _init_audio(self):
        try:
            if pygame.mixer.get_init():
                self.sound = {p.stem: pygame.mixer.Sound(str(p))
                              for p in ASSETS.glob('*.wav') if p.stem != 'music'}
                self.sound_enabled = True
                music = ASSETS / 'music.wav'
                if music.exists():
                    pygame.mixer.music.load(str(music))
                    pygame.mixer.music.set_volume(self.settings['music_volume'])
                    pygame.mixer.music.play(-1)
                    self.music_enabled = True
                    if not self.settings['music']:
                        pygame.mixer.music.pause()
        except pygame.error:
            self.sound_enabled = False

    def sfx(self, name: str):
        if self.settings.get('sound') and self.sound_enabled and name in self.sound:
            self.sound[name].set_volume(self.settings['sound_volume'])
            self.sound[name].play()

    def save(self):
        try:
            save_game(self.round_no, self.rivals, self.gallery, self.history, self.settings, campaign=self.campaign)
        except OSError as exc:
            self.notify(f'Could not save: {exc}')

    def notify(self, message: str, seconds=3.4):
        self.toast = message
        self.toast_time = seconds

    def begin_round(self, mission_id=None):
        """Start the next unlocked story contest, a replay, or a commission."""
        mission = BY_ID.get(mission_id) if mission_id else available_story(self.campaign)
        if mission is None:
            self.scene = 'campaign'
            self.notify('The whole story is complete. Replay or take a commission!')
            return
        if mission.side and not available_side(self.campaign, mission):
            self.notify('That woodland client has not arrived yet.')
            return
        if not mission.side and STORY.index(mission) > self.campaign['next_story']:
            self.notify('Finish the preceding contests first!')
            return
        self.mission = mission
        self.mode = 'side' if mission.side else 'story'
        self._prepare_competition()
        if mission.chapter not in self.campaign['seen_chapters']:
            self.show_overlay('chapter')

    def _prepare_competition(self):
        self.scene = 'clearing'
        self.finished = False
        self.pie = Pie(title=f'My masterpiece #{self.round_no}')
        self.drag = None
        self.tool = 0
        self.color_variant = min(self.color_variant, unlocked_colors(self.campaign) - 1)
        self.mirror_mode = False
        if self.mission and self.selected not in (self.mission.allowed or INGREDIENTS):
            self.selected = next((k for k in DECORATIONS if k in self.mission.allowed), 'mud')
        self.undos.clear()
        self.redos.clear()
        if self.mission:
            m = self.mission
            self.theme = (m.title, m.description, m.focus)
        else:
            self.theme = THEMES[(self.round_no - 1) % len(THEMES)]
        self.round_started_at = self.timer
        try:
            previous = Pie.from_dict(self.gallery[-1]['pie']) if self.gallery else None
        except (ValueError, TypeError, KeyError):
            previous = None
        allowed = self.mission.allowed if self.mission else ()
        weather = self.mission.weather if self.mission else 'clear'
        self.rival_pies = [make_entry(r, self.round_no, 7393, previous,
                                      allowed=allowed, weather=weather) for r in self.rivals]
        self.presentation_step = 0
        self.inspected = 0
        self.sibling_actions = set()

    def interact_sibling(self, name: str, action: str) -> None:
        if name in self.sibling_actions:
            self.notify(f'You already spoke to {name} before this contest.')
            return
        rival = next((r for r in self.rivals if r.name == name), None)
        if rival is None or self.scene != 'clearing':
            return
        self.sibling_actions.add(name)
        self.notify(respond_to_player(rival, action), seconds=5.0)
        try:
            previous = Pie.from_dict(self.gallery[-1]['pie']) if self.gallery else None
        except (ValueError, TypeError, KeyError):
            previous = None
        index = 0 if name == 'Bruno' else 1
        self.rival_pies[index] = make_entry(
            rival, self.round_no, 7393, previous,
            allowed=self.mission.allowed if self.mission else (),
            weather=self.mission.weather if self.mission else 'clear')
        self.sfx('pop')

    def start_free_build(self):
        """A genuinely judgment-free construction session that can be saved."""
        self.mode = 'free'
        self.mission = None
        self.theme = ('Creative Meadow', 'No goals, no points, just glorious mud.', 'Originality')
        self.pie = Pie(title='My free-build mud creation')
        self.undos.clear()
        self.redos.clear()
        self.tool = 0
        self.color_variant = 0
        self.mirror_mode = False
        self.drag = None
        self.scene = 'craft'
        self.finished = False
        if not self.settings.get('tutorial_seen', False):
            self.settings['tutorial_seen'] = True
            self.save()
            self.show_overlay('tutorial')

    def allowed_ingredient(self, kind):
        return not self.mission or not self.mission.allowed or kind in self.mission.allowed

    def cycle_color(self):
        count = unlocked_colors(self.campaign)
        self.color_variant = (self.color_variant + 1) % count
        self.notify(f'Decoration color {self.color_variant + 1} of {count}. Six colors are available by Chapter 5!')

    def toggle_mirror(self):
        if self.campaign['next_story'] < 6:
            self.notify('Complete Chapter 1 to learn the twin-decoration trick!')
            return
        self.mirror_mode = not self.mirror_mode
        self.notify('Twin decoration mode: '+('ON' if self.mirror_mode else 'OFF'))

    def dry_layer(self):
        if self.campaign['next_story'] < 18:
            self.notify('The gentle drying technique unlocks in Storm Season.')
            return
        index = self._layer_at(self.mouse)
        if index is None:
            self.notify('Point to a mud tier, then press D to dry it.')
            return
        self.snapshot()
        layer = self.pie.layers[index]
        layer.wetness = max(.28, round(layer.wetness - .13, 3))
        self.notify('A careful pat of dry leaves firms up this tier.')
        self.sfx('squish')

    def place_decoration(self, kind, tier, x, y):
        """Craft one decoration, or two actual matching mirrored objects."""
        self.pie.add_deco(kind, tier, x, y, color=self.color_variant)
        if self.mirror_mode and self.campaign['next_story'] >= 6 and abs(x) >= .18                 and len(self.pie.decorations) < 120:
            self.pie.add_deco(kind, tier, -x, y, color=self.color_variant)

    def choose_chapter(self, encouragement: bool):
        chapter = self.mission.chapter
        if chapter not in self.campaign['seen_chapters']:
            self.campaign['seen_chapters'].append(chapter)
            self.campaign['choices'][str(chapter)] = 'encourage' if encouragement else 'challenge'
            if encouragement:
                for rival in self.rivals:
                    rival.affection = min(100, rival.affection + 4)
                    rival.remember('You encouraged us before a big chapter.')
                self.notify('Both cubs beam. They will remember your kindness.')
            else:
                for rival in self.rivals:
                    rival.affection = max(5, rival.affection - 2)
                    rival.remember('You challenged us to build something better.')
                self.notify('Bruno grins at your challenge; Daisy looks determined.')
            self.save()
        self.close_overlay()

    def start_crafting(self):
        self.scene = 'craft'
        if not self.settings.get('tutorial_seen',False):
            self.settings['tutorial_seen'] = True
            self.save()
            self.show_overlay('tutorial')

    def snapshot(self):
        self.undos.append(self.pie.to_dict())
        self.undos = self.undos[-60:]
        self.redos.clear()

    def undo(self):
        if not self.undos:
            self.notify('Nothing left to undo.')
            return
        self.redos.append(self.pie.to_dict())
        self.pie = Pie.from_dict(self.undos.pop())
        self.sfx('pop')

    def redo(self):
        if not self.redos:
            self.notify('Nothing left to redo.')
            return
        self.undos.append(self.pie.to_dict())
        self.pie = Pie.from_dict(self.redos.pop())
        self.sfx('pop')

    def submit(self):
        if self.mode == 'free':
            if not self.pie.layers:
                self.notify('Make at least one mud tier before saving!')
                return
            self.gallery_page = 0
            self.gallery.append({'round': self.round_no, 'theme': 'Creative Meadow · Free Build',
                                 'pie': self.pie.to_dict(), 'signature': fingerprint(self.pie),
                                 'score': 0, 'free': True})
            self.gallery = self.gallery[-60:]
            self.save()
            self.scene = 'gallery'
            self.sfx('fanfare')
            self.notify('Your free-build creation is safely in the scrapbook!')
            return
        if not self.pie.layers:
            self.notify('Scoop at least one muddy layer first!')
            return
        self.entries = [self.pie.copy(), *[pie.copy() for pie in self.rival_pies]]
        self.names = ['You', 'Bruno', 'Daisy']
        self.display_entries = []
        self.collapsed = {}
        self.judgments = []
        for idx, entry in enumerate(self.entries):
            visual, fall = collapse_if_needed(entry, weather=self.mission.weather if self.mission else 'clear')
            self.display_entries.append(visual)
            self.collapsed[self.names[idx]] = fall
            recent = [h.get('signatures', {}).get(self.names[idx], '') for h in self.history]
            # Old saves predate the per-competitor signature history.
            if idx == 0 and not any(recent):
                recent = [item.get('signature', '') for item in self.gallery]
            self.judgments.append(judge(entry, self.theme[2], recent, weather=self.mission.weather if self.mission else 'clear'))
        self.scene = 'presentation'
        self.presentation_step = 0
        self.presentation_since = self.timer
        self.collapse_sound_played = False
        self.sfx('fanfare')

    def finish_round(self):
        if self.finished:
            self.scene = 'results'
            return
        scores = {name: evaluation.total for name, evaluation in zip(self.names, self.judgments)}
        events = update_relationships(self.rivals, scores, self.collapsed, self.round_no)
        winner = max(scores, key=scores.get)
        self.last_winner = winner
        self.events = events
        self.mission_medals = 0
        self.mission_checks = []
        if self.mission:
            self.mission_medals, self.mission_checks = medals_for(
                self.mission, self.pie, self.judgments[0].total)
            previous_story_progress = self.campaign['next_story']
            self.campaign = record_result(self.campaign, self.mission, self.mission_medals)
            # Zero is divisible by six, but is NOT a chapter completion.
            if (not self.mission.side and
                    self.campaign['next_story'] > previous_story_progress and
                    self.campaign['next_story'] % 6 == 0):
                if self.campaign['next_story'] <= 24:
                    self.notify('Chapter complete! A new decoration color is unlocked.')
                else:
                    self.notify('Chapter complete! A new keepsake is waiting in the gallery.')
            self.chapter_view = min(5, self.campaign['next_story'] // 6)
        self.gallery_page = 0
        self.gallery.append({'round': self.round_no, 'theme': self.theme[0],
                             'pie': self.pie.to_dict(), 'signature': fingerprint(self.pie),
                             'score': self.judgments[0].total, 'mission': self.mission.id if self.mission else None,
                             'medals': self.mission_medals})
        self.gallery = self.gallery[-60:]
        self.history.append({'round': self.round_no, 'theme': self.theme[0],
                             'scores': scores, 'winner': winner, 'events': events,
                             'mission': self.mission.id if self.mission else None,
                             'medals': self.mission_medals,
                             'signatures': {name: fingerprint(pie)
                                            for name, pie in zip(self.names,self.entries)}})
        self.history = self.history[-100:]
        self.round_no += 1
        self.save()
        self.finished = True
        self.scene = 'results'
        self.sfx('fanfare' if winner == 'You' else 'pop')

    def button(self, rect, text, callback, primary=False, small=False, active=False, disabled=False):
        """Forest-fair printed placards; hitboxes remain exactly unchanged."""
        rect = pygame.Rect(rect)
        hovered = rect.collidepoint(self.mouse) and not disabled
        fill = (198, 154, 93) if primary else ((178, 191, 138) if active else PAPER)
        if hovered:
            fill = (220, 179, 109) if primary else (230, 216, 176)
        if disabled:
            fill = (157, 157, 131)
        # Slight offset ink/wood shadow so actions read as pressed objects.
        pygame.draw.rect(self.canvas, (47, 52, 42), rect.move(2,3), border_radius=2)
        self.paint.rect(self.canvas, rect, fill, 2, (75, 59, 48), 2)
        if not disabled:
            pygame.draw.line(self.canvas, (242, 225, 175),
                             (rect.left+5,rect.top+3), (rect.right-6,rect.top+3),1)
        if active:
            pygame.draw.rect(self.canvas, (45, 88, 61),
                             (rect.x+4, rect.y+5, 5, max(3, rect.h-10)))
        self.paint.text(self.canvas, text, rect.center, 16 if small else 20,
                        (96, 91, 78) if disabled else INK,
                        bold=True, center=True, max_w=rect.width-16)
        if not disabled and self.overlay is None:
            self.buttons.append((rect, callback))

    def _heading(self, title, subtitle=None):
        self.paint.rect(self.canvas, (0, 0, 1280, 94), (31, 52, 46), 0, alpha=251)
        pygame.draw.line(self.canvas, (176, 145, 90), (0,93), (1280,93), 3)
        self.paint.text(self.canvas, title, (38, 15), 35, CREAM, bold=True, max_w=990)
        if subtitle:
            self.paint.text(self.canvas, subtitle, (41, 63), 16, (212, 198, 160), max_w=1180)

    def _sprite(self, name, center, size, bounce=True, expression=None):
        """Draw a real expression sprite for cubs; preserve existing judge assets.

        Expressions share the same bounding box, so hitboxes, letterboxing and
        composition stay stable. Reduced-motion also disables idle blinking.
        """
        key = 'player' if name.lower() == 'you' else name.lower()
        if key in ('player', 'bruno', 'daisy'):
            if expression is None:
                phase = (self.timer + {'player': .8, 'bruno': 2.1, 'daisy': 3.2}[key]) % 5.3
                expression = 'blink' if phase < .16 and not self.settings['reduced_motion'] else 'idle'
            variant = key if expression == 'idle' else f'{key}_{expression}'
            if variant in self.paint.images:
                key = variant
        bob = (-3 * math.sin(self.timer * 2.4 + sum(map(ord,name)))
               if bounce and not self.settings['reduced_motion'] else 0)
        return self.paint.image(self.canvas, key, center, size, center=True, bounce=bob)

    def _stat_bar(self, name, amount, x, y, width=190, size=15):
        value = clamp(amount, 0, 100)
        self.paint.text(self.canvas, name, (x,y), size, INK, bold=True)
        self.paint.text(self.canvas, str(round(value)), (x+width-22,y), size, INK)
        self.paint.rect(self.canvas,(x,y+22,width,9),(205,200,177),5)
        color = (92,148,103) if value>=60 else (214,157,89) if value>=30 else (199,108,90)
        self.paint.rect(self.canvas,(x,y+22,int(width*value/100),9),color,5)

    def draw_ambience(self):
        """Lightweight procedural atmosphere, distinct from competition rules."""
        weather = self.mission.weather if self.mission else 'clear'
        tick = 0 if self.settings['reduced_motion'] else self.timer
        if weather == 'night':
            tint=pygame.Surface((W,H),pygame.SRCALPHA)
            tint.fill((29,35,75,64))
            self.canvas.blit(tint,(0,0))
            for i in range(42):
                x=(i*193+71)%W
                y=(i*89+17)%490
                r=1+(i%4==0)
                pygame.draw.circle(self.canvas,(254,230,156),(x,y),r)
        elif weather == 'rain':
            for i in range(59):
                x=int((i*127 + tick*68) % W)
                y=int((i*211 + tick*268) % H)
                pygame.draw.line(self.canvas,(176,212,229),(x,y),(x-9,y+19),2)
        elif weather == 'wind':
            for i in range(22):
                x=int((i*179 + tick*76) % W)
                y=int((i*83 + 27) % 590)
                pygame.draw.arc(self.canvas,(221,231,197),
                                (x,y,46,12),.2,3.0,1)

    def draw_title(self):
        self.canvas.blit(self.paint.images['forest'], (0, 0))
        self.paint.rect(self.canvas,(44,72,745,579),CREAM,30,(103,88,64),3,alpha=244)
        self.paint.text(self.canvas,'MUD PIE',(92,101),78,DARK,bold=True)
        self.paint.text(self.canvas,'MASTERS',(92,184),78,DARK,bold=True)
        self.paint.text(self.canvas,'A very serious contest about dirt.',(96,292),24,INK,bold=True)
        stats = campaign_statistics(self.campaign)
        self.paint.wrap(self.canvas,'36 story contests, 12 woodland commissions, six chapters, and two very competitive siblings.',96,330,585,19)
        self.paint.text(self.canvas,f"Story {stats['story_done']}/36  ·  Commissions {stats['side_done']}/12  ·  {stats['stars']} stars",(96,409),19,DARK,bold=True)
        self.button((96,451,332,57),'CONTINUE THE STORY',
                    self.begin_round if available_story(self.campaign) else lambda:setattr(self,'scene','epilogue'),primary=True)
        self.button((443,451,284,57),'CHAPTER MAP',lambda:setattr(self,'scene','campaign'))
        self.button((96,521,332,54),'FREE-BUILD MEADOW',self.start_free_build)
        self.button((443,521,284,54),'MY SCRAPBOOK',lambda:setattr(self,'scene','gallery'))
        self.button((96,593,235,42),'SETTINGS',lambda:self.show_overlay('settings'),small=True)
        self.paint.text(self.canvas,f"Round {self.round_no} · {int(self.campaign['seconds']//60)} min in game",(348,605),16,INK)
        self._sprite('player',(956,400),(330,396))
        self._sprite('daisy',(1127,517),(190,226))
        self._sprite('bruno',(844,538),(170,206))
        self.paint.rect(self.canvas,(837,77,361,53),PAPER,19,(126,99,73))
        self.paint.text(self.canvas,'No eating the entries, cubs!',(852,94),18,INK,bold=True)

    def draw_campaign(self):
        self.canvas.blit(self.paint.images['forest'],(0,0))
        stats=campaign_statistics(self.campaign)
        self._heading('THE FOREST FAIR · CHAPTER MAP',
                      f"{stats['story_done']}/36 story contests · {stats['side_done']}/12 commissions · {stats['stars']} stars")
        self.button((1055,19,188,54),'TITLE SCREEN',lambda:setattr(self,'scene','title'),small=True)
        max_chapter=min(5,self.campaign['next_story']//6)
        for i,c in enumerate(CHAPTERS):
            unlocked=i<=max_chapter
            self.button((20+i*209,106,198,54),f'{i+1}. '+('FIRST PUDDLE','PETAL PICNIC','ROCKY RIDGE','STORM','MOONLIGHT','GOLDEN CUP')[i],
                        lambda ch=i:setattr(self,'chapter_view',ch),small=True,
                        active=self.chapter_view==i,disabled=not unlocked)
        chapter=self.chapter_view
        current=CHAPTERS[chapter]
        self.paint.rect(self.canvas,(22,176,1236,414),CREAM,19,(113,91,65),2,alpha=247)
        self.paint.text(self.canvas,f'CHAPTER {chapter+1}: {current.name}',(46,190),27,DARK,bold=True)
        self.paint.text(self.canvas,current.introduction,(47,231),16,INK,max_w=1150)
        if chapter in self.campaign['chapter_rewards']:
            self.paint.text(self.canvas,'KEEPSAKE EARNED: '+current.keepsake,(47,251),13,(127,91,50),bold=True)
        rows=STORY[chapter*6:chapter*6+6]
        for i,m in enumerate(rows):
            x=41+(i%2)*613
            y=271+(i//2)*100
            index=chapter*6+i
            unlocked=index<=self.campaign['next_story']
            medal=self.campaign['story_medals'].get(m.id,0)
            fill=(249,241,218) if unlocked else (211,207,193)
            self.paint.rect(self.canvas,(x,y,587,85),fill,14,(125,104,78),2)
            mark=(f'{medal} STAR' + ('S' if medal != 1 else '')) if medal else ('NEXT' if unlocked else 'LOCKED')
            self.paint.text(self.canvas,f'{index+1:02d}. {m.title}',(x+12,y+7),19,DARK,bold=True,max_w=390)
            self.paint.text(self.canvas,mark,(x+490,y+10),17,(153,106,42),bold=True)
            self.paint.text(self.canvas,m.description,(x+12,y+34),14,INK,max_w=552)
            if unlocked:
                self.button((x+400,y+53,165,26),'REPLAY' if medal>=2 else 'RETRY GOALS' if medal else 'PLAY CONTEST',
                            lambda mid=m.id:self.begin_round(mid),small=True)
        self.paint.rect(self.canvas,(23,598,1233,108),CREAM,16,(113,91,65),2,alpha=245)
        self.paint.text(self.canvas,'WOODLAND COMMISSIONS · OPTIONAL', (41,607),18,DARK,bold=True)
        for i,m in enumerate(SIDES[chapter*2:chapter*2+2]):
            medal=self.campaign['side_medals'].get(m.id,0)
            self.button((41+i*608,640,582,48),
                        f"{str(medal) + ' STARS' if medal else 'NEW'}  {m.title}",
                        lambda mid=m.id:self.begin_round(mid),small=True,
                        disabled=not available_side(self.campaign,m))

    def draw_clearing(self):
        self.canvas.blit(self.paint.images['forest'], (0,0))
        self.draw_ambience()
        self._heading(f"Round {self.round_no} · {self.theme[0]}", self.theme[1])
        for i,(name,title,weights) in enumerate(JUDGES):
            x = 30 + i*411
            self.paint.rect(self.canvas,(x,108,397,119),CREAM,19,(99,91,68),2,alpha=239)
            self._sprite(name,(x+70,170),(99,118),False)
            self.paint.text(self.canvas,name,(x+132,117),25,DARK,bold=True)
            self.paint.text(self.canvas,title,(x+132,151),18,INK)
            focus = FEATURES[weights.index(max(weights))]
            self.paint.text(self.canvas,f'Most loves: {focus}',(x+132,177),17,(115,96,55),bold=True)
            top=sorted(effective_weights(weights,self.theme[2]).items(), key=lambda pair:pair[1],reverse=True)[:2]
            self.paint.text(self.canvas,f'{top[0][0]} {top[0][1]:.0%} · {top[1][0]} {top[1][1]:.0%}',
                            (x+132,205),13,(88,100,73),max_w=245)
        if self.mission:
            goals = '   |   '.join(g.label for g in self.mission.goals)
            self.paint.rect(self.canvas,(40,230,1198,28),PAPER,10,(137,112,84),1,alpha=241)
            self.paint.text(self.canvas,'YOUR COMMISSION: '+goals,(58,236),15,DARK,bold=True,max_w=1160)
        for idx,(name,pos) in enumerate((('Bruno',235),('player',637),('Daisy',1032))):
            self.paint.rect(self.canvas,(pos-166,258,327,353),(255,245,217),24,(91,77,56),2,alpha=219)
            if idx!=1:
                elapsed=max(0,self.timer-self.round_started_at)
                rival=self.rival_pies[0 if idx==0 else 1]
                visible=min(len(rival.layers),1+int(elapsed/2.4))
                partial=Pie(layers=[l for l in rival.layers[:visible]],
                            decorations=[d for d in rival.decorations if d.layer<visible and elapsed>6])
                draw_pie(self.canvas,partial,pos+83,480,.28)
                self._sprite(name,(pos-43,407),(161,193))
            else:
                self._sprite(name,(pos,400),(210,250))
            label = 'YOU' if idx == 1 else name.upper()
            self.paint.text(self.canvas,label,(pos,516),27,DARK,bold=True,center=True)
            subtitle = ['Dreams of a HUGE tower','The next mud-pie legend','Loves pretty little details'][idx]
            self.paint.text(self.canvas,subtitle,(pos,550),16,INK,center=True)
            if idx != 1:
                status='Gathering ingredients…' if self.timer-self.round_started_at<2.4 else ('Stacking muddy tiers…' if self.timer-self.round_started_at<6 else 'Decorating a secret entry!')
                self.paint.text(self.canvas,status,(pos,577),15,(102,86,65),center=True)
            else:
                self.paint.text(self.canvas,'Your table is waiting.',(pos,578),17,(98,111,71),center=True)
        self.button((66,635,218,56),'BACK TO TITLE',lambda:setattr(self,'scene','title'))
        if self.mission:
            self.paint.rect(self.canvas,(318,635,466,56),CREAM,13,(131,109,84),2,alpha=248)
            self.paint.text(self.canvas,f'Three-star score: {self.mission.target} + complete goals',
                            (550,654),18,DARK,bold=True,center=True)
        for i,rival in enumerate(self.rivals):
            self.paint.text(self.canvas,f'Affinity {rival.affection}/100',
                            (235 if i==0 else 1032,596),13,(114,89,71),center=True)
        for name, x in (('Bruno', 235), ('Daisy', 1032)):
            locked = name in self.sibling_actions
            self.button((x-150,610,144,25),'CHEER ON ♥',lambda n=name:self.interact_sibling(n,'cheer'),small=True,disabled=locked)
            self.button((x+2,610,144,25),'DARE THEM',lambda n=name:self.interact_sibling(n,'dare'),small=True,disabled=locked)
        self.button((834,640,392,62),'LET’S MAKE A MUD PIE!',self.start_crafting,primary=True)

    def _palette_rect(self, index):
        return pygame.Rect(35,386+index*46,231,41)

    def _work_scale(self):
        return min(1.0, 392/max(1,self.pie.height), 632/max(1,self.pie.footprint))

    def _display_tier_bounds(self):
        scale=self._work_scale()
        total=0.0
        bounds=[]
        for layer in self.pie.layers:
            total+=layer.height
            bounds.append((TABLE_X+(layer.x-layer.width/2)*scale,
                           TABLE_Y-total*scale,layer.width*scale,layer.height*scale))
        return bounds

    def _layer_at(self, position):
        x,y = position
        for i in range(len(self.pie.layers)-1,-1,-1):
            px,py,w,h = self._display_tier_bounds()[i]
            if w and (px-6)<=x<=(px+w+6) and (py-5)<=y<=(py+h+14):
                return i
        return None

    def _deco_at(self,position):
        x,y=position
        for i in range(len(self.pie.decorations)-1,-1,-1):
            d=self.pie.decorations[i]
            if self.pie.layers[d.layer].fallen:
                continue
            scale=self._work_scale()
            px,py=decoration_anchor(self.pie,d,TABLE_X,TABLE_Y,scale)
            if (px-x)**2+(py-y)**2<(26*scale+8)**2:
                return i
        return None

    def _relative_deco(self, layer_i, pos):
        layer=self.pie.layers[layer_i]
        height=sum(l.height for l in self.pie.layers[:layer_i+1])
        scale=self._work_scale()
        x=clamp(((pos[0]-TABLE_X)/scale-layer.x)/max(layer.width*.44,1),-1,1)
        y=clamp((pos[1]-(TABLE_Y-height*scale))/(max(layer.height*.77*scale,1)),0,1)
        return x,y

    def add_mud_flecks(self, pos, amount=5):
        """Small brief soil splashes, respecting reduced motion preferences."""
        if self.settings.get('reduced_motion'):
            return
        x, y = pos
        for i in range(amount):
            direction = (i * 2.399 + self.timer * 5) % (2 * math.pi)
            speed = 24 + i * 6
            self.mud_flecks.append([float(x), float(y),
                math.cos(direction) * speed, math.sin(direction) * speed - 30,
                .36 + i*.028, 1 + i%3])
        self.mud_flecks = self.mud_flecks[-90:]

    def draw_mud_flecks(self):
        for x, y, _, _, ttl, r in self.mud_flecks:
            if 0 < x < W and 0 < y < H:
                tone = (116, 80, 53) if r > 1 else (165, 121, 77)
                pygame.draw.circle(self.canvas, tone, (int(x),int(y)),r)

    def draw_craft(self):
        self.canvas.blit(self.paint.images['table'],(0,0))
        self.draw_ambience()
        self._heading(f'Your workbench · {self.theme[0]}','Tiny paws. Serious masterpieces.  •  No time limit')
        self.button((1059,17,201,56),'SAVE MY PIE' if self.mode=='free' else 'SUBMIT PIE',self.submit,primary=True,disabled=not self.pie.layers)
        self.paint.rect(self.canvas,(20,105,263,587),CREAM,21,(117,90,61),2,alpha=245)
        self.paint.text(self.canvas,'YOUR TOOLS',(40,116),21,DARK,bold=True)
        for i,tool in enumerate(TOOLS):
            self.button((35,145+47*i,233,41),f'{i+1}. {tool}',lambda n=i:setattr(self,'tool',n),
                        active=(self.tool==i),small=True)
        self.paint.text(self.canvas,'INGREDIENTS',(40,352),20,DARK,bold=True)
        for i,kind in enumerate(INGREDIENTS):
            rect=self._palette_rect(i)
            selected=self.selected==kind
            self.paint.rect(self.canvas,rect,(178,191,138) if selected else PAPER,10,(132,106,78),2)
            draw_ingredient(self.canvas,kind,rect.x+26,rect.y+20,.78,color_variant=self.color_variant)
            self.paint.text(self.canvas,kind.title(),(rect.x+60,rect.y+10),18,
                            INK if self.allowed_ingredient(kind) else (165,151,135),bold=selected)
            if not self.allowed_ingredient(kind):
                self.paint.text(self.canvas,'NOT TODAY',(rect.x+144,rect.y+11),11,(171,77,65),bold=True)
            if kind=='mud':
                self.paint.text(self.canvas,'drag to add tier',(rect.x+135,rect.y+11),12,(130,106,84))
        self.paint.rect(self.canvas,(1039,107,221,579),CREAM,20,(121,92,64),2,alpha=245)
        self.paint.text(self.canvas,'PIE REPORT',(1054,119),20,DARK,bold=True)
        stab=evaluate_stability(self.pie, weather=self.mission.weather if self.mission else 'clear')
        self.paint.text(self.canvas,f'{len(self.pie.layers)} muddy tiers',(1055,159),18,INK)
        self.paint.text(self.canvas,f'{len(self.pie.decorations)} decorations',(1055,187),18,INK)
        if self.pie.layers:
            worked = sum(l.workable for l in self.pie.layers)
            self.paint.text(self.canvas,f'Kneaded tiers: {worked}/{len(self.pie.layers)}',(1055,211),14,INK)
        self._stat_bar('Stability',stab.score,1055,230,180)
        self.paint.wrap(self.canvas,stab.notes[-1],1055,270,176,15)
        if self.mission and self.mission.weather != 'clear':
            self.paint.text(self.canvas,f'Weather: {self.mission.weather.upper()}',
                            (1055,313),12,(150,86,64),bold=True)
        self.paint.text(self.canvas,'TODAY’S CHALLENGE' if self.mission else 'CREATIVE MEADOW',
                        (1055,335),17,DARK,bold=True)
        if self.mission:
            for i,goal in enumerate(self.mission.goals[:3]):
                value, ok = goal_progress(self.pie,goal, self.mission.weather)
                # One complete objective per line with progress directly underneath.
                # The old 133-pixel label was clipped to 'At least 1 mud t…'
                # and concealed essential rules from new players.
                y = 356 + i * 24
                self.paint.text(self.canvas,('OK ' if ok else '- ')+goal.label,
                                (1055,y),11,(54,130,72) if ok else INK,max_w=187)
                self.paint.text(self.canvas,f'{value:g}/{goal.target:g}',
                                (1197,y+12),10,(54,130,72) if ok else INK,max_w=50)
        else:
            self.paint.wrap(self.canvas,'Build anything! Nothing is graded.',1055,360,183,15)
        self.button((1054,431,190,34),
                    f'COLOR {self.color_variant+1}/{unlocked_colors(self.campaign)} (C)',
                    self.cycle_color,small=True)
        if self.campaign['next_story'] >= 6:
            self.paint.text(self.canvas,'M: Twin decor '+('ON' if self.mirror_mode else 'OFF'),
                            (1055,462),12,DARK,bold=self.mirror_mode)
        self.button((1054,465,91,40),'UNDO',self.undo,small=True)
        self.button((1152,465,92,40),'REDO',self.redo,small=True)
        self.button((1054,513,190,43),'START OVER',lambda:self.show_overlay('reset'),small=True)
        self.button((1054,563,190,42),'HELP / ? ',lambda:self.show_overlay('tutorial'),small=True)
        self.button((1054,611,190,43),'PAUSE / ESC',lambda:self.show_overlay('settings'),small=True)
        # Ingredient target/workbench hints.
        self.paint.rect(self.canvas,(321,111,702,45),(228,213,173),15,(157,126,85),1,alpha=232)
        instr = (
            'DRAG MUD from the bowl to the table. Stir a tier by dragging it.',
            'SPREAD sideways or THICKEN upward: the same mud changes shape.',
            'DRAG MUD to add a tier; drag an existing tier to shift its balance.',
            f'DRAG {self.selected.upper()} from the tray onto a tier. Right-click to remove.'
        )[self.tool]
        self.paint.text(self.canvas,instr,(339,122),17,INK,max_w=670)
        if self.pie.layers:
            wobble=math.sin(self.timer*8)*3 if stab.risk!='stable' and not self.settings['reduced_motion'] else 0
            draw_pie(self.canvas,self.pie,TABLE_X,TABLE_Y,self._work_scale(),wobble)
        else:
            self.paint.rect(self.canvas,(461,349,401,133),(226,208,166),23,(137,107,73),2,alpha=214)
            self.paint.text(self.canvas,'A blank canvas of glorious dirt!',(661,384),23,DARK,bold=True,center=True)
            self.paint.text(self.canvas,'Drag MUD from the tray to begin.',(661,428),19,INK,center=True)
        self.draw_mud_flecks()
        # The player is physically present at the craft bench: a tiny plush
        # spectator, drawn BEHIND any grabbed object and without a click target.
        # Keep the center of the work area unobstructed for hands-on shaping.
        cub_expression = 'cheer' if len(self.pie.layers) >= 3 and len(self.pie.decorations) >= 4 else None
        cub_thought = ('I DID THAT!' if cub_expression == 'cheer' else
                       'Squish squish!' if self.pie.layers else 'Gimme mud!')
        self.paint.rect(self.canvas, (844, 359, 170, 44), (244, 222, 178),
                        2, (115, 83, 62), 2, alpha=244)
        self.paint.text(self.canvas, cub_thought, (929, 381), 16, (84, 65, 53),
                        bold=True, center=True, max_w=153)
        self._sprite('player', (926, 528), (190, 228), expression=cub_expression)
        if self.drag and self.drag.get('type')=='palette':
            x,y=self.mouse
            draw_ingredient(self.canvas,self.drag['kind'],x,y,1.4)
            if WORKSPACE.collidepoint(self.mouse):
                pygame.draw.circle(self.canvas,(255,241,189),(x,y),18,2)
        self.paint.rect(self.canvas,(314,647,714,58),(222,204,161),15,(134,109,72),2,alpha=247)
        tip=("Mix a tier by circling your paw. Knead until firm; excessive water is risky.",
             "Stretch sideways to flatten; drag up to thicken and narrow. No free mud!",
             "Stack: drag a tier to move it; drag upward to bring it to the top.",
             "Decorate: choose a color (C), mirror pairs (M), and drag items. R rotates latest.")[self.tool]
        self.paint.wrap(self.canvas,tip,329,658,683,16)

    def draw_presentation(self):
        self.canvas.blit(self.paint.images['forest'],(0,0))
        self.draw_ambience()
        idx=self.presentation_step
        who=self.names[idx]
        self._heading(f'Presenting: {who}!',f'{self.theme[0]} · the judges are watching very closely')
        self.paint.rect(self.canvas,(48,113,834,520),CREAM,26,(110,89,69),3,alpha=239)
        ready_to_fall = self.collapsed.get(who,False)
        has_fallen = self.timer-self.presentation_since >= 1.45
        pie=self.display_entries[idx] if (has_fallen or not ready_to_fall) else self.entries[idx]
        scale=min(1.25,365/max(1,pie.height),500/max(1,pie.footprint))
        tremor=math.sin(self.timer*21)*9 if ready_to_fall and not has_fallen and not self.settings['reduced_motion'] else 0
        draw_pie(self.canvas,pie,467,534,scale,tremor)
        self.paint.text(self.canvas,self.entries[idx].title,(472,562),25,DARK,bold=True,center=True,max_w=750)
        if ready_to_fall:
            self.paint.rect(self.canvas,(154,265,407,57),(199,139,104),14,(153,85,68),2)
            text='OH NO! THE UPPER TIER COLLAPSED!' if has_fallen else 'UH-OH… THAT TOWER IS WOBBLING!'
            self.paint.text(self.canvas,text,(164,284),18,(104,51,49),bold=True)
        self.paint.rect(self.canvas,(912,112,329,521),CREAM,24,(110,89,69),2,alpha=242)
        character='player' if idx==0 else who.lower()
        self._sprite(character,(1073,269),(194,230),
                     expression='sad' if ready_to_fall and has_fallen else 'cheer')
        score=self.judgments[idx].total
        self.paint.text(self.canvas,f'Judge average: {score:.1f}',(939,391),23,DARK,bold=True)
        strongest=max(FEATURES,key=lambda k:self.judgments[idx].features[k])
        self.paint.text(self.canvas,f'Best trait: {strongest}',(940,430),18,INK)
        note='Petal: ' + self.judgments[idx].verdicts[0].comment
        if self.collapsed.get(who) and who=='Bruno':
            note='Daisy giggles. Bruno insists it was a DESIGN choice.'
        self.paint.wrap(self.canvas,note,940,477,276,17)
        self.paint.rect(self.canvas,(47,646,250,57),(216,197,155),14,(120,103,76),2,alpha=232)
        self.paint.text(self.canvas,'JUDGING IN PROGRESS',(172,674),16,INK,bold=True,center=True)
        self.button((915,643,323,59), 'SEE THE NEXT PIE  →' if idx<2 else 'OPEN THE RESULTS  →',
                    self.advance_presentation,primary=True)
        self.paint.text(self.canvas,f'{idx+1} / 3',(790,663),19,INK,bold=True)

    def advance_presentation(self):
        if self.presentation_step<2:
            self.presentation_step+=1
            self.presentation_since=self.timer
            self.collapse_sound_played=False
            self.sfx('pop')
        else:
            self.finish_round()

    def draw_results(self):
        self.canvas.blit(self.paint.images['forest'],(0,0))
        self.draw_ambience()
        winner=self.last_winner
        self._heading(f'And the winner is… {winner.upper()}!',f'{self.theme[0]} · Round {self.round_no-1} results')
        if self.mission:
            medal_message=f'Challenge stars: {self.mission_medals} / 3'
            self.paint.rect(self.canvas,(840,372,398,32),PAPER,11,(110,95,71),1)
            self.paint.text(self.canvas,medal_message,(854,380),17,DARK,bold=True)
        for i,name in enumerate(self.names):
            x=42+i*415
            iswinner=(name==winner)
            self.paint.rect(self.canvas,(x,117,385,270),(255,240,196) if iswinner else CREAM,22,
                            (170,119,65) if iswinner else (105,92,65),3,alpha=246)
            self._sprite(name, (x+66,172), (84,102), False,
                         expression='cheer' if iswinner else 'sad')
            pie=self.display_entries[i]
            scale=min(.58,143/max(1,pie.height))
            draw_pie(self.canvas,pie,x+190,277,scale)
            self.paint.text(self.canvas,name,(x+22,302),24,DARK,bold=True)
            self.paint.text(self.canvas,f'{self.judgments[i].total:.1f} pts',(x+190,304),24,DARK,bold=True)
            if iswinner:
                self.paint.text(self.canvas,'FOREST CHAMPION',(x+24,345),19,(137,100,43),bold=True)
            self.button((x+270,341,97,37),'INSPECT',lambda j=i:setattr(self,'inspected',j),
                        small=True,active=self.inspected==i)
        evaluation=self.judgments[self.inspected]
        name=self.names[self.inspected]
        self.paint.rect(self.canvas,(42,404,777,265),CREAM,21,(111,94,67),2,alpha=245)
        self.paint.text(self.canvas,f'{name} · Score breakdown',(65,421),28,DARK,bold=True)
        for j,(feature,value) in enumerate(evaluation.features.items()):
            y=469+j*36
            self.paint.text(self.canvas,feature,(70,y),17,INK,bold=True)
            self.paint.rect(self.canvas,(225,y+3,435,17),(216,206,179),8)
            self.paint.rect(self.canvas,(225,y+3,int(435*value/100),17),(99,145,100),8)
            self.paint.text(self.canvas,f'{value:.0f} / 100',(676,y),17,INK)
        self.paint.rect(self.canvas,(840,405,397,265),CREAM,21,(111,94,67),2,alpha=245)
        self.paint.text(self.canvas,'WHAT THE JUDGES SAID',(858,422),20,DARK,bold=True)
        for j,v in enumerate(evaluation.verdicts):
            y=468+j*51
            self.paint.text(self.canvas,f'{v.name} · {v.score:.1f}',(861,y),17,INK,bold=True)
            self.paint.text(self.canvas,v.comment,(861,y+22),14,(94,88,70),max_w=350)
        if self.events:
            event=self.events[1 if self.inspected==2 else 0]
            self.paint.text(self.canvas,event,(860,628),13,(110,78,60),max_w=349)
        retry_required=(self.mission is not None and not self.mission.side
                        and self.mission_medals==1 and
                        STORY.index(self.mission)==self.campaign['next_story'])
        self.button((840,671,392,44),
                    'RETRY CHALLENGE GOALS' if retry_required else 'VIEW FOREST FINALE' if self.campaign['next_story'] == 36 and self.mission and not self.mission.side else 'CHAPTER MAP' if self.campaign['next_story'] == 36 else 'NEXT STORY CONTEST',
                    (lambda mid=self.mission.id:self.begin_round(mid)) if retry_required else (lambda:setattr(self,'scene','epilogue')) if self.campaign['next_story'] == 36 and self.mission and not self.mission.side else (lambda:setattr(self,'scene','campaign')) if self.campaign['next_story'] == 36 else self.begin_round,
                    primary=True,small=True)
        self.button((45,672,300,42),'BACK TO TITLE',lambda:setattr(self,'scene','title'),small=True)
        if self.mission:
            self.button((355,672,455,42),'CHALLENGE REPORT',lambda:self.show_overlay('report'),small=True)

    def draw_gallery(self):
        self.canvas.blit(self.paint.images['forest'],(0,0))
        pages=max(1,(len(self.gallery)+8)//9)
        self.gallery_page=max(0,min(self.gallery_page,pages-1))
        self._heading('Your muddy scrapbook',f'{len(self.gallery)} creations · Page {self.gallery_page+1}/{pages}')
        self.button((1020,20,222,53),'TITLE SCREEN',lambda:setattr(self,'scene','title'))
        self.button((704,28,135,40),'← NEWER',lambda:self.turn_gallery_page(-1),small=True,
                    disabled=self.gallery_page==0)
        self.button((849,28,142,40),'OLDER →',lambda:self.turn_gallery_page(1),small=True,
                    disabled=self.gallery_page>=pages-1)
        if not self.gallery:
            self.paint.rect(self.canvas,(183,212,919,238),CREAM,25,(108,92,67),2,alpha=247)
            self.paint.text(self.canvas,'No masterpieces yet. Your first competition awaits!',(642,318),27,DARK,center=True)
            return
        entries=list(reversed(self.gallery))[self.gallery_page*9:self.gallery_page*9+9]
        for i,entry in enumerate(entries):
            x=45+(i%3)*411
            y=108+(i//3)*198
            self.paint.rect(self.canvas,(x,y,389,180),CREAM,18,(115,95,66),2,alpha=244)
            try:
                draw_pie(self.canvas,Pie.from_dict(entry['pie']),x+187,y+138,.39)
                label=('Free-build creation' if entry.get('free') else f"Round {entry['round']} · {entry['score']:.1f} pts")
            except (KeyError,ValueError,TypeError):
                label='An older, damaged scrapbook entry'
            self.paint.text(self.canvas,label,(x+14,y+12),19,DARK,bold=True,max_w=350)
            self.paint.text(self.canvas,entry.get('theme','Forest contest'),(x+14,y+39),15,INK,max_w=350)

    def turn_gallery_page(self, amount):
        pages=max(1,(len(self.gallery)+8)//9)
        self.gallery_page=max(0,min(self.gallery_page+amount,pages-1))

    def draw_epilogue(self):
        self.canvas.blit(self.paint.images['forest'],(0,0))
        stats=campaign_statistics(self.campaign)
        self.paint.rect(self.canvas,(111,84,1052,567),CREAM,31,(145,101,53),4,alpha=244)
        self.paint.text(self.canvas,'THE GOLDEN MUD CUP', (640,122),48,DARK,bold=True,center=True)
        self.paint.text(self.canvas,'A forest full of muddy memories.',(640,192),26,INK,center=True)
        self._sprite('bruno',(365,373),(212,253))
        self._sprite('player',(640,359),(238,285))
        self._sprite('daisy',(923,373),(212,253))
        if self.campaign['next_story']==36:
            message='You completed all 36 story contests. Your siblings still want rematches!'
        else:
            message='The Golden Mud Cup awaits at the end of the story.'
        self.paint.text(self.canvas,message,(640,516),19,DARK,bold=True,center=True,max_w=985)
        self.paint.text(self.canvas,' · '.join(CHAPTERS[i].keepsake for i in self.campaign['chapter_rewards'])[:135],
                        (640,236),13,(119,85,54),center=True,max_w=980)
        self.paint.text(self.canvas,f"{stats['stars']} earned stars · {stats['side_done']} commissions · {len(self.gallery)} creations in your scrapbook",
                        (640,555),18,INK,center=True)
        self.button((165,593,305,46),'CHAPTER MAP',lambda:setattr(self,'scene','campaign'),small=True)
        self.button((486,593,306,46),'FREE BUILD',self.start_free_build,small=True)
        self.button((807,593,302,46),'TITLE',lambda:setattr(self,'scene','title'),small=True)

    def show_overlay(self, name):
        self.overlay=name
        self.sfx('pop')

    def close_overlay(self):
        self.overlay=None

    def _overlay_button(self,rect,text,callback,primary=False):
        r=pygame.Rect(rect)
        hovered=r.collidepoint(self.mouse)
        self.paint.rect(self.canvas,r,(251,205,137) if (primary or hovered) else PAPER,14,(115,93,66),2)
        self.paint.text(self.canvas,text,r.center,20,INK,bold=True,center=True,max_w=r.width-16)
        self.buttons.append((r,callback))

    def draw_overlay(self):
        veil=pygame.Surface((W,H),pygame.SRCALPHA)
        veil.fill((24,40,30,165))
        self.canvas.blit(veil,(0,0))
        if self.overlay=='settings':
            self.paint.rect(self.canvas,(328,81,630,568),CREAM,28,(90,78,54),4)
            self.paint.text(self.canvas,'PAUSE & SETTINGS',(373,111),35,DARK,bold=True)
            for i,(key,label) in enumerate((('sound','Sound effects'),('music','Forest music'),('reduced_motion','Reduced motion'))):
                self._overlay_button((376,174+i*59,532,47),f"{label}: {'ON' if self.settings[key] else 'OFF'}",
                                     lambda k=key:self.toggle_setting(k))
            for i,(key,label) in enumerate((('sound_volume','SFX volume'),('music_volume','Music volume'))):
                y=362+i*50
                self.paint.text(self.canvas,f'{label}: {round(self.settings[key]*100)}%',(380,y+8),20,DARK,bold=True)
                self._overlay_button((756,y,60,41),'-',lambda k=key:self.adjust_volume(k,-.1))
                self._overlay_button((826,y,60,41),'+',lambda k=key:self.adjust_volume(k,+.1))
            self._overlay_button((376,483,532,48),'FULLSCREEN / WINDOWED (F11)',self.toggle_fullscreen)
            self._overlay_button((376,556,532,58),'RETURN TO THE GAME',self.close_overlay,True)
        elif self.overlay=='tutorial':
            self.paint.rect(self.canvas,(233,103,814,515),CREAM,27,(88,77,51),4)
            self.paint.text(self.canvas,'HOW TO BECOME A MUD LEGEND',(273,133),32,DARK,bold=True)
            lines=[
                '1. DRAG MUD from the tray. Every scoop has a finite fixed volume.',
                '2. SCOOP / MIX (1): stir across a tier until the mud holds together.',
                '3. SHAPE (2): spread sideways to flatten; UP thickens and narrows.',
                '4. STACK (3): move tiers sideways, or drag UP to reorder them.',
                '5. DECORATE (4): drag objects onto tiers; spread details out!',
                '6. Right-click a decoration to remove it; right-click mud for a new shape.',
                '7. Ctrl+Z/Y undo/redo; R rotates the latest decoration.',
                '8. C changes colors. M mirrors (Ch. 2); D dries mud (Ch. 4).',
                '9. In the clearing, cheer or dare a sibling to change their entry.'
            ]
            for i,line in enumerate(lines):
                self.paint.wrap(self.canvas,line,278,191+i*38,730,17)
            self._overlay_button((438,541,401,56),'I GOT THIS!',self.close_overlay,True)
        elif self.overlay=='report':
            self.paint.rect(self.canvas,(216,88,848,544),CREAM,26,(96,80,57),4)
            self.paint.text(self.canvas,'CONTEST REPORT', (260,117),34,DARK,bold=True)
            if self.mission:
                self.paint.text(self.canvas,self.mission.title,(260,169),25,INK,bold=True)
                self.paint.text(self.canvas,
                    f'Stars: {self.mission_medals}/3   ·   Three-star target: {self.mission.target} points',
                    (260,206),20,DARK,bold=True)
                for i,(goal,value,ok) in enumerate(self.mission_checks):
                    self.paint.rect(self.canvas,(254,252+i*57,766,48),
                                    (172,191,145) if ok else (226,192,155),12)
                    self.paint.text(self.canvas,('PASS  ' if ok else 'TRY AGAIN  ')+goal.label,
                                    (270,265+i*57),17,DARK,bold=True,max_w=560)
                    self.paint.text(self.canvas,f'Your value: {value:g}',(824,265+i*57),16,INK,max_w=180)
                self.paint.wrap(self.canvas,
                    'Both goals must pass to unlock the next story contest.' if self.mission_medals==1 and not self.mission.side else self.mission.story,
                    260,452,751,19)
                if not self.mission.side and self.mission.chapter in self.campaign['chapter_rewards']:
                    self.paint.text(self.canvas,'Chapter keepsake: '+CHAPTERS[self.mission.chapter].keepsake,
                                    (260,512),16,(132,91,41),bold=True)
            self._overlay_button((420,553,438,53),'BACK TO RESULTS',self.close_overlay,True)
        elif self.overlay=='chapter':
            ch=CHAPTERS[self.mission.chapter]
            self.paint.rect(self.canvas,(211,83,858,558),CREAM,28,(94,77,52),4)
            self.paint.text(self.canvas,f'CHAPTER {self.mission.chapter+1}: {ch.name}',(252,110),32,DARK,bold=True)
            self.paint.wrap(self.canvas,ch.introduction,255,170,752,20)
            self._sprite('bruno',(357,351),(164,196))
            self._sprite('daisy',(895,351),(164,196))
            self.paint.wrap(self.canvas,ch.bruno_line,244,464,354,18)
            self.paint.wrap(self.canvas,ch.daisy_line,665,464,346,18)
            self._overlay_button((256,558,355,58),'ENCOURAGE MY SIBLINGS',lambda:self.choose_chapter(True),True)
            self._overlay_button((626,558,384,58),'CHALLENGE THEM TO COMPETE',lambda:self.choose_chapter(False))
        elif self.overlay=='reset':
            self.paint.rect(self.canvas,(358,230,564,263),CREAM,25,(96,82,55),4)
            self.paint.text(self.canvas,'START OVER?',(399,268),35,DARK,bold=True)
            self.paint.wrap(self.canvas,'Your current mud pie will be cleared. Undo history will be kept, just in case!',402,331,477,21)
            self._overlay_button((388,416,234,56),'KEEP MY PIE',self.close_overlay)
            self._overlay_button((638,416,247,56),'CLEAR THE TABLE',self.reset_pie,True)

    def reset_pie(self):
        self.snapshot()
        self.pie=Pie(title=f'My masterpiece #{self.round_no}')
        self.close_overlay()
        self.sfx('splat')

    def toggle_setting(self,key):
        self.settings[key]=not self.settings[key]
        if key=='music' and self.music_enabled:
            if self.settings[key]:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()
        self.save()

    def adjust_volume(self,key,change):
        self.settings[key]=round(clamp(self.settings[key]+change,0,1),2)
        if key=='music_volume' and self.music_enabled:
            pygame.mixer.music.set_volume(self.settings[key])
        if key=='sound_volume':
            self.sfx('pop')
        self.save()

    def toggle_fullscreen(self):
        self.fullscreen=not self.fullscreen
        try:
            flags=pygame.FULLSCREEN if self.fullscreen else pygame.RESIZABLE
            self.display=pygame.display.set_mode((1280,720),flags)
        except pygame.error:
            self.fullscreen=False
            self.display=pygame.display.set_mode((1280,720),pygame.RESIZABLE)
            self.notify('Fullscreen unavailable on this display.')

    def draw(self):
        self.buttons=[]
        if self.scene=='title': self.draw_title()
        elif self.scene=='clearing': self.draw_clearing()
        elif self.scene=='craft': self.draw_craft()
        elif self.scene=='presentation': self.draw_presentation()
        elif self.scene=='results': self.draw_results()
        elif self.scene=='gallery': self.draw_gallery()
        elif self.scene=='campaign': self.draw_campaign()
        elif self.scene=='epilogue': self.draw_epilogue()
        if self.toast_time>0:
            # Avoid covering the workbench title, which formerly spent much
            # of crafting gameplay hidden behind long notifications.
            if self.scene == 'craft' and not self.overlay:
                r, center, max_w = (322, 166, 702, 43), (673, 187), 665
            else:
                r, center, max_w = (295, 32, 668, 50), (630, 57), 628
            self.paint.rect(self.canvas,r,(224,203,153),15,(125,95,63),2,alpha=250)
            self.paint.text(self.canvas,self.toast,center,16,INK,bold=True,center=True,max_w=max_w)
        if self.overlay:
            self.buttons=[]
            self.draw_overlay()
        dw,dh=self.display.get_size()
        scale=min(dw/W,dh/H)
        sw,sh=max(1,round(W*scale)),max(1,round(H*scale))
        img=pygame.transform.scale(self.canvas,(sw,sh)) if (sw,sh)!=(W,H) else self.canvas
        self.display.fill((28,43,35))
        self.display.blit(img,((dw-sw)//2,(dh-sh)//2))
        pygame.display.flip()

    def to_logical(self, position):
        dw,dh=self.display.get_size()
        scale=min(dw/W,dh/H)
        if scale<=0:
            return (-100,-100)
        ox,oy=(dw-W*scale)/2,(dh-H*scale)/2
        return (int((position[0]-ox)/scale),int((position[1]-oy)/scale))

    def on_down(self, pos,button):
        self.mouse=pos
        if button==1:
            for rect,callback in reversed(self.buttons):
                if rect.collidepoint(pos):
                    callback()
                    self.sfx('pop')
                    return
        if self.overlay or self.scene!='craft':
            return
        if button==3:
            d=self._deco_at(pos)
            if d is not None:
                self.snapshot()
                self.pie.decorations.pop(d)
                self.sfx('pop')
                self.notify('Decoration removed.')
            elif self.tool==1:
                l=self._layer_at(pos)
                if l is not None:
                    self.snapshot()
                    layer=self.pie.layers[l]
                    layer.shape=SHAPES[(SHAPES.index(layer.shape)+1)%len(SHAPES)]
                    self.sfx('squish')
            return
        if button!=1:
            return
        # Palette drag and ingredient selection, even if the tool differs.
        for i,kind in enumerate(INGREDIENTS):
            if self._palette_rect(i).collidepoint(pos):
                if not self.allowed_ingredient(kind):
                    self.notify(f'{kind.title()} are unavailable in this contest!')
                    return
                self.selected=kind
                self.drag={'type':'palette','kind':kind,'start':pos,'last':pos,'distance':0.}
                self.sfx('pop')
                return
        if not WORKSPACE.collidepoint(pos):
            return
        if self.tool==3:
            d=self._deco_at(pos)
            if d is not None:
                self.snapshot()
                self.drag={'type':'deco','idx':d,'start':pos,'last':pos}
            else:
                l=self._layer_at(pos)
                if l is not None and self.selected in DECORATIONS and self.allowed_ingredient(self.selected):
                    self.snapshot()
                    x,y=self._relative_deco(l,pos)
                    self.place_decoration(self.selected,l,x,y)
                    self.sfx('pop')
            return
        l=self._layer_at(pos)
        if l is None:
            self.notify('Grab MUD from the ingredient tray first!')
            return
        self.snapshot()
        layer=self.pie.layers[l]
        if self.tool==0:
            self.drag={'type':'mix','idx':l,'last':pos,'distance':0,'initial':layer.wetness,'worked':layer.worked}
        elif self.tool==1:
            self.drag={'type':'shape','idx':l,'start':pos,'width':layer.width,'height':layer.height}
        elif self.tool==2:
            self.drag={'type':'stackmove','idx':l,'start':pos,'initial_x':layer.x}

    def on_motion(self,pos):
        self.mouse=pos
        if not self.drag or self.overlay or self.scene!='craft':
            return
        d=self.drag
        if d['type']=='palette':
            d['distance']+=math.dist(d['last'],pos)
            d['last']=pos
        elif d['type']=='mix':
            if self.timer-self.last_fleck_time>.07:
                self.add_mud_flecks(pos)
                self.last_fleck_time=self.timer
            d['distance']+=math.dist(d['last'],pos)
            d['last']=pos
            layer=self.pie.layers[d['idx']]
            layer.mix(d['distance'],starting_wetness=d['initial'],starting_worked=d['worked'])
        elif d['type']=='shape':
            if self.timer-self.last_fleck_time>.09:
                self.add_mud_flecks(pos,3)
                self.last_fleck_time=self.timer
            layer=self.pie.layers[d['idx']]
            scale=self._work_scale()
            dx=(pos[0]-d['start'][0])/scale
            dy=(pos[1]-d['start'][1])/scale
            if abs(dx) >= abs(dy):
                layer.reshape(d['width'] + dx * 1.1)
            else:
                thickness=clamp(d['height']-dy*.65,23,93)
                layer.reshape(layer.volume / thickness)
        elif d['type']=='stackmove':
            layer=self.pie.layers[d['idx']]
            layer.x=clamp(d['initial_x']+(pos[0]-d['start'][0])/self._work_scale(),-205,205)
        elif d['type']=='deco':
            target=self._layer_at(pos)
            if target is not None:
                deco=self.pie.decorations[d['idx']]
                deco.layer=target
                deco.x,deco.y=self._relative_deco(target,pos)

    def on_up(self,pos,button):
        self.mouse=pos
        if button!=1 or self.scene!='craft' or not self.drag:
            return
        d=self.drag
        self.drag=None
        if d['type']=='palette':
            if not WORKSPACE.collidepoint(pos):
                self.notify(f'{d["kind"].title()} selected. Drag it onto your pie.')
                return
            kind=d['kind']
            if kind=='mud':
                if len(self.pie.layers)>=7:
                    self.notify('Seven tiers is the limit. A brave attempt!')
                    return
                self.snapshot()
                x=clamp(pos[0]-TABLE_X,-150,150)
                # The first layer is anchored near the central pedestal.
                if not self.pie.layers:
                    x=clamp(x,-65,65)
                # A scoop is always the same finite quantity of mud.
                wet=.42+(.13 if self.mission and self.mission.weather=='rain' else 0)
                self.pie.add_layer(x,190,46,wet)
                self.add_mud_flecks(pos, 12)
                self.tool=2 if len(self.pie.layers)>1 else 0
                self.sfx('splat')
            else:
                l=self._layer_at(pos)
                if l is None:
                    self.notify('Decorations must land on a mud tier.')
                    return
                self.snapshot()
                x,y=self._relative_deco(l,pos)
                self.place_decoration(kind,l,x,y)
                self.tool=3
                self.sfx('pop')
        elif d['type']=='stackmove':
            if d['start'][1]-pos[1]>70 and len(self.pie.layers)>1:
                idx=d['idx']
                layer=self.pie.layers.pop(idx)
                self.pie.layers.append(layer)
                for deco in self.pie.decorations:
                    if deco.layer==idx:
                        deco.layer=len(self.pie.layers)-1
                    elif deco.layer>idx:
                        deco.layer-=1
                self.notify('Tier moved to the very top!')
            self.sfx('squish')
        elif d['type']=='shape':
            self.add_mud_flecks(pos, 7)
            layer=self.pie.layers[d['idx']]
            deformation=abs(math.log(max(.01,layer.width)/max(.01,d['width'])))
            if deformation>.22:
                layer.damage=clamp(layer.damage + (deformation-.22)*(.19 if layer.workable else .55),0,1)
            self.notify('The scoop stays the same size: spreading mud makes it thinner.'
                        if layer.width>d['width'] else 'Thicker mud makes a narrower tier.')
            self.sfx('squish')
        elif d['type']=='mix':
            self.add_mud_flecks(pos, 7)
            self.sfx('squish')
            layer=self.pie.layers[d['idx']]
            self.notify('Nicely kneaded! Your mud is pliable and cohesive.' if layer.workable
                        else 'Too soupy! Pat this layer dry (D from Storm Season).'
                        if layer.wetness>.73 else 'Keep stirring to bind the muddy grains.')
        elif d['type']=='deco':
            self.sfx('pop')

    def on_key(self,event):
        if event.key==pygame.K_F12:
            from datetime import datetime
            folder=default_path().parent/'screenshots'
            try:
                folder.mkdir(parents=True,exist_ok=True)
                target=folder/f'pie-{datetime.now():%Y%m%d-%H%M%S}.png'
                pygame.image.save(self.canvas,str(target))
                self.notify(f'Screenshot saved to {target.name}')
            except (OSError,pygame.error) as exc:
                self.notify(f'Screenshot failed: {exc}')
            return
        if event.key==pygame.K_F11:
            self.toggle_fullscreen()
            return
        if event.key==pygame.K_ESCAPE:
            if self.overlay:self.close_overlay()
            elif self.scene in ('craft','clearing','presentation','results'):
                self.show_overlay('settings')
            elif self.scene in ('gallery','campaign','epilogue'):self.scene='title'
            return
        if self.overlay:
            return
        if self.scene=='craft':
            if event.key in (pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4):
                self.tool=event.key-pygame.K_1
            elif event.key==pygame.K_z and event.mod&pygame.KMOD_CTRL:
                self.undo()
            elif event.key==pygame.K_y and event.mod&pygame.KMOD_CTRL:
                self.redo()
            elif event.key==pygame.K_r and self.pie.decorations:
                self.snapshot()
                self.pie.decorations[-1].angle+=30
                self.sfx('pop')
            elif event.key==pygame.K_h or event.key==pygame.K_F1:
                self.show_overlay('tutorial')
            elif event.key==pygame.K_c:
                self.cycle_color()
            elif event.key==pygame.K_m:
                self.toggle_mirror()
            elif event.key==pygame.K_d:
                self.dry_layer()
            elif event.key==pygame.K_RETURN:
                self.submit()
        elif self.scene=='presentation' and event.key in (pygame.K_SPACE,pygame.K_RETURN):
            self.advance_presentation()

    def update(self, dt):
        self.timer+=dt
        self.toast_time=max(0,self.toast_time-dt)
        if self.mud_flecks:
            for p in self.mud_flecks:
                p[0] += p[2] * dt
                p[1] += p[3] * dt
                p[3] += 130 * dt
                p[4] -= dt
            self.mud_flecks = [p for p in self.mud_flecks if p[4] > 0]
        if self.scene in ('clearing','craft','presentation','results','campaign','epilogue'):
            self.campaign['seconds'] += dt
        if self.scene=='presentation' and hasattr(self,'collapsed'):
            who=self.names[self.presentation_step]
            if (self.collapsed.get(who,False) and not self.collapse_sound_played
                    and self.timer-self.presentation_since>=1.45):
                self.collapse_sound_played=True
                self.sfx('splat')

    def handle_event(self, event):
        """Handle one SDL event for both the live loop and automated input tests.

        Bots must send pygame events through this dispatcher rather than calling
        on_down/on_key directly. This keeps resize and letterbox conversion tested.
        """
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEMOTION:
            self.on_motion(self.to_logical(event.pos))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_down(self.to_logical(event.pos), event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.on_up(self.to_logical(event.pos), event.button)
        elif event.type == pygame.KEYDOWN:
            self.on_key(event)
        elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
            if event.w >= 600 and event.h >= 380:
                self.display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    def step_frame(self, dt: float):
        """Advance a single real game-loop frame, processing queued SDL events."""
        self.update(max(0, min(float(dt), .05)))
        for event in pygame.event.get():
            self.handle_event(event)
        self.draw()

    def run(self):
        clock = pygame.time.Clock()
        self.draw()  # Prime button hit-targets before the first event.
        while self.running:
            self.step_frame(clock.tick(60) / 1000)
        self.save()
        pygame.quit()
