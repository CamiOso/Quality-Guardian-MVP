"""Motor de liquidación de nómina — versión con 3 bugs deliberados para demo QA."""

from typing import Dict


def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float,
) -> Dict[str, float]:
    """Liquida la nómina mensual de un trabajador según la legislación colombiana.

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
    if salario_base < 1_300_000:
        raise ValueError(
            f"El salario_base ({salario_base:,.0f}) no puede ser menor "
            "al SMLMV vigente de $1.300.000."
        )

    if horas_extras_diurnas < 0 or horas_extras_nocturnas < 0:
        raise ValueError(
            "Las horas extras no pueden ser negativas. "
            f"Recibido: diurnas={horas_extras_diurnas}, nocturnas={horas_extras_nocturnas}."
        )

    # BUG 1 (R1): recargo diurno incorrecto — 1.20 en lugar de 1.25
    extra_diurna = horas_extras_diurnas * vlr_hora * 1.20

    # R2 correcto
    extra_nocturna = horas_extras_nocturnas * vlr_hora * 1.75

    total_devengado = salario_base + extra_diurna + extra_nocturna

    # BUG 2 (R4): frontera exclusiva — salario exacto 2.600.000 pierde el auxilio
    auxilio_transporte = 162_000.0 if salario_base < 2_600_000 else 0.0

    # BUG 3 (R3): tasa 3% en lugar del 4% legal
    salud = total_devengado * 0.03
    pension = total_devengado * 0.03

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
