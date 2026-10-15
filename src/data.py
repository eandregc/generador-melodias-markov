"""
Datos del generador: estados (notas y acordes), frecuencias, matrices de
transición diseñadas con teoría musical y la melodía de referencia.
"""

import numpy as np

# Frecuencias (Hz) en afinación temperada, La4 = 440 Hz
FRECUENCIAS = {
    "Do4": 261.63, "Re4": 293.66, "Mi4": 329.63, "Fa4": 349.23,
    "Sol4": 392.00, "La4": 440.00, "Si4": 493.88, "Do5": 523.25,
}

NOTAS = ["Do4", "Re4", "Mi4", "Fa4", "Sol4", "La4", "Si4", "Do5"]

# Acordes de la tonalidad de Do mayor (tríadas construidas sobre cada grado)
ACORDES = {
    "I (Do)":     ["Do4", "Mi4", "Sol4"],
    "ii (Rem)":   ["Re4", "Fa4", "La4"],
    "iii (Mim)":  ["Mi4", "Sol4", "Si4"],
    "IV (Fa)":    ["Fa4", "La4", "Do5"],
    "V (Sol)":    ["Sol4", "Si4", "Re4"],
    "vi (Lam)":   ["La4", "Do5", "Mi4"],
    "vii° (Si°)": ["Si4", "Re4", "Fa4"],
}
GRADOS = list(ACORDES.keys())

# Duraciones posibles de cada nota: corcheas, negras y negra con punto
DURACIONES_MS = [250, 250, 500, 500, 500, 750]

# Filas = nota actual, columnas = nota siguiente (mismo orden que NOTAS).
# Criterios musicales usados para asignar probabilidades:
#   - Se favorece el movimiento por grado conjunto (notas vecinas).
#   - Saltos de tercera y quinta son frecuentes; saltos grandes son raros.
#   - Si (sensible) tiende fuertemente a resolver en Do.
#   - Fa tiende a resolver en Mi.
#   - Do y Sol (tónica y dominante) funcionan como puntos de apoyo.
P_NOTAS = np.array([
    #  Do4   Re4   Mi4   Fa4   Sol4  La4   Si4   Do5
    [0.05, 0.30, 0.25, 0.05, 0.25, 0.05, 0.00, 0.05],  # Do4
    [0.35, 0.05, 0.30, 0.10, 0.10, 0.00, 0.10, 0.00],  # Re4
    [0.15, 0.25, 0.05, 0.25, 0.25, 0.05, 0.00, 0.00],  # Mi4
    [0.05, 0.10, 0.40, 0.05, 0.25, 0.15, 0.00, 0.00],  # Fa4
    [0.15, 0.05, 0.20, 0.15, 0.05, 0.20, 0.05, 0.15],  # Sol4
    [0.05, 0.00, 0.05, 0.15, 0.40, 0.05, 0.20, 0.10],  # La4
    [0.05, 0.05, 0.00, 0.00, 0.15, 0.15, 0.00, 0.60],  # Si4
    [0.10, 0.00, 0.05, 0.00, 0.30, 0.15, 0.35, 0.05],  # Do5
])

# Progresiones armónicas basadas en armonía funcional:
#   tónica (I, vi, iii) -> subdominante (IV, ii) -> dominante (V, vii°) -> tónica
P_ACORDES = np.array([
    #  I     ii    iii   IV    V     vi    vii°
    [0.05, 0.15, 0.05, 0.30, 0.25, 0.15, 0.05],  # I
    [0.05, 0.05, 0.00, 0.10, 0.60, 0.05, 0.15],  # ii
    [0.05, 0.05, 0.05, 0.30, 0.05, 0.50, 0.00],  # iii
    [0.30, 0.15, 0.05, 0.05, 0.35, 0.05, 0.05],  # IV
    [0.65, 0.00, 0.05, 0.05, 0.05, 0.20, 0.00],  # V
    [0.05, 0.30, 0.05, 0.35, 0.15, 0.05, 0.05],  # vi
    [0.80, 0.00, 0.10, 0.00, 0.05, 0.05, 0.00],  # vii°
])

# Melodía de referencia para el modo "aprendido": Himno a la alegría (Beethoven)
HIMNO_ALEGRIA = [
    "Mi4", "Mi4", "Fa4", "Sol4", "Sol4", "Fa4", "Mi4", "Re4",
    "Do4", "Do4", "Re4", "Mi4", "Mi4", "Re4", "Re4",
    "Mi4", "Mi4", "Fa4", "Sol4", "Sol4", "Fa4", "Mi4", "Re4",
    "Do4", "Do4", "Re4", "Mi4", "Re4", "Do4", "Do4",
    "Re4", "Re4", "Mi4", "Do4", "Re4", "Mi4", "Fa4", "Mi4", "Do4",
    "Re4", "Mi4", "Fa4", "Mi4", "Re4", "Do4", "Re4", "Sol4",
    "Mi4", "Mi4", "Fa4", "Sol4", "Sol4", "Fa4", "Mi4", "Re4",
    "Do4", "Do4", "Re4", "Mi4", "Re4", "Do4", "Do4",
]
