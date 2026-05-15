# Propuestas rechazadas

Propuestas que **no se deben implementar tal como están**, ya sea por:

- depender de datasets que envejecen sin un proceso de actualización
  explícito (sin script en `tools/`, sin cadencia documentada),
- haber sido intentadas con datos sintéticos y revertidas,
- requerir una decisión conceptual previa no tomada,
- entrar en conflicto con la política `no datos personales`.

> **Para el builder agent (humano o automatizado):** no elijas de esta
> carpeta. Si querés reactivar una, primero resolvé el motivo del
> rechazo (que figura en el bloque "🚫 RECHAZADA" al inicio de cada
> archivo). Recién después moverla a `pending/`.

## Inventario y motivo

| # | Propuesta | Motivo |
|---|---|---|
| 03 | `nombres` | Base AAIP/RENAPER cambia con cada año de nacimientos. Intento previo con frecuencias sintéticas fue revertido. Requiere `tools/bajar_nombres.py`. |
| 06 | `municipios` | Listado INDEC de ~2300 gobiernos locales no puede derivarse de `departamentos`. Intento previo con "1 muni por depto" fue revertido. Requiere descarga oficial INDEC + decisión sobre solapamiento con `ciudades`/`localidades`. |
| 07 | `localidades` | BAHRA del INDEC tiene códigos oficiales propios; no son inventables ni derivables. Intento previo (que motivó el feedback "¿está actualizada BAHRA?") fue revertido. Requiere descarga oficial INDEC. |
| 08 | `indices` | IPC/UVA/CER/ICL son mensuales — embeber implica desactualización inevitable. Intento previo con valores simulados fue revertido. Reactivar SOLO con `tools/bajar_indices.py` automatizado o dejar el caso de uso en `arg.economia` (online). |
| 09 | `empresas` | CUITs sintéticos asociados a empresas reales son **directamente falsos** (CUIT pertenece a otra entidad). Requiere padrón oficial CNV/JGM/AFIP + validación de licencia. Atención: política `no datos personales`. |
| 10 | `vencimientos` | Pre-existente. Tablas anuales AFIP. Mismo patrón de "dato que envejece sin proceso de update". |
| 11 | `dias_habiles` | Pre-existente. Depende del extra `feriados`. Revisar si conviene una versión liviana en core. |
| 12 | `obras_sociales` | Pre-existente. Padrón RNOS oficial; mismo patrón de "dato que envejece sin proceso de update". |

## Criterio general (consolidado tras 2026-05-13)

Una propuesta se rechaza si **al menos una** de estas condiciones aplica:

1. **Requiere dataset oficial** que cambia con cadencia conocida (mensual,
   trimestral, anual) **y** no hay script en `tools/` que lo baje +
   workflow que lo refresque antes de releases.

2. **No puede sintetizarse fielmente**: los códigos/identificadores son
   propios de la fuente oficial (BAHRA, RNOS, padrón CNV, RENAPER) y
   un valor "parecido pero inventado" es falso, no aproximado.

3. **Choca con la política `no datos personales`** y el scope no acota
   inequívocamente a entidades públicas por obligación regulatoria.

4. **Solapamiento conceptual no resuelto** con módulos existentes
   (ej. ciudad vs municipio vs localidad vs aglomerado).

## Cómo reactivar una propuesta

1. Resolver el motivo concreto que figura en su bloque "🚫 RECHAZADA".
2. Si depende de datos oficiales, agregar antes el script `tools/bajar_X.py`
   que demuestre la descarga reproducible.
3. Editar la propuesta indicando cómo cambió y borrar/actualizar el
   bloque "RECHAZADA".
4. Mover a `pending/`.
5. Recién entonces puede ser elegida por el builder agent.

## Antecedentes

- 2026-05-13 — revisión honesta: se sacaron 5 módulos (`localidades`,
  `municipios`, `nombres`, `indices`, `empresas`) y se redujo `afip` a
  IVA + reexports. Reporte: `reports/2026-05-13_correccion_honesta.md`.
- Filosofía consolidada: **mejor que falte un módulo a que devuelva
  datos falsos silenciosamente.**
