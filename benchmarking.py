import time
from backtracking import run_backtracking
from beam_search   import run_beam_search
from local_search  import run_local_search
from problem       import DOMAIN, count_violations


# ── Utilidades ───────────────────────────────────────────────────────────────

def _server_layout(assignment: dict) -> str:
    parts = []
    for server in DOMAIN:
        members = [m for m, s in assignment.items() if s == server]
        parts.append(f"{server}:{members}")
    return "  |  ".join(parts)


# ── Benchmark individual ─────────────────────────────────────────────────────

def _bench_backtracking() -> dict:
    start  = time.perf_counter()
    result = run_backtracking()
    elapsed = time.perf_counter() - start
    result["time"] = elapsed
    return result


def _bench_beam(k: int) -> dict:
    start  = time.perf_counter()
    result = run_beam_search(k=k)
    elapsed = time.perf_counter() - start
    result["time"] = elapsed
    return result


def _bench_local(max_iterations: int = 100, seed: int | None = 42) -> dict:
    start  = time.perf_counter()
    result = run_local_search(max_iterations=max_iterations, seed=seed)
    elapsed = time.perf_counter() - start
    result["time"] = elapsed
    return result


# ── Reporte comparativo ──────────────────────────────────────────────────────

def _print_separator(char: str = "─", width: int = 70) -> None:
    print(char * width)


def run_benchmark(beam_k: int = 3,
                  icm_max_iter: int = 100,
                  icm_seed: int = 42) -> None:
    print("\n")
    _print_separator("═")
    print("   TASK 2.4 — BENCHMARKING Y CONCLUSIONES")
    print("   CSP: Despliegue de 8 Microservicios en 3 Servidores")
    _print_separator("═")

    # ── Ejecutar los tres algoritmos ─────────────────────────────────────────
    print("\n  Ejecutando algoritmos…")

    bt  = _bench_backtracking()
    bs  = _bench_beam(k=beam_k)
    ls  = _bench_local(max_iterations=icm_max_iter, seed=icm_seed)

    # ── Tabla comparativa ────────────────────────────────────────────────────
    print()
    _print_separator()
    print(f"  {'Algoritmo':<30} {'¿Válida?':<12} {'Violaciones':<14} {'Tiempo (s)':<14}")
    _print_separator()

    def row(name, found, violations, elapsed):
        valid_str = "✓  SÍ" if found else "✗  NO"
        print(f"  {name:<30} {valid_str:<12} {violations:<14} {elapsed:.6f}")

    row(f"Backtracking (Forward Check)",
        bt["found"], count_violations(bt["assignment"]) if bt["assignment"] else "N/A", bt["time"])

    row(f"Beam Search (K={beam_k})",
        bs["found"], bs["violations"], bs["time"])

    row(f"Local Search ICM (max={icm_max_iter} iter)",
        ls["found"], ls["violations"], ls["time"])

    _print_separator()

    # ── Detalle por algoritmo ────────────────────────────────────────────────
    print("\n  ── Detalle de asignaciones ─────────────────────────────────────")

    print(f"\n  [Backtracking]  nodos explorados: {bt['nodes_explored']}")
    if bt["assignment"]:
        print(f"  {_server_layout(bt['assignment'])}")
    else:
        print("  Sin solución.")

    print(f"\n  [Beam Search K={beam_k}]")
    if bs["assignment"]:
        print(f"  {_server_layout(bs['assignment'])}")
        if not bs["found"]:
            print(f"  ⚠  Atascado con {bs['violations']} violación/es. Pruebe K mayor.")
    else:
        print("  Sin candidatos.")

    print(f"\n  [Local Search ICM]  iteraciones: {ls['iterations']}")
    if ls["assignment"]:
        print(f"  Inicial  → violaciones: {ls['initial_violations']}")
        print(f"  Final    → {_server_layout(ls['assignment'])}")
        if not ls["found"]:
            print(f"  ⚠  Óptimo local con {ls['violations']} violación/es.")

    # ── Análisis y conclusiones ───────────────────────────────────────────────
    print()
    _print_separator()
    print("  ANÁLISIS Y CONCLUSIONES")
    _print_separator()

    conclusiones = f"""
  Resultados empíricos vs. predicción teórica:

  1. EXACTITUD
     • Backtracking encontró solución válida : {'SÍ' if bt['found'] else 'NO'}
       → Confirma la teoría: Backtracking es EXACTO (garantiza la solución
         si existe, usando Forward Checking para podar ramas inútiles).

     • Beam Search (K={beam_k}) encontró solución válida : {'SÍ' if bs['found'] else 'NO'}
       → {'Confirma' if not bs['found'] else 'En este caso'} la teoría: Beam Search es APROXIMADO; con K pequeño
         puede descartar el camino correcto al podar candidatos.
         (K=1=greedy, K=∞=BFS completo).

     • Local Search ICM encontró solución válida : {'SÍ' if ls['found'] else 'NO'}
       → {'Confirma' if not ls['found'] else 'En este caso'} la teoría: ICM es APROXIMADO y puede quedar
         atrapado en óptimos locales. El peso (nº de restricciones
         satisfechas) nunca decrece entre iteraciones, lo que garantiza
         convergencia pero NO optimalidad global.

  2. VELOCIDAD
     • Backtracking : {bt['time']:.6f} s  (complejidad exponencial O(b^n))
     • Beam Search  : {bs['time']:.6f} s  (complejidad lineal  O(K·n·b))
     • Local Search : {ls['time']:.6f} s  (complejidad lineal  O(iter·n·b))

     Para este problema pequeño (n=8 variables, b=3 valores) la diferencia
     de tiempo es mínima porque el espacio de búsqueda es manejable.
     En problemas más grandes (n≫8), la brecha exponencial/lineal se hace
     dramáticamente evidente: Backtracking escalaría mal mientras que
     Beam Search e ICM permanecerían rápidos.

  3. TRADEOFF EFICIENCIA vs. EXACTITUD (diapositiva 9 del PDF)
     • Solo Backtracking GARANTIZA encontrar la asignación óptima (Weight=1).
     • Beam Search y ICM sacrifican exactitud por velocidad.
     • En aplicaciones reales de despliegue de microservicios donde el
       número de servicios y restricciones crece, los algoritmos aproximados
       son preferibles por su escalabilidad lineal, aceptando el riesgo
       de soluciones sub-óptimas.
"""
    print(conclusiones)
    _print_separator("═")
