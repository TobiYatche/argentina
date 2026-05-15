# Research Agent

Actuá como agente de investigación para el paquete `argentina`.

Leé:
- AGENT_CONTEXT.md
- ROADMAP.md
- README.md
- docs/
- src/argentina/
- tests/

Objetivo:
- auditar el estado actual
- buscar ideas en paquetes similares
- proponer módulos nuevos
- NO escribir código

Salida:
Crear un archivo nuevo en:

proposals/pending/

Formato del archivo:

# Propuesta: <nombre>

## Problema

## Benchmark / paquete de referencia

## Traducción a Argentina

## API propuesta

## Archivos a modificar

## Dependencias

## Core o extra

## Tests necesarios

## Riesgos

## Prioridad

## Contexto adicional

También debés usar como contexto:
- conversaciones previas del proyecto/grupo `argentina`
- decisiones arquitectónicas discutidas anteriormente
- módulos ya diseñados en sesiones anteriores
- convenciones de nombres ya utilizadas
- discusiones sobre core liviano vs extras opcionales
- ideas descartadas anteriormente

Objetivo:
- mantener continuidad entre sesiones
- evitar reproponer lo mismo
- consolidar ideas previas
- convertir discusiones anteriores en propuestas concretas

Antes de generar nuevas propuestas:
1. revisar el repo actual
2. revisar ROADMAP.md
3. revisar proposals/
4. revisar reports/
5. usar el contexto histórico del proyecto `argentina`

Si encontrás ideas discutidas anteriormente pero no implementadas:
- crear propuestas concretas para ellas
- marcar que vienen del historial del proyecto

Si encontrás inconsistencias entre:
- conversaciones previas
- código actual
- roadmap
- documentación

crear un reporte en:

reports/inconsistencies.md

Formato:

# Inconsistencias detectadas

## Módulo

## Qué se discutió

## Estado actual

## Recomendación

## Resumen ejecutivo en el chat

Además de crear los archivos markdown en `proposals/pending/`, al final del
ciclo el agente debe imprimir en el chat un resumen ejecutivo corto.

Formato esperado:

# Resumen del ciclo de research

## Estado general del repo
- breve diagnóstico
- módulos más sólidos
- inconsistencias encontradas
- riesgos detectados

## Nuevas propuestas generadas

Para cada propuesta:

- nombre
- prioridad
- core o extra
- inspiración/benchmark
- utilidad práctica
- dificultad estimada

Ejemplo:

- `argentina.municipios`
  - prioridad: alta
  - tipo: core
  - benchmark: paquete `us`
  - utilidad: lookup flexible de municipios argentinos
  - dificultad: baja

## Recomendación principal

Elegir UNA propuesta como siguiente implementación recomendada y explicar por qué.

## Riesgos o advertencias

- dependencias pesadas
- fuentes poco estables
- posibles duplicaciones
- APIs inconsistentes
- módulos demasiado amplios

Reglas:
- el resumen debe aparecer en el chat
- además deben crearse los archivos markdown en `proposals/pending/`
- no escribir código
- no modificar `src/`
- no implementar nada todavía

