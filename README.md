# Generador de Melodías con Cadenas de Markov
Una melodía es una secuencia de notas que van cambiando a lo largo del tiempo, por lo que puede verse como un **proceso estocástico**: si X_t es la nota que suena en el instante t, la melodía es la colección {X_0, X_1, X_2, ...}. En este proyecto se modela esa secuencia con una **cadena de Markov**, donde la probabilidad de la siguiente nota depende solamente de la nota que está sonando:

```
P(X_{t+1} = j | X_t = i, X_{t-1}, ..., X_0) = P(X_{t+1} = j | X_t = i) = p_ij
```

**Características clave:**

* **Estados:** Las notas de la escala de Do mayor (Do4 a Do5) o, en el modo de acordes, los siete acordes de la tonalidad (I, ii, iii, IV, V, vi, vii°).
* **Matriz de transición:** Las probabilidades se asignaron con teoría musical: se favorece el movimiento por grado conjunto, Si (sensible) resuelve a Do, Fa tiende a Mi y Do y Sol funcionan como notas de reposo. En los acordes se sigue la armonía funcional (tónica → subdominante → dominante → tónica). Cada fila de la matriz suma 1 y el programa lo valida.
* **Generador de números aleatorios:** Cada transición se decide con el método de la transformada inversa: se genera u ~ U(0,1) y se elige el primer estado cuya probabilidad acumulada sea mayor que u.
* **Generación de tonos:** Cada nota se imprime y se reproduce con `winsound.Beep(frecuencia, duración)` usando afinación temperada (La4 = 440 Hz). La melodía también se puede exportar a `.wav`.
* **Distribución estacionaria:** Se calcula π = πP para saber qué proporción del tiempo suena cada nota en una melodía muy larga.
* **Aprendizaje de un estilo:** El modo `aprendido` estima la matriz contando las transiciones de una melodía real (*Himno a la alegría*, Beethoven).

## Matriz de transición de notas

```
          Do4     Re4     Mi4     Fa4    Sol4     La4     Si4     Do5
Do4      0.05    0.30    0.25    0.05    0.25    0.05    0.00    0.05
Re4      0.35    0.05    0.30    0.10    0.10    0.00    0.10    0.00
Mi4      0.15    0.25    0.05    0.25    0.25    0.05    0.00    0.00
Fa4      0.05    0.10    0.40    0.05    0.25    0.15    0.00    0.00
Sol4     0.15    0.05    0.20    0.15    0.05    0.20    0.05    0.15
La4      0.05    0.00    0.05    0.15    0.40    0.05    0.20    0.10
Si4      0.05    0.05    0.00    0.00    0.15    0.15    0.00    0.60
Do5      0.10    0.00    0.05    0.00    0.30    0.15    0.35    0.05
```

## Distribución del Proyecto
generador_melodias/
├── src/
│   ├── data.py       # Define los estados (notas y acordes), sus frecuencias, las matrices de transición y la melodía de referencia.
│   ├── model.py      # Contiene la clase CadenaMarkov (validación, distribución estacionaria, aprendizaje y generación) y la transformada inversa.
│   ├── audio.py      # Reproduce los tonos con winsound y exporta la melodía a un archivo .wav.
│   └── main.py       # Script principal: elige el modo, genera las transiciones, imprime cada nota y la hace sonar.
├── ejemplos/         # Melodías de ejemplo generadas por el programa (.wav).
├── .gitignore        # Excluye la caché de Python y los .wav generados en src.
└── requirements.txt  # Dependencias del entorno virtual (numpy).

## Ejecución

```bash
pip install -r requirements.txt
cd src
python main.py                          # 32 transiciones con la cadena de notas
python main.py --n 50 --semilla 10      # 50 transiciones reproducibles
python main.py --modo acordes --n 16    # progresión de acordes
python main.py --modo aprendido         # matriz aprendida del Himno a la alegría
python main.py --wav melodia.wav        # además guarda la melodía en .wav
```

> El sonido usa `winsound`, que viene incluido en Python para Windows. En otros sistemas el programa imprime la melodía y se puede escuchar con la opción `--wav`.
