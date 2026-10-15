"""
Generación de tonos: reproducción con winsound y exportación a .wav.
"""

import time
import wave

import numpy as np

try:
    import winsound  # Generador de tonos de Windows: Beep(frecuencia, duración)
except ImportError:
    winsound = None

FS = 44100


def tocar_tono(frecuencia, duracion_ms):
    """Hace sonar un tono con la frecuencia (Hz) y duración (ms) indicadas."""
    if winsound:
        winsound.Beep(int(round(frecuencia)), int(duracion_ms))
    else:
        time.sleep(duracion_ms / 1000)  # en otros sistemas solo se respeta el tiempo


def tocar(frecuencias, duracion_ms):
    """Una nota suena completa; un acorde se toca arpegiado porque Beep solo da un tono a la vez."""
    for f in frecuencias:
        tocar_tono(f, duracion_ms // len(frecuencias))


def sintetizar(frecuencias, duracion_ms, fs=FS):
    """Onda senoidal (o suma de senoidales para un acorde) con envolvente suave."""
    t = np.linspace(0, duracion_ms / 1000, int(fs * duracion_ms / 1000), endpoint=False)
    onda = sum(np.sin(2 * np.pi * f * t) for f in frecuencias) / len(frecuencias)
    ataque = min(len(t), int(0.01 * fs))
    envolvente = np.exp(-3 * t)
    envolvente[:ataque] *= np.linspace(0, 1, ataque)
    return onda * envolvente


def guardar_wav(segmentos, archivo, fs=FS):
    audio = np.concatenate(segmentos)
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767 * 0.8)
    with wave.open(archivo, "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(fs)
        w.writeframes(audio.tobytes())
