# Matriz de Casos de Prueba · Quality Guardian · Nómina Pro

Cada caso incluye entrada completa y salida esperada completa del dict.
El agente debe usar EXACTAMENTE estos valores al generar los tests pytest.

Fórmulas aplicadas:
- extra_diurna = horas_extras_diurnas * vlr_hora * 1.25
- extra_nocturna = horas_extras_nocturnas * vlr_hora * 1.75
- total_devengado = salario_base + extra_diurna + extra_nocturna
- auxilio_transporte = 162000 si salario_base <= 2600000, si no 0
- salud = total_devengado * 0.04
- pension = total_devengado * 0.04
- neto_pagar = total_devengado + auxilio_transporte - salud - pension

---

## CP-01 · Happy path básico sin extras

**Regla:** R3, R4

**Entrada:**
- salario_base: 1500000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 6250

**Salida esperada:**
- salario_base: 1500000
- extra_diurna: 0
- extra_nocturna: 0
- auxilio_transporte: 162000
- salud: 60000
- pension: 60000
- neto_pagar: 1542000

---

## CP-02 · Solo horas extras diurnas

**Regla:** R1, R3, R4

**Entrada:**
- salario_base: 2000000
- horas_extras_diurnas: 10
- horas_extras_nocturnas: 0
- vlr_hora: 8333

**Salida esperada:**
- salario_base: 2000000
- extra_diurna: 104162.5
- extra_nocturna: 0
- auxilio_transporte: 162000
- salud: 84166.5
- pension: 84166.5
- neto_pagar: 2097829.5

---

## CP-03 · Solo horas extras nocturnas

**Regla:** R2, R3, R4

**Entrada:**
- salario_base: 2000000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 8
- vlr_hora: 8333

**Salida esperada:**
- salario_base: 2000000
- extra_diurna: 0
- extra_nocturna: 116662.0
- auxilio_transporte: 162000
- salud: 84666.48
- pension: 84666.48
- neto_pagar: 2109329.04

---

## CP-04 · Horas extras mixtas diurnas y nocturnas

**Regla:** R1, R2, R3, R4

**Entrada:**
- salario_base: 1800000
- horas_extras_diurnas: 5
- horas_extras_nocturnas: 3
- vlr_hora: 7500

**Salida esperada:**
- salario_base: 1800000
- extra_diurna: 46875
- extra_nocturna: 39375
- auxilio_transporte: 162000
- salud: 75450
- pension: 75450
- neto_pagar: 1897350

---

## CP-05 · Caso límite auxilio de transporte — salario exacto 2600000

**Regla:** R4 (límite inclusivo)

**Entrada:**
- salario_base: 2600000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 10833

**Salida esperada:**
- salario_base: 2600000
- extra_diurna: 0
- extra_nocturna: 0
- auxilio_transporte: 162000
- salud: 104000
- pension: 104000
- neto_pagar: 2554000

---

## CP-06 · Salario por encima del umbral — sin auxilio

**Regla:** R4 (no aplica)

**Entrada:**
- salario_base: 2600001
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 10833

**Salida esperada:**
- salario_base: 2600001
- extra_diurna: 0
- extra_nocturna: 0
- auxilio_transporte: 0
- salud: 104000.04
- pension: 104000.04
- neto_pagar: 2392000.92

---

## CP-07 · Verificación exacta del descuento de salud

**Regla:** R3

**Entrada:**
- salario_base: 1500000
- horas_extras_diurnas: 4
- horas_extras_nocturnas: 0
- vlr_hora: 6250

**Salida esperada:**
- salario_base: 1500000
- extra_diurna: 31250
- extra_nocturna: 0
- auxilio_transporte: 162000
- salud: 61250
- pension: 61250
- neto_pagar: 1570750.0

---

## CP-08 · Excepción por horas negativas

**Regla:** R5

**Entrada:**
- salario_base: 1500000
- horas_extras_diurnas: -5
- horas_extras_nocturnas: 0
- vlr_hora: 6250

**Salida esperada:**
- Lanza ValueError

---

## CP-09 · Excepción por salario menor al mínimo

**Regla:** R5

**Entrada:**
- salario_base: 1200000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 5000

**Salida esperada:**
- Lanza ValueError

---

## CP-10 · Salario exactamente en el mínimo permitido

**Regla:** R5 (borde inferior válido)

**Entrada:**
- salario_base: 1300000
- horas_extras_diurnas: 0
- horas_extras_nocturnas: 0
- vlr_hora: 5416

**Salida esperada:**
- salario_base: 1300000
- extra_diurna: 0
- extra_nocturna: 0
- auxilio_transporte: 162000
- salud: 52000
- pension: 52000
- neto_pagar: 1358000.0
