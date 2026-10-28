"""Generates a "cha-ching" cash register / money sound effect (money.wav)."""
import wave
import numpy as np

SR = 44100
rng = np.random.default_rng(7)


def t(sec):
    return np.arange(int(SR * sec)) / SR


def bell(freq, dur, decay):
    # Metallic bell: inharmonic partials with fast decay
    x = t(dur)
    partials = [(1.0, 1.0), (2.76, 0.5), (5.40, 0.25), (8.93, 0.12), (1.5, 0.3)]
    s = sum(a * np.sin(2 * np.pi * freq * r * x) * np.exp(-x * decay * r ** 0.5)
            for r, a in partials)
    return s * np.minimum(1, x / 0.002)


def click(dur, decay):
    # Mechanical drawer "cha": filtered noise burst
    x = t(dur)
    n = rng.standard_normal(len(x))
    n = np.diff(n, prepend=0)  # brighten
    return n * np.exp(-x * decay)


def coin(freq, dur=0.25):
    x = t(dur)
    s = np.sin(2 * np.pi * freq * x) + 0.6 * np.sin(2 * np.pi * freq * 1.48 * x)
    return s * np.exp(-x * 18)


out = np.zeros(int(SR * 1.6))


def add(sig, at, gain):
    i = int(at * SR)
    end = min(len(out), i + len(sig))
    out[i:end] += gain * sig[:end - i]


add(click(0.08, 60), 0.00, 0.35)   # "cha"
add(click(0.05, 80), 0.06, 0.25)
add(bell(2093, 1.4, 4.0), 0.12, 0.55)  # "ching" (C7)
add(bell(2637, 1.4, 4.5), 0.13, 0.40)  # E7
for i, f in enumerate([3100, 3500, 2900, 3800, 3300]):  # coin jingle
    add(coin(f), 0.20 + i * 0.045 + rng.uniform(0, 0.02), 0.12)

out /= np.max(np.abs(out)) * 1.1
pcm = (out * 32767).astype(np.int16)
with wave.open("money.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote money.wav")
