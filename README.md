# Connect Four - TD Learning

Implementación de algoritmos de búsqueda para resolver problemas de satisfacción de restricciones (CSP).

## Descripción

Este proyecto implementa tres algoritmos de búsqueda para asignar microservicios a servidores con restricciones de anti-afinidad y capacidad máxima:

## Uso

```bash
python main.py
```


- **Backtracking Search**: Algoritmo exacto con Forward Checking. Garantiza encontrar una solución válida.
- **Beam Search**: Algoritmo aproximado que mantiene K candidatos simultáneamente. Más rápido pero no garantiza optimalidad.
- **Local Search (ICM)**: Búsqueda local iterativa. Comienza con asignación aleatoria y mejora incrementalmente.

## Archivos

- `main.py`: Punto de entrada. Ejecuta todos los algoritmos y benchmarks.
- `problem.py`: Define variables, dominios, restricciones y funciones de evaluación.
- `backtracking.py`: Implementación del algoritmo de backtracking con lookahead.
- `beam_search.py`: Implementación del algoritmo de beam search.
- `local_search.py`: Implementación de búsqueda local con movimientos aleatorios.
- `benchmarking.py`: Comparación de rendimiento entre algoritmos.


## Restricciones

- 8 microservicios (M1-M8) a distribuir en 3 servidores (S1-S3)
- Capacidad máxima de 3 microservicios por servidor
- Pares de anti-afinidad que no pueden asignarse al mismo servidor
