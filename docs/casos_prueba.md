# Matriz de Casos de Prueba · Quality Guardian · Nómina Pro

Cada caso incluye: entrada, salida esperada y la regla de negocio que valida.
El agente debe generar un test de pytest por cada caso.

---

## CP-01 · Happy path básico sin extras (R3, R4)

**Regla:** R3 (seguridad social) · R4 (auxilio de transporte)

**Entrada:**
- salario_base: 1_500_000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 6_250

**Salida esperada:**
- total_devengado: 1_500_000
- descuento_salud: 60_000  (4% de 1_500_000)
- descuento_pension: 60_000  (4% de 1_500_000)
- auxilio_transporte: 162_000  (aplica porque salario_base <= 2_600_000)
- total_a_pagar: 1_542_000

---

## CP-02 · Solo horas extras diurnas (R1)

**Regla:** R1 (recargo diurno 25%)

**Entrada:**
- salario_base: 2_000_000
- horas_extras_diurnas: 10
- horas_extras_nocturnas: 0
- vlr_hora: 8_333

**Salida esperada:**
- extras_diurnas: 10 * 8_333 * 1.25 = 104_162.5
- total_devengado: 2_104_162.5

---

## CP-03 · Solo horas extras nocturnas (R2)

**Regla:** R2 (recargo nocturno 75%)

**Entrada:**
- salario_base: 2_000_000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 8
- vlr_hora: 8_333

**Salida esperada:**
- extras_nocturnas: 8 * 8_333 * 1.75 = 116_662
- total_devengado: 2_116_662

---

## CP-04 · Horas extras mixtas — diurnas y nocturnas (R1 + R2) ⬅ caso propio célula

**Regla:** R1 + R2 combinadas

**Entrada:**
- salario_base: 1_800_000
- horas_extras_diurnas: 5
- horas_extras_nocturnas: 3
- vlr_hora: 7_500

**Salida esperada:**
- extras_diurnas: 5 * 7_500 * 1.25 = 46_875
- extras_nocturnas: 3 * 7_500 * 1.75 = 39_375
- total_devengado: 1_886_250
- descuento_salud: 75_450  (4% de 1_886_250)
- descuento_pension: 75_450
- auxilio_transporte: 162_000
- total_a_pagar: 1_897_350

---

## CP-05 · Caso límite auxilio de transporte — salario exacto $2.600.000 (R4)

**Regla:** R4 (umbral exacto del auxilio)

**Entrada:**
- salario_base: 2_600_000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 10_833

**Salida esperada:**
- auxilio_transporte: 162_000  (aplica porque salario_base <= 2_600_000, el límite es inclusivo)
- total_devengado: 2_600_000

---

## CP-06 · Salario por encima del umbral — sin auxilio de transporte (R4)

**Regla:** R4 (no aplica auxilio)

**Entrada:**
- salario_base: 2_600_001
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 10_833

**Salida esperada:**
- auxilio_transporte: 0  (salario_base > 2_600_000, no aplica)

---

## CP-07 · Verificación exacta del descuento de salud (R3)

**Regla:** R3 (4% salud sobre total devengado incluyendo extras)

**Entrada:**
- salario_base: 1_500_000
- horas_extras_diurnas: 4
- horas_extras_nocturnas: 0
- vlr_hora: 6_250

**Salida esperada:**
- extras_diurnas: 4 * 6_250 * 1.25 = 31_250
- total_devengado: 1_531_250
- descuento_salud: 61_250  (exactamente 4% de 1_531_250)

---

## CP-08 · Excepción por horas negativas (R5)

**Regla:** R5 (validación de entradas)

**Entrada:**
- salario_base: 1_500_000
- horas_extras_diurnas: -5
- horas_extras_nocturnas: 0
- vlr_hora: 6_250

**Salida esperada:**
- Lanza excepción con mensaje claro indicando que las horas no pueden ser negativas

---

## CP-09 · Excepción por salario menor al mínimo (R5)

**Regla:** R5 (salario_base < $1.300.000)

**Entrada:**
- salario_base: 1_200_000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 5_000

**Salida esperada:**
- Lanza excepción con mensaje claro indicando que el salario es menor al mínimo permitido

---

## CP-10 · Salario exactamente en el mínimo permitido — sin excepción (R5) ⬅ caso propio célula

**Regla:** R5 (borde inferior, debe funcionar sin error)

**Entrada:**
- salario_base: 1_300_000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 5_416

**Salida esperada:**
- No lanza excepción
- auxilio_transporte: 162_000  (aplica porque 1_300_000 <= 2_600_000)
- descuento_salud: 52_000  (4% de 1_300_000)
- descuento_pension: 52_000
