import copy
from problem import VARIABLES, DOMAIN, delta, count_violations


# ── Estado global del algoritmo ─────────────────────────────────────────────
_best_assignment: dict | None = None
_best_weight:     int         = -1
_nodes_explored:  int         = 0


def _reset_state() -> None:
    global _best_assignment, _best_weight, _nodes_explored
    _best_assignment = None
    _best_weight     = -1
    _nodes_explored  = 0


# ── Forward Checking (Lookahead) ────────────────────────────────────────────

def _lookahead(assignment: dict, variable: str, value: str,
               domains: dict) -> dict | None:
    new_domains = copy.deepcopy(domains)
    extended    = dict(assignment)
    extended[variable] = value

    for var in VARIABLES:
        if var in extended:          # ya asignada, ignorar
            continue
        new_dom = []
        for val in new_domains[var]:
            if delta(extended, var, val) != 0:
                new_dom.append(val)
        if not new_dom:              # dominio vacío → backtrack
            return None
        new_domains[var] = new_dom

    return new_domains


# ── Selección de variable (MRV: Minimum Remaining Values) ──────────────────

def _choose_variable(assignment: dict, domains: dict) -> str:
    unassigned = [v for v in VARIABLES if v not in assignment]
    return min(unassigned, key=lambda v: len(domains[v]))


# ── Algoritmo principal ─────────────────────────────────────────────────────

def _backtrack(assignment: dict, weight: int, domains: dict) -> None:
    global _best_assignment, _best_weight, _nodes_explored

    _nodes_explored += 1

    # Caso base: asignación completa
    if len(assignment) == len(VARIABLES):
        if weight > _best_weight:
            _best_weight     = weight
            _best_assignment = dict(assignment)
        return

    # Elegir variable
    xi = _choose_variable(assignment, domains)

    # Iterar sobre los valores del dominio de Xi
    for v in domains[xi]:

        # δ = producto de factores activos (binario: 1 o 0)
        d = delta(assignment, xi, v)
        if d == 0:
            continue                  # poda: restricción violada

        # Lookahead (Forward Checking)
        new_domains = _lookahead(assignment, xi, v, domains)
        if new_domains is None:
            continue                  # dominio futuro vacío → poda

        # Recursión
        assignment[xi] = v
        _backtrack(assignment, weight * d, new_domains)
        del assignment[xi]

        # Optimización: si ya encontramos peso = 1 (solución perfecta), parar
        if _best_weight == 1:
            return


def run_backtracking() -> dict:
    _reset_state()

    # Dominios iniciales: todos los servidores disponibles para cada variable
    initial_domains = {v: list(DOMAIN) for v in VARIABLES}

    _backtrack({}, 1, initial_domains)

    return {
        "assignment":     _best_assignment,
        "weight":         _best_weight,
        "nodes_explored": _nodes_explored,
        "found":          _best_weight == 1,
    }


# ── Salida legible ───────────────────────────────────────────────────────────

def print_results(result: dict) -> None:
    print("\n" + "=" * 50)
    print("  BACKTRACKING SEARCH (con Forward Checking)")
    print("=" * 50)

    if result["assignment"] is None:
        print("  No se encontró ninguna solución.")
        return

    status = "✓ VÁLIDA" if result["found"] else "✗ INVÁLIDA"
    print(f"  Solución válida  : {status}")
    print(f"  Nodos explorados : {result['nodes_explored']}")
    print(f"  Peso final       : {result['weight']}")
    print("\n  Asignación por servidor:")
    from problem import DOMAIN
    for server in DOMAIN:
        members = [m for m, s in result["assignment"].items() if s == server]
        print(f"    {server}: {members}")

    violations = count_violations(result["assignment"])
    print(f"\n  Violaciones      : {violations}")
