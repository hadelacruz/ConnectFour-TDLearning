
import random
from problem import VARIABLES, DOMAIN, count_violations


# ── Heurística de peso para ICM ──────────────────────────────────────────────

def _weight(assignment: dict) -> int:
    return -count_violations(assignment)


# ── Asignación inicial aleatoria ─────────────────────────────────────────────

def _random_assignment(seed: int | None = None) -> dict:
    rng = random.Random(seed)
    return {v: rng.choice(DOMAIN) for v in VARIABLES}


# ── Algoritmo ICM ────────────────────────────────────────────────────────────

def run_local_search(max_iterations: int = 100,
                     seed: int | None = None) -> dict:
    # Paso 1: asignación inicial aleatoria
    x = _random_assignment(seed)
    initial = dict(x)
    initial_violations = count_violations(initial)

    iteration    = 0
    converged    = False

    # Historial de pesos para detectar convergencia
    prev_weight = _weight(x)

    for iteration in range(1, max_iterations + 1):
        improved = False

        # Paso 2: iterar por cada variable Xi
        for variable in VARIABLES:
            best_val    = x[variable]   # valor actual como referencia
            best_weight = _weight(x)

            # Probar cada valor del dominio
            for v in DOMAIN:
                candidate = dict(x)
                candidate[variable] = v
                w = _weight(candidate)

                if w > best_weight:
                    best_weight = w
                    best_val    = v

            # x ← xv con el peso mayor
            if best_val != x[variable]:
                x[variable] = best_val
                improved = True

        current_weight = _weight(x)

        # Verificar convergencia: sin cambios en esta iteración completa
        if not improved or current_weight == 0:   # 0 violaciones = óptimo global
            converged = True
            break

        prev_weight = current_weight

    violations = count_violations(x)

    return {
        "assignment":          x,
        "violations":          violations,
        "found":               violations == 0,
        "iterations":          iteration,
        "initial":             initial,
        "initial_violations":  initial_violations,
        "converged":           converged,
        "max_iterations":      max_iterations,
    }


# ── Salida legible ───────────────────────────────────────────────────────────

def print_results(result: dict) -> None:
    print("\n" + "=" * 50)
    print("  LOCAL SEARCH — ICM (Iterated Conditional Modes)")
    print("=" * 50)

    print(f"\n  Asignación inicial (aleatoria):")
    from problem import DOMAIN
    for server in DOMAIN:
        members = [m for m, s in result["initial"].items() if s == server]
        print(f"    {server}: {members}")
    print(f"  Violaciones iniciales : {result['initial_violations']}")

    print(f"\n  Resultado tras ICM:")
    status = "✓ VÁLIDA" if result["found"] else "✗ INVÁLIDA (óptimo local)"
    print(f"  Solución válida  : {status}")
    print(f"  Violaciones      : {result['violations']}")

    conv_str = "Sí (antes del límite)" if result["converged"] else f"No (límite {result['max_iterations']} alcanzado)"
    print(f"  Convergió        : {conv_str}")
    print(f"  Iteraciones      : {result['iterations']}")

    print("\n  Asignación final por servidor:")
    for server in DOMAIN:
        members = [m for m, s in result["assignment"].items() if s == server]
        print(f"    {server}: {members}")

    if not result["found"]:
        print("\n  NOTA: ICM quedó en un óptimo local.")
        print("        Intente con una semilla diferente o más iteraciones.")
