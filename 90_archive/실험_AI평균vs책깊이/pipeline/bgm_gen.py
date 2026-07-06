"""
절차적 BGM 생성기 — 외부 음원 없이도 들을만한 lo-fi 스타일 앰비언트 트랙
moviepy로 합성될 영상 길이만큼 만들어둔다
샌드박스에서도 동작 (numpy/scipy 의존)
"""
import os, math
import numpy as np
import wave

SR = 44100   # sample rate

# C major pentatonic (소프트하고 안전)
NOTES = [
    220.00, 246.94, 277.18, 329.63, 369.99,  # A3, B3, C#4, E4, F#4
    440.00, 493.88, 554.37,                  # A4, B4, C#5
]

def envelope(t, length, attack=0.02, release=0.6):
    n = len(t)
    env = np.ones(n)
    a = int(attack * n)
    r = int(release * n)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return env

def soft_synth(freq, dur, sr=SR, harmonics=(1.0, 0.4, 0.18, 0.08)):
    """sin + few harmonics + slight detune for soft pad-like tone"""
    n = int(dur * sr)
    t = np.linspace(0, dur, n, endpoint=False)
    wave_ = np.zeros(n)
    for i, amp in enumerate(harmonics):
        f = freq * (i + 1)
        wave_ += amp * np.sin(2 * np.pi * f * t)
    # detune layer
    wave_ += 0.4 * np.sin(2 * np.pi * (freq * 1.005) * t)
    wave_ *= envelope(t, dur)
    return wave_ / max(np.max(np.abs(wave_)), 1e-6) * 0.6

def bell(freq, dur, sr=SR):
    n = int(dur * sr)
    t = np.linspace(0, dur, n, endpoint=False)
    w = np.sin(2 * np.pi * freq * t) * np.exp(-3.0 * t)
    w += 0.3 * np.sin(2 * np.pi * freq * 2.01 * t) * np.exp(-5.0 * t)
    return w * 0.4

def make_track(total_seconds, out_path):
    """Make a slow chord-arpeggio track of given length."""
    rng = np.random.default_rng(42)
    audio = np.zeros(int(total_seconds * SR))
    t = 0.0
    chord_dur = 8.0
    while t < total_seconds:
        # pick 3 notes from pentatonic for a soft chord
        chord = rng.choice(NOTES, size=3, replace=False)
        # play notes spaced over chord_dur with overlap
        for i, freq in enumerate(chord):
            start = t + i * (chord_dur / 6.0)
            note_dur = chord_dur * 0.9
            if start + note_dur > total_seconds:
                note_dur = total_seconds - start
                if note_dur <= 0.1:
                    break
            tone = soft_synth(freq * 0.5, note_dur)  # octave down → bass-like pad
            s = int(start * SR)
            e = s + len(tone)
            if e > len(audio):
                tone = tone[:len(audio) - s]
                e = len(audio)
            audio[s:e] += tone * 0.18
        # occasional bell on first note
        if rng.random() < 0.5:
            f = rng.choice(NOTES) * 2
            tone = bell(f, 1.6)
            s = int(t * SR)
            e = s + len(tone)
            if e > len(audio):
                tone = tone[:len(audio)-s]; e = len(audio)
            audio[s:e] += tone * 0.10
        t += chord_dur

    # very gentle white-noise wash
    noise = (rng.standard_normal(len(audio)) * 0.012)
    audio += noise

    # soft master compressor / clip
    peak = np.max(np.abs(audio))
    if peak > 0.95:
        audio = audio * (0.95 / peak)
    # convert to int16
    pcm = np.int16(audio * 32767)
    # write 16-bit mono wav
    with wave.open(out_path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    out  = os.path.join(here, "audio", "bgm.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    make_track(600, out)
    print("BGM wrote:", out, os.path.getsize(out)//1024, "KB")
