"""
Cadena de Markov de primer orden:

    P(X_{t+1} = j | X_t = i, X_{t-1}, ..., X_0) = P(X_{t+1} = j | X_t = i) = P[i][j]
"""

import numpy as np


def siguiente_estado(fila_probabilidades, rng):
    """
    Método de la transformada inversa: se genera u ~ U(0,1) y se elige el primer
    estado j cuya probabilidad acumulada sea mayor que u.
    """
    u = rng.random()
    acumulada = 0.0
    for j, p in enumerate(fila_probabilidades):
        acumulada += p
        if u < acumulada:
            return j, u
    return len(fila_probabilidades) - 1, u  # por redondeo numérico


class CadenaMarkov:
    def __init__(self, estados, P):
        self.estados = list(estados)
        self.P = np.asarray(P, dtype=float)
        self.validar()

    @classmethod
    def desde_secuencia(cls, secuencia, estados):
        """Estima P[i][j] = (# veces que i va a j) / (# veces que sale de i)."""
        idx = {e: k for k, e in enumerate(estados)}
        conteos = np.zeros((len(estados), len(estados)))
        for actual, siguiente in zip(secuencia[:-1], secuencia[1:]):
            conteos[idx[actual], idx[siguiente]] += 1
        P = np.zeros_like(conteos)
        for i, fila in enumerate(conteos):
            total = fila.sum()
            # Si un estado nunca aparece en el corpus, se deja con distribución uniforme
            P[i] = fila / total if total > 0 else np.full(len(estados), 1 / len(estados))
        return cls(estados, P)

    def validar(self):
        """Verifica que P sea una matriz estocástica (filas no negativas que suman 1)."""
        if np.any(self.P < 0):
            raise ValueError("Hay probabilidades negativas")
        sumas = self.P.sum(axis=1)
        if not np.allclose(sumas, 1.0):
            raise ValueError(f"Las filas no suman 1 -> {sumas}")

    def distribucion_estacionaria(self):
        """Resuelve pi = pi P con sum(pi) = 1 (vector propio izquierdo con valor propio 1)."""
        valores, vectores = np.linalg.eig(self.P.T)
        k = np.argmin(np.abs(valores - 1))
        pi = np.real(vectores[:, k])
        return pi / pi.sum()

    def generar(self, n_transiciones, rng, inicial=None):
        """Simula la cadena y regresa la lista de (índice de estado, u) visitados."""
        actual = self.estados.index(inicial) if inicial else 0
        recorrido = [(actual, None)]
        for _ in range(n_transiciones):
            actual, u = siguiente_estado(self.P[actual], rng)
            recorrido.append((actual, u))
        return recorrido

    def imprimir(self):
        ancho = max(len(e) for e in self.estados) + 1
        print(" " * ancho + "".join(f"{e.split(' (')[0]:>8}" for e in self.estados))
        for e, fila in zip(self.estados, self.P):
            print(f"{e:<{ancho}}" + "".join(f"{p:8.2f}" for p in fila))
