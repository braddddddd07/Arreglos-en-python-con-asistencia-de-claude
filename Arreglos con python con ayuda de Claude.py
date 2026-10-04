"""
ADA2 - Arreglos e Infografía
Matriz de calificaciones: alumnos x materias.

Compara dos organizaciones de la misma matriz:
  A) filas = alumnos,  columnas = materias   -> matriz[alumno][materia]
  B) filas = materias, columnas = alumnos    -> matriz[materia][alumno]

Tres pruebas:
  1. Acceso directo por índice (O(1))
  2. Búsqueda secuencial de (alumno 321, materia 5) recorriendo la matriz
  3. Recorrido completo sumando todas las calificaciones
"""
import random
import time

ALUMNO_BUSCADO = 321
MATERIA_BUSCADA = 5


def generar_a(n_alumnos, n_materias):
    """Layout A: matriz[alumno][materia]. Calificaciones aleatorias 0-100."""
    return [[random.randint(0, 100) for _ in range(n_materias)]
            for _ in range(n_alumnos)]


def transponer(m):
    """Layout B a partir de A, para que ambos tengan EXACTAMENTE los mismos datos."""
    return [list(col) for col in zip(*m)]


# ---------- Búsqueda secuencial ----------
def buscar_a(m, alumno, materia):
    """Recorre por alumnos (filas) y dentro de cada uno por materias (columnas)."""
    pasos = 0
    for i, fila in enumerate(m, start=1):
        for j, valor in enumerate(fila, start=1):
            pasos += 1
            if i == alumno and j == materia:
                return valor, pasos
    return None, pasos


def buscar_b(m, alumno, materia):
    """Recorre por materias (filas) y dentro de cada una por alumnos (columnas)."""
    pasos = 0
    for j, fila in enumerate(m, start=1):
        for i, valor in enumerate(fila, start=1):
            pasos += 1
            if i == alumno and j == materia:
                return valor, pasos
    return None, pasos


# ---------- Recorrido completo ----------
def suma_a(m):
    total = 0
    for fila in m:
        for v in fila:
            total += v
    return total


def suma_b(m):
    total = 0
    for fila in m:
        for v in fila:
            total += v
    return total


def medir(func, *args, repeticiones=1):
    t0 = time.perf_counter()
    for _ in range(repeticiones):
        resultado = func(*args)
    return (time.perf_counter() - t0) / repeticiones, resultado


def demo_500x6():
    print("=== DEMO: 500 alumnos x 6 materias ===")
    a = generar_a(500, 6)
    b = transponer(a)
    print(f"Acceso directo A[alumno {ALUMNO_BUSCADO}][materia {MATERIA_BUSCADA}] = "
          f"{a[ALUMNO_BUSCADO-1][MATERIA_BUSCADA-1]}")
    print(f"Acceso directo B[materia {MATERIA_BUSCADA}][alumno {ALUMNO_BUSCADO}] = "
          f"{b[MATERIA_BUSCADA-1][ALUMNO_BUSCADO-1]}")
    va, pa = buscar_a(a, ALUMNO_BUSCADO, MATERIA_BUSCADA)
    vb, pb = buscar_b(b, ALUMNO_BUSCADO, MATERIA_BUSCADA)
    print(f"Búsqueda secuencial A: valor={va}, pasos={pa}")
    print(f"Búsqueda secuencial B: valor={vb}, pasos={pb}\n")


def benchmark(casos):
    print(f"{'Alumnos':>8} {'Materias':>9} | {'Pasos A':>10} {'Pasos B':>10} | "
          f"{'Busq A (ms)':>12} {'Busq B (ms)':>12} | {'Suma A (ms)':>12} {'Suma B (ms)':>12}")
    print("-" * 105)
    filas = []
    for n_al, n_mat in casos:
        a = generar_a(n_al, n_mat)
        b = transponer(a)
        reps = 20 if n_al * n_mat < 200_000 else 3
        ta, (va, pa) = medir(buscar_a, a, ALUMNO_BUSCADO, MATERIA_BUSCADA, repeticiones=reps)
        tb, (vb, pb) = medir(buscar_b, b, ALUMNO_BUSCADO, MATERIA_BUSCADA, repeticiones=reps)
        assert va == vb  # misma celda en ambos layouts
        sa, _ = medir(suma_a, a, repeticiones=reps)
        sb, _ = medir(suma_b, b, repeticiones=reps)
        filas.append((n_al, n_mat, pa, pb, ta*1e3, tb*1e3, sa*1e3, sb*1e3))
        print(f"{n_al:>8} {n_mat:>9} | {pa:>10} {pb:>10} | "
              f"{ta*1e3:>12.4f} {tb*1e3:>12.4f} | {sa*1e3:>12.3f} {sb*1e3:>12.3f}")
    return filas


if __name__ == "__main__":
    random.seed(42)
    demo_500x6()
    # Combinaciones de 1000/10000/100000 alumnos con 100/500/10000 materias.
    # Se omiten las que superan ~10 millones de celdas (listas de Python de
    # 1e9 enteros no caben en memoria de una laptop normal).
    alumnos = [1000, 10000, 100000]
    materias = [100, 500, 10000]
    casos = [(n, m) for n in alumnos for m in materias if n * m <= 10_000_000]
    benchmark(casos)
