# ── Variables y dominios ────────────────────────────────────────────────────
VARIABLES = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
DOMAIN    = ["S1", "S2", "S3"]
MAX_CAPACITY = 3          # máximo de microservicios por servidor

# ── Pares de anti-afinidad ──────────────────────────────────────────────────
ANTI_AFFINITY_PAIRS = [
    ("M1", "M2"),
    ("M3", "M4"),
    ("M5", "M6"),
    ("M1", "M5"),
]


# ── Funciones de evaluación de restricciones ────────────────────────────────

def count_violations(assignment: dict) -> int:
    violations = 0

    # Anti-afinidad
    for (mi, mj) in ANTI_AFFINITY_PAIRS:
        if mi in assignment and mj in assignment:
            if assignment[mi] == assignment[mj]:
                violations += 1

    # Capacidad
    server_counts = {}
    for server in assignment.values():
        server_counts[server] = server_counts.get(server, 0) + 1
    for cnt in server_counts.values():
        if cnt > MAX_CAPACITY:
            violations += 1          # una violación por servidor sobre-cargado

    return violations


def is_valid(assignment: dict) -> bool:
    """Retorna True si la asignación completa no viola ninguna restricción."""
    if len(assignment) != len(VARIABLES):
        return False
    return count_violations(assignment) == 0


def delta(assignment: dict, variable: str, value: str) -> int:
    test = dict(assignment)
    test[variable] = value

    # Anti-afinidad: verificar pares donde 'variable' participa
    for (mi, mj) in ANTI_AFFINITY_PAIRS:
        if variable in (mi, mj):
            other = mj if variable == mi else mi
            if other in test and test[other] == value:
                return 0

    # Capacidad: contar microservicios en el servidor elegido
    count = sum(1 for v in test.values() if v == value)
    if count > MAX_CAPACITY:
        return 0

    return 1


def print_assignment(assignment: dict, label: str = "Asignación") -> None:
    """Imprime la asignación de forma legible."""
    print(f"\n{label}:")
    for server in DOMAIN:
        members = [m for m, s in assignment.items() if s == server]
        print(f"  {server}: {members}")
    violations = count_violations(assignment)
    valid      = "✓ VÁLIDA" if violations == 0 else f"✗ INVÁLIDA ({violations} violación/es)"
    print(f"  Estado: {valid}")
