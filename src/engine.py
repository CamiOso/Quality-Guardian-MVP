"""Motor de liquidación de nómina — reglas laborales colombianas 2024."""

from typing import Dict


def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float,
) -> Dict[str, float]:
    """Liquida la nómina mensual de un trabajador según la legislación colombiana.

    Reglas aplicadas:
        R1 (CST art. 168): Hora extra diurna = vlr_hora * 1.25 (recargo del 25%).
        R2 (CST art. 168): Hora extra nocturna = vlr_hora * 1.75 (recargo del 75%).
        R3 (Ley 100/1993): Descuento del 4% para salud y 4% para pensión
            calculados sobre el total_devengado (salario_base + extras).
        R4 (Decreto 2871/2023): Auxilio de transporte de $162.000 cuando
            salario_base <= $2.600.000 (2 SMLMV).
        R5 (CST art. 145): salario_base no puede ser menor al SMLMV ($1.300.000).
            Ninguna cantidad de horas puede ser negativa.

    Args:
        salario_base: Salario base mensual en COP. Mínimo $1.300.000 (SMLMV 2024).
        horas_extras_diurnas: Cantidad de horas extra con recargo diurno (>= 0).
        horas_extras_nocturnas: Cantidad de horas extra con recargo nocturno (>= 0).
        vlr_hora: Valor de la hora ordinaria en COP.

    Returns:
        Diccionario con el desglose completo de la liquidación:
            - salario_base (float): Salario base ingresado.
            - extra_diurna (float): Valor total de horas extras diurnas.
            - extra_nocturna (float): Valor total de horas extras nocturnas.
            - auxilio_transporte (float): $162.000 si aplica, $0 si no.
            - salud (float): Descuento del 4% sobre total_devengado.
            - pension (float): Descuento del 4% sobre total_devengado.
            - neto_pagar (float): Monto final a pagar al trabajador.

    Raises:
        ValueError: Si salario_base < 1.300.000 o alguna hora es negativa.
    """
    # R5 — validación de salario mínimo legal
    if salario_base < 1_300_000:
        raise ValueError(
            f"El salario_base ({salario_base:,.0f}) no puede ser menor "
            "al SMLMV vigente de $1.300.000."
        )

    # R5 — validación de horas no negativas
    if horas_extras_diurnas < 0 or horas_extras_nocturnas < 0:
        raise ValueError(
            "Las horas extras no pueden ser negativas. "
            f"Recibido: diurnas={horas_extras_diurnas}, nocturnas={horas_extras_nocturnas}."
        )

    # R1 — hora extra diurna: vlr_hora * 1.25
    extra_diurna = horas_extras_diurnas * vlr_hora * 1.25

    # R2 — hora extra nocturna: vlr_hora * 1.75
    extra_nocturna = horas_extras_nocturnas * vlr_hora * 1.75

    # Base para calcular descuentos de seguridad social (no incluye auxilio)
    total_devengado = salario_base + extra_diurna + extra_nocturna

    # R4 — auxilio de transporte: aplica si salario_base <= 2 SMLMV
    auxilio_transporte = 162_000.0 if salario_base <= 2_600_000 else 0.0

    # R3 — descuentos de seguridad social sobre total_devengado
    salud = total_devengado * 0.04
    pension = total_devengado * 0.04

    neto_pagar = total_devengado + auxilio_transporte - salud - pension

    return {
        "salario_base": round(salario_base, 2),
        "extra_diurna": round(extra_diurna, 2),
        "extra_nocturna": round(extra_nocturna, 2),
        "auxilio_transporte": round(auxilio_transporte, 2),
        "salud": round(salud, 2),
        "pension": round(pension, 2),
        "neto_pagar": round(neto_pagar, 2),
    }
