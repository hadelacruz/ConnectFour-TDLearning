from backtracking import run_backtracking, print_results as bt_print
from beam_search   import run_beam_search,   print_results as bs_print
from local_search  import run_local_search,  print_results as ls_print
from benchmarking  import run_benchmark


# ── Configuración 
BEAM_K          = 3     
ICM_MAX_ITER    = 100   
ICM_SEED        = 42    


def print_header(title: str) -> None:
    width = 60
    print("\n" + "█" * width)
    padding = (width - len(title) - 2) // 2
    print("█" + " " * padding + title + " " * (width - padding - len(title) - 2) + "█")
    print("█" * width)


# ── Task 2.1 — Backtracking Search ───────────────────────────────────────────
def task_2_1() -> None:
    print_header("BACKTRACKING SEARCH")
    print("\n  Descripción:")
    print("  Algoritmo exacto con Forward Checking (Lookahead).")
    print("  Garantiza encontrar una asignación válida (Weight = 1).")
    print("  Usa heurística MRV para elegir la próxima variable.\n")

    result = run_backtracking()
    bt_print(result)


# ── Task 2.2 — Beam Search ───────────────────────────────────────────────────
def task_2_2() -> None:
    print_header("BEAM SEARCH")
    print("\n  Descripción:")
    print(f"  Algoritmo aproximado con K = {BEAM_K} candidatos simultáneos.")
    print("  Heurística de prune: menor número de restricciones violadas.")
    print("  No garantiza encontrar la asignación de peso máximo.\n")

    # Ejecutar con distintos valores de K para mostrar el tradeoff
    for k in [1, BEAM_K, 10]:
        result = run_beam_search(k=k)
        bs_print(result)


# ── Task 2.3 — Local Search (ICM) ────────────────────────────────────────────
def task_2_3() -> None:
    print_header("LOCAL SEARCH (ICM)")
    print("\n  Descripción:")
    print("  Búsqueda local mediante Modos Condicionales Iterados.")
    print("  Inicia con asignación aleatoria y mejora iterativamente.")
    print(f"  Límite: {ICM_MAX_ITER} iteraciones. Semilla: {ICM_SEED}.\n")

    result = run_local_search(max_iterations=ICM_MAX_ITER, seed=ICM_SEED)
    ls_print(result)


# ── Task 2.4 — Benchmarking y Conclusiones ───────────────────────────────────
def task_2_4() -> None:
    print_header("BENCHMARKING Y CONCLUSIONES")
    run_benchmark(
        beam_k       = BEAM_K,
        icm_max_iter = ICM_MAX_ITER,
        icm_seed     = ICM_SEED,
    )


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    print("\n" + "=" * 60)
    print("  CSP: DESPLIEGUE DE MICROSERVICIOS")
    print("=" * 60)
    print("\n  Problema:")
    print("  • 8 microservicios (M1–M8) → 3 servidores (S1, S2, S3)")
    print("  • Capacidad máxima: 3 microservicios por servidor")
    print("  • Anti-afinidad: (M1,M2), (M3,M4), (M5,M6), (M1,M5)")

    task_2_1()
    task_2_2()
    task_2_3()
    task_2_4()


if __name__ == "__main__":
    main()
