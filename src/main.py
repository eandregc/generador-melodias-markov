"""
Generador de melodías con cadenas de Markov.

Uso:
    python main.py                          # 32 notas, modo notas
    python main.py --modo acordes --n 16
    python main.py --modo aprendido --semilla 7
    python main.py --sin-sonido --wav melodia.wav
"""

import argparse
import random
import sys

from data import (ACORDES, DURACIONES_MS, FRECUENCIAS, GRADOS, HIMNO_ALEGRIA,
                  NOTAS, P_ACORDES, P_NOTAS)
from model import CadenaMarkov
from audio import guardar_wav, sintetizar, tocar


def crear_cadena(modo):
    if modo == "notas":
        return CadenaMarkov(NOTAS, P_NOTAS), "Do4"
    if modo == "acordes":
        return CadenaMarkov(GRADOS, P_ACORDES), "I (Do)"
    return CadenaMarkov.desde_secuencia(HIMNO_ALEGRIA, NOTAS), "Mi4"


def main():
    parser = argparse.ArgumentParser(description="Generador de melodías con cadenas de Markov")
    parser.add_argument("--modo", choices=["notas", "acordes", "aprendido"], default="notas")
    parser.add_argument("--n", type=int, default=32, help="número de transiciones")
    parser.add_argument("--semilla", type=int, default=None,
                        help="semilla del generador aleatorio")
    parser.add_argument("--sin-sonido", action="store_true", help="no reproducir los tonos")
    parser.add_argument("--wav", default=None, help="guardar la melodía en un archivo .wav")
    args = parser.parse_args()

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    rng = random.Random(args.semilla)
    cadena, inicial = crear_cadena(args.modo)

    print(f"\n=== Matriz de transición ({args.modo}) ===")
    cadena.imprimir()
    pi = cadena.distribucion_estacionaria()
    print("\nDistribución estacionaria (proporción de tiempo a largo plazo):")
    print("  " + ", ".join(f"{e}: {p:.3f}" for e, p in zip(cadena.estados, pi)))

    print(f"\n=== Melodía generada: {args.n} transiciones ===")
    print(f"{'t':>3}  {'u ~ U(0,1)':>10}  {'estado':<11} {'frecuencia(s) Hz':<26} dur(ms)")
    segmentos = []
    for t, (k, u) in enumerate(cadena.generar(args.n, rng, inicial)):
        estado = cadena.estados[k]
        duracion = rng.choice(DURACIONES_MS)
        if args.modo == "acordes":
            duracion = 1000  # un acorde por compás
            notas = ACORDES[estado]
        else:
            notas = [estado]
        freqs = [FRECUENCIAS[nota] for nota in notas]
        u_txt = "  (inicio)" if u is None else f"{u:10.4f}"
        f_txt = ", ".join(f"{f:.1f}" for f in freqs)
        print(f"{t:>3}  {u_txt}  {estado:<11} {f_txt:<26} {duracion}", flush=True)

        if not args.sin_sonido:
            tocar(freqs, duracion)
        segmentos.append(sintetizar(freqs, duracion))

    if args.wav:
        guardar_wav(segmentos, args.wav)
        print(f"\nMelodía guardada en {args.wav}")


if __name__ == "__main__":
    main()
