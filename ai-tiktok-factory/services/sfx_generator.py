"""
Sound Effects (SFX) Generator and Audio Mixing Helper.
Generates subtle UI transition sounds (whoosh, pop, chime)
and builds a synchronized SFX audio track aligned with visual beats.
"""

import math
import struct
import wave
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import config

SFX_DIR = config.ASSETS_DIR / "sfx"
SFX_DIR.mkdir(parents=True, exist_ok=True)

def generate_sine_tone(freq: float, duration: float, sample_rate: int = 44100, volume: float = 0.5) -> np.ndarray:
    """Generate a clean sine wave."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(2 * np.pi * freq * t) * volume

def generate_whoosh_sfx(output_path: Path, sample_rate: int = 44100):
    """
    Generate a modern, smooth cinematic UI whoosh transition sound (0.35s).
    A filtered sweep from low to mid frequencies with fast exponential rise and decay.
    """
    duration = 0.35
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)
    
    # Frequency sweep from 150 Hz up to 800 Hz and back down to 200 Hz
    freq_curve = 150 + 650 * np.sin(np.pi * (t / duration))
    phase = 2 * np.pi * np.cumsum(freq_curve) / sample_rate
    
    # White noise blended with sine
    rng = np.random.default_rng(42)
    noise = rng.normal(0, 0.15, total_samples)
    
    # Envelope: smooth rise and smooth decay (Bell curve / Hanning)
    envelope = np.sin(np.pi * (t / duration)) ** 2
    
    signal = (np.sin(phase) * 0.4 + noise) * envelope * 0.3
    _save_wav(output_path, signal, sample_rate)

def generate_pop_sfx(output_path: Path, sample_rate: int = 44100):
    """
    Generate a crisp modern UI pop sound (0.08s).
    Fast downward frequency drop (pitch chirp).
    """
    duration = 0.08
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)
    
    # Pitch drops rapidly from 850 Hz to 180 Hz
    freq_drop = 850 * np.exp(-t * 35) + 180
    phase = 2 * np.pi * np.cumsum(freq_drop) / sample_rate
    
    # Fast decaying envelope
    envelope = np.exp(-t * 40)
    signal = np.sin(phase) * envelope * 0.45
    _save_wav(output_path, signal, sample_rate)

def generate_chime_sfx(output_path: Path, sample_rate: int = 44100):
    """
    Generate a soft celestial notification chime (0.6s).
    Dual harmonic tones at 880 Hz (A5) and 1320 Hz (E6).
    """
    duration = 0.6
    total_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, total_samples, False)
    
    envelope = np.exp(-t * 6)
    tone1 = np.sin(2 * np.pi * 880 * t) * 0.3
    tone2 = np.sin(2 * np.pi * 1320 * t) * 0.2
    tone3 = np.sin(2 * np.pi * 1760 * t) * 0.1
    
    signal = (tone1 + tone2 + tone3) * envelope * 0.4
    _save_wav(output_path, signal, sample_rate)

def _save_wav(path: Path, samples: np.ndarray, sample_rate: int):
    """Save 16-bit PCM mono WAV file."""
    # Clip to -1.0 to 1.0
    samples = np.clip(samples, -1.0, 1.0)
    int_samples = (samples * 32767).astype(np.int16)
    
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(int_samples.tobytes())

def ensure_default_sfx() -> Tuple[Path, Path, Path]:
    """Ensure whoosh, pop, and chime WAV files exist in assets/sfx/."""
    whoosh_path = SFX_DIR / "whoosh.wav"
    pop_path = SFX_DIR / "pop.wav"
    chime_path = SFX_DIR / "chime.wav"
    
    if not whoosh_path.exists():
        generate_whoosh_sfx(whoosh_path)
    if not pop_path.exists():
        generate_pop_sfx(pop_path)
    if not chime_path.exists():
        generate_chime_sfx(chime_path)
        
    return whoosh_path, pop_path, chime_path

def build_sfx_timeline_track(
    beat_times: List[float],
    total_duration: float,
    output_path: Path,
    sample_rate: int = 44100
) -> Path:
    """
    Build a continuous master SFX audio track aligned with every visual beat transition.
    Places a subtle whoosh/pop at beat starts.
    """
    whoosh_p, pop_p, chime_p = ensure_default_sfx()
    
    total_samples = int(math.ceil(total_duration * sample_rate))
    master_audio = np.zeros(total_samples, dtype=np.float32)
    
    def load_wav(path: Path) -> np.ndarray:
        with wave.open(str(path), "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
            return data
            
    whoosh_data = load_wav(whoosh_p)
    pop_data = load_wav(pop_p)
    chime_data = load_wav(chime_p)
    
    # Place sound effects at beat boundaries
    for i, t in enumerate(beat_times):
        start_idx = int(t * sample_rate)
        if start_idx >= total_samples:
            continue
            
        # First beat: subtle whoosh; Last beat: chime; Intermediate beats: alternate whoosh/pop
        if i == len(beat_times) - 1:
            sfx = chime_data
            vol = 0.25
        elif i % 2 == 0:
            sfx = whoosh_data
            vol = 0.18
        else:
            sfx = pop_data
            vol = 0.22
            
        end_idx = min(start_idx + len(sfx), total_samples)
        segment_len = end_idx - start_idx
        master_audio[start_idx:end_idx] += sfx[:segment_len] * vol
        
    _save_wav(output_path, master_audio, sample_rate)
    return output_path
