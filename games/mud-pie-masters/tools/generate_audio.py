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
    beat = 60 / 114
    samples = [0.0] * round(32 * beat * RATE)
    melody = [
        [76, 79, 81, 79, 76], [74, 79, 81, 83, 79],
        [76, 81, 84, 81, 79], [77, 81, 79, 76, 77],
        [76, 79, 84, 81, 79], [77, 81, 84, 81, 77],
        [74, 79, 83, 81, 79], [76, 74, 72, 76, 72],
    ]
    chords = [(60,64,67),(67,71,74),(69,72,76),(65,69,72),
              (60,64,67),(65,69,72),(67,71,74),(60,64,67)]

    def pluck(note, onset, beats, gain):
        freq = 440 * 2 ** ((note - 69) / 12)
        start = round(onset * beat * RATE)
        length = round(beats * beat * RATE)
        for i in range(min(length, len(samples) - start)):
            t = i / RATE
            phase = 2 * math.pi * freq * t
            envelope = min(1, t / .022, (length-i) / (RATE * .035)) * math.exp(-t * 6)
            samples[start+i] += gain * envelope * (math.sin(phase) + .15*math.sin(2*phase))

    for bar, (phrase, chord) in enumerate(zip(melody, chords)):
        for offset, note in zip((0,.75,1.5,2.5,3.25), phrase):
            pluck(note, bar*4+offset, .7, .22)
        for offset, note in zip((0,1,2,3), (*chord,chord[1])):
            pluck(note, bar*4+offset, .87, .12)
    destination = OUT / 'music.wav'
    with wave.open(str(destination), 'wb') as track:
        track.setparams((1, 2, RATE, 0, 'NONE', 'not compressed'))
        track.writeframes(struct.pack('<' + 'h' * len(samples), *(round(sample * 32767) for sample in samples)))


if __name__=='__main__':
    for s,d in (('pop',.16),('squish',.31),('splat',.48),('fanfare',.94)):
        synth_effect(s,d)
    synth_music()
    print('Generated 4 original SFX + 1 music loop')
