"""Motor de liquidación de nómina — reglas laborales colombianas 2024."""

# Constantes legales (Decreto 2655 de 2023 y Decreto 2871 de 2023)
SALARIO_MINIMO = 1_300_000.0
TOPE_AUXILIO_TRANSPORTE = 2 * SALARIO_MINIMO   # 2 SMLMV = 2.600.000
AUXILIO_TRANSPORTE = 162_000.0
RECARGO_DIURNO = 0.25
RECARGO_NOCTURNO = 0.75
DESCUENTO_SALUD = 0.04
DESCUENTO_PENSION = 0.04


class ErrorNomina(ValueError):
    """Excepción para datos de entrada inválidos en la liquidación."""


def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float,
) -> dict:
    """Liquida la nómina mensual de un trabajador.

    Args:
        salario_base: Salario base mensual en COP. Mínimo SMLMV (1.300.000).
        horas_extras_diurnas: Horas extra con recargo diurno del 25%.
        horas_extras_nocturnas: Horas extra con recargo nocturno del 75%.
        vlr_hora: Valor de la hora ordinaria en COP.

    Returns:
        dict con las siguientes llaves:
            - devengado (float): salario_base + valor horas extras
            - auxilio_transporte (float): 162.000 si aplica, 0 si no
            - descuento_salud (float): 4% sobre devengado
            - descuento_pension (float): 4% sobre devengado
            - total_descuentos (float): salud + pensión
            - neto_a_pagar (float): devengado + auxilio - descuentos

    Raises:
        ErrorNomina: Si salario_base < SMLMV o alguna hora es negativa.
    """
    # R5 — validaciones de entrada
    if salario_base < SALARIO_MINIMO:
        raise ErrorNomina(
            f"El salario_base ({salario_base:,.0f}) no puede ser menor "
            f"al SMLMV ({SALARIO_MINIMO:,.0f})."
        )
    if horas_extras_diurnas < 0 or horas_extras_nocturnas < 0:
        raise ErrorNomina("Las horas extras no pueden ser negativas.")

    # R1 — hora extra diurna: valor_hora * (1 + 25%)
    valor_he_diurnas = horas_extras_diurnas * vlr_hora * RECARGO_DIURNO  # BUG-1: falta el +1, paga solo el 25% en vez del 125%

    # R2 — hora extra nocturna: valor_hora * (1 + 75%)
    valor_he_nocturnas = horas_extras_nocturnas * vlr_hora * (1 + RECARGO_NOCTURNO)

    devengado = salario_base + valor_he_diurnas + valor_he_nocturnas

    # R4 — auxilio de transporte: solo si salario_base no supera 2 SMLMV
    auxilio = AUXILIO_TRANSPORTE if salario_base < TOPE_AUXILIO_TRANSPORTE else 0.0  # BUG-2: < en vez de <=, borde exacto 2.6M pierde auxilio

    # R3 — descuentos de ley: salud y pensión sobre devengado (no incluye auxilio)
    descuento_salud = (devengado + auxilio) * DESCUENTO_SALUD  # BUG-3: descuento incluye auxilio, la ley lo excluye
    descuento_pension = (devengado + auxilio) * DESCUENTO_PENSION
    total_descuentos = descuento_salud + descuento_pension

    neto_a_pagar = devengado + auxilio - total_descuentos

    return {
        "devengado": round(devengado, 2),
        "auxilio_transporte": round(auxilio, 2),
        "descuento_salud": round(descuento_salud, 2),
        "descuento_pension": round(descuento_pension, 2),
        "total_descuentos": round(total_descuentos, 2),
        "neto_a_pagar": round(neto_a_pagar, 2),
    }
