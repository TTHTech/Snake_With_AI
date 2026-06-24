"""Hệ thống âm thanh: tiếng ăn mồi (crunch.wav) + nhạc nền tự sinh (bgm.wav)."""
import os
import wave
import struct
import math
import pygame

SAMPLE_RATE = 22050
_BASE = os.path.dirname(os.path.abspath(__file__))
_SOUND_DIR = os.path.join(_BASE, 'Sound')

sound_enabled = True          # bật/tắt toàn bộ âm thanh
_sounds = {}
_inited = False


def _ensure_mixer():
    if pygame.mixer.get_init() is None:
        try:
            pygame.mixer.init(SAMPLE_RATE, -16, 2, 512)
        except Exception as e:
            print("Mixer init error:", e)


def _note_samples(freq, dur, vol=0.16):
    """Sinh 1 nốt sine có envelope nhẹ để tránh tiếng tách."""
    n = int(SAMPLE_RATE * dur)
    atk = max(1, int(n * 0.04))
    rel = max(1, int(n * 0.25))
    out = []
    for i in range(n):
        if i < atk:
            env = i / atk
        elif i > n - rel:
            env = (n - i) / rel
        else:
            env = 1.0
        out.append(vol * env * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
    return out


def _generate_bgm(path):
    """Tạo vòng lặp nhạc nền nhẹ (thang ngũ cung La thứ)."""
    A3, C4, D4, E4, G4 = 220.0, 261.63, 293.66, 329.63, 392.0
    A4, C5, D5, E5 = 440.0, 523.25, 587.33, 659.25
    R = 0  # nghỉ
    melody = [
        (A4, .32), (C5, .32), (E5, .32), (D5, .32),
        (C5, .32), (A4, .32), (G4, .32), (R, .16),
        (E4, .32), (G4, .32), (A4, .32), (C5, .32),
        (A4, .32), (G4, .32), (E4, .32), (R, .16),
        (D4, .32), (E4, .32), (G4, .32), (A4, .32),
        (C5, .32), (A4, .32), (D5, .32), (R, .16),
        (E5, .32), (D5, .32), (C5, .32), (A4, .32),
        (G4, .32), (E4, .32), (A3, .48), (R, .24),
    ]
    samples = []
    for f, d in melody:
        if f == R:
            samples.extend([0.0] * int(SAMPLE_RATE * d))
        else:
            samples.extend(_note_samples(f, d, vol=0.14))

    with wave.open(path, 'w') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        frames = bytearray()
        for s in samples:
            v = int(max(-1.0, min(1.0, s)) * 32000)
            frames += struct.pack('<hh', v, v)
        w.writeframes(bytes(frames))


def init():
    global _inited
    if _inited:
        return
    _ensure_mixer()
    crunch = os.path.join(_SOUND_DIR, 'crunch.wav')
    try:
        _sounds['eat'] = pygame.mixer.Sound(crunch)
        _sounds['eat'].set_volume(0.5)
    except Exception as e:
        print("Load crunch error:", e)

    bgm = os.path.join(_SOUND_DIR, 'bgm.wav')
    if not os.path.exists(bgm):
        try:
            _generate_bgm(bgm)
        except Exception as e:
            print("BGM generate error:", e)
    _inited = True


def play_eat():
    if sound_enabled and 'eat' in _sounds:
        _sounds['eat'].play()


def start_music():
    if not sound_enabled:
        return
    bgm = os.path.join(_SOUND_DIR, 'bgm.wav')
    if not os.path.exists(bgm):
        return
    try:
        pygame.mixer.music.load(bgm)
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("Music play error:", e)


def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass


def set_enabled(on):
    """Bật/tắt toàn bộ âm thanh."""
    global sound_enabled
    sound_enabled = bool(on)
    if sound_enabled:
        start_music()
    else:
        stop_music()
