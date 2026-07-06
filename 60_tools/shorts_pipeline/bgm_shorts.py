"""쇼츠용 절차생성 BGM (~130초, 약간 긴장감 있는 lo-fi)"""
import os, numpy as np, wave

SR = 44100

def make_track(total_seconds, out_path):
    rng = np.random.default_rng(99)
    audio = np.zeros(int(total_seconds * SR))
    # Pentatonic in A minor, slightly tense
    notes = [220.00, 246.94, 277.18, 329.63, 369.99, 440.00, 493.88]
    chord_dur = 4.0
    t = 0.0
    while t < total_seconds:
        chord = rng.choice(notes, size=3, replace=False)
        for i, freq in enumerate(chord):
            start = t + i * (chord_dur / 6.0)
            note_dur = chord_dur * 0.85
            if start + note_dur > total_seconds:
                note_dur = total_seconds - start
                if note_dur <= 0.1: break
            n = int(note_dur * SR)
            tt = np.linspace(0, note_dur, n, endpoint=False)
            tone = (np.sin(2*np.pi*freq*0.5*tt) + 0.4*np.sin(2*np.pi*freq*1.0*tt) + 0.18*np.sin(2*np.pi*freq*1.5*tt))
            env = np.ones(n)
            a = int(0.02 * n); r = int(0.5 * n)
            if a > 0: env[:a] = np.linspace(0, 1, a)
            if r > 0: env[-r:] = np.linspace(1, 0, r)
            tone *= env / max(np.max(np.abs(tone)), 1e-6) * 0.6
            s = int(start * SR); e = s + len(tone)
            if e > len(audio): tone = tone[:len(audio)-s]; e = len(audio)
            audio[s:e] += tone * 0.18
        t += chord_dur
    # noise
    audio += rng.standard_normal(len(audio)) * 0.012
    peak = np.max(np.abs(audio))
    if peak > 0.95: audio *= 0.95 / peak
    pcm = np.int16(audio * 32767)
    with wave.open(out_path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "audio", "bgm.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    make_track(140, out)
    print("BGM:", out, os.path.getsize(out)//1024, "KB")
