"""Generates a "money counter ramping up" sound effect (money_counter.wav).

Coin ticks speed up and rise in pitch, then finish on a bright payout chime.
"""
import wave
import numpy as np

SR = 44100
DUR = 3.2
RAMP = 2.2  # seconds of ticking before the final chime


def t(sec):
    return np.arange(int(SR * sec)) / SR


def tick(freq, dur=0.09):
    # Short bright coin "tink": two partials, fast decay
    x = t(dur)
    s = (np.sin(2 * np.pi * freq * x)
         + 0.5 * np.sin(2 * np.pi * freq * 2.01 * x)
         + 0.25 * np.sin(2 * np.pi * freq * 3.02 * x))
    return s * np.exp(-x * 45) * np.minimum(1, x / 0.001)


def chime(freq, dur=1.0):
    x = t(dur)
    partials = [(1, 1.0), (2, 0.4), (3, 0.2), (4.2, 0.1)]
    s = sum(a * np.sin(2 * np.pi * freq * r * x) for r, a in partials)
    vib = 1 + 0.15 * np.sin(2 * np.pi * 6 * x)  # little shimmer
    return s * vib * np.exp(-x * 3.5) * np.minimum(1, x / 0.003)


out = np.zeros(int(SR * DUR))


def add(sig, at, gain):
    i = int(at * SR)
    end = min(len(out), i + len(sig))
    out[i:end] += gain * sig[:end - i]


# Ticks: gap shrinks from 0.16s to 0.025s, pitch climbs ~1.5 octaves
now, p = 0.0, 0.0
while now < RAMP:
    p = now / RAMP
    freq = 900 * 2 ** (1.6 * p ** 1.3)
    add(tick(freq), now, 0.35 + 0.25 * p)
    gap = 0.16 * (1 - p) ** 1.8 + 0.025
    now += gap

# Final payout: major chord arpeggio + sustained chord
base = 1046.5  # C6
for i, ratio in enumerate([1, 1.26, 1.5, 2]):
    add(chime(base * ratio, 1.0), RAMP + 0.05 + i * 0.04, 0.3)
add(chime(base * 2, 1.0), RAMP + 0.25, 0.2)

out /= np.max(np.abs(out)) * 1.1
# soft fade at the very end
fade = int(0.15 * SR)
out[-fade:] *= np.linspace(1, 0, fade)
pcm = (out * 32767).astype(np.int16)
with wave.open("money_counter.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote money_counter.wav")
