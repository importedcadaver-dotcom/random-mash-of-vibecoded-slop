"""Offline synthesis of original, gentle sound effects and forest music.
No third-party Python libraries or external copyrighted recordings required.
"""
from __future__ import annotations
import math
import random
import struct
import wave
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / 'assets'
RATE = 22050
RNG = random.Random(57)


def save(name, samples):
    destination = OUT / f'{name}.wav'
    with wave.open(str(destination),'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(struct.pack('<'+'h'*len(samples),*(int(max(-1,min(1,x)) * 24500) for x in samples)))


def synth_effect(name, duration):
    count=int(RATE*duration)
    samples=[]
    filtered=0.0
    for i in range(count):
        t=i/RATE
        f=i/max(1,count-1)
        if name=='pop':
            signal=(math.sin(2*math.pi*(540-250*f)*t)*.55 + math.sin(2*math.pi*820*t)*.15)
            envelope=(1-f)**4
        elif name=='squish':
            noise=RNG.uniform(-1,1)
            filtered=filtered*.89+noise*.11
            signal=.55*math.sin(2*math.pi*(135+26*math.sin(t*37))*t)+filtered*.7
            envelope=(math.sin(math.pi*f)**.7)*(.85-.25*f)
        elif name=='splat':
            noise=RNG.uniform(-1,1)
            filtered=filtered*.85+noise*.15
            signal=.6*math.sin(2*math.pi*(95-50*f)*t)+filtered*.85
            envelope=(1-f)**1.3
        else:
            notes=[392,493.88,587.33,784]
            n=min(len(notes)-1,int(t/.2))
            st=t-n*.2
            signal=(math.sin(2*math.pi*notes[n]*t) + .25*math.sin(2*math.pi*notes[n]*2*t))
            envelope=min(1,st/.018)*math.exp(-st*7.0)*.65
        samples.append(signal*envelope*.55)
    save(name,samples)


def synth_music():
    duration=12
    n=duration*RATE
    # Original four-chord pentatonic lullaby. No recognizable licensed tune.
    roots=[196,174.61,220,164.81]
    melody=[392,440,493.88,440,392,349.23,329.63,392,440,392,329.63,293.66,
            329.63,392,440,493.88,523.25,493.88,440,392,349.23,329.63,293.66,392]
    notes_per_sec=2
    data=[]
    for i in range(n):
        t=i/RATE
        chord=min(3,int(t//3))
        root=roots[chord]
        beat=int(t*notes_per_sec)
        phase=(t*notes_per_sec)%1
        note=melody[beat%len(melody)]
        pluck=math.exp(-phase*5)*math.sin(2*math.pi*note*t)
        soft=(math.sin(2*math.pi*root/2*t)+.22*math.sin(2*math.pi*root*t))*.22
        texture=.07*math.sin(2*math.pi*root*1.5*t)*math.sin(2*math.pi*t*.12)
        volume=min(1,t/.55,(duration-t)/.55)
        data.append((.23*pluck+.14*soft+texture)*max(0,volume))
    save('music',data)


if __name__=='__main__':
    for s,d in (('pop',.16),('squish',.31),('splat',.48),('fanfare',.94)):
        synth_effect(s,d)
    synth_music()
    print('Generated 4 original SFX + 1 music loop')
