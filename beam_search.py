from problem import VARIABLES, DOMAIN, count_violations


# ── Función de puntuación (heurística) ──────────────────────────────────────

def _score(assignment: dict) -> int:
    return -count_violations(assignment)


# ── Algoritmo principal ──────────────────────────────────────────────────────

def run_beam_search(k: int = 3) -> dict:
    # C inicia con una sola asignación vacía
    candidates: list[dict] = [{}]
    steps = 0

    for i, variable in enumerate(VARIABLES):
        steps += 1
        extended: list[dict] = []

        # ── Extend ──────────────────────────────────────────────────────────
        for x in candidates:
            for v in DOMAIN:
                new_x = dict(x)
                new_x[variable] = v
                extended.append(new_x)

        # ── Prune ───────────────────────────────────────────────────────────
        # Ordenar por score descendente y conservar los K mejores
        extended.sort(key=_score, reverse=True)
        candidates = extended[:k]

    # El mejor candidato al final es el primero (mayor score)
    best = candidates[0] if candidates else {}
    violations = count_violations(best)

    return {
        "assignment": best,
        "violations": violations,
        "found":      violations == 0,
        "k":          k,
        "steps":      steps,
    }


# ── Salida legible ───────────────────────────────────────────────────────────

def print_results(result: dict) -> None:
    print("\n" + "=" * 50)
    print(f"  BEAM SEARCH  (K = {result['k']})")
    print("=" * 50)

    if not result["assignment"]:
        print("  No se generó ningún candidato.")
        return

    status = "✓ VÁLIDA" if result["found"] else f"✗ INVÁLIDA"
    print(f"  Solución válida  : {status}")
    print(f"  Violaciones      : {result['violations']}")
    print(f"  Pasos ejecutados : {result['steps']}")

    print("\n  Asignación por servidor:")
    from problem import DOMAIN
    for server in DOMAIN:
        members = [m for m, s in result["assignment"].items() if s == server]
        print(f"    {server}: {members}")

    if not result["found"]:
        print("\n  NOTA: Beam Search no garantiza encontrar la solución")
        print(f"        óptima. Pruebe con un K mayor (actual K={result['k']}).")
