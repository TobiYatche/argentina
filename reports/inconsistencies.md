# Inconsistencias detectadas

Auditoría del 2026-05-13 sobre el repo `argentina` (v0.3.0).
Comparación entre `ROADMAP.md`, `src/argentina/`, `docs/`, y el historial del
proyecto en memoria.

---

## Módulo: afip

### Qué se discutió

`ROADMAP.md → Core` lista `afip` como uno de los módulos del núcleo del paquete.
La filosofía del paquete (`AGENT_CONTEXT.md`) lo permite: serían tablas oficiales
embebidas + lookups, sin scraping ni internet.

### Estado actual

No existe `src/argentina/afip.py`. Lo único relacionado con AFIP en el repo está
disperso dentro de `src/argentina/personas.py`: `limpiar_cuit`, `validar_cuit`,
`tipo_cuit`, `formatear_cuit`, `extraer_dni_de_cuit`, `generar_cuit`,
`calcular_digito_cuit`. No hay nada sobre Monotributo, IVA, Ganancias.

`docs/modulos/` tampoco tiene `afip.md`.

### Recomendación

Implementar el módulo siguiendo `proposals/pending/02_afip.md`. La
implementación CUIT permanece en `personas` (no romper compatibilidad) y `afip`
la reexporta por descubribilidad. Agregar las tablas Monotributo/IVA/Ganancias
como CSV embebidos con vigencia por año.

---

## Módulo: ciudades / aglomerados

### Qué se discutió

`ROADMAP.md → Core` enumera explícitamente:
provincias, departamentos, clean, personas, postal, bancos, afip, fechas,
telefonos, direcciones, educacion, salud. **No menciona** `ciudades` ni
`aglomerados`.

### Estado actual

Ambos módulos existen, están exportados en `src/argentina/__init__.py`, tienen
tests (`test_ciudades.py`, `test_aglomerados.py`), datos embebidos
(`ciudades.csv`, `aglomerados.csv`), notebooks de prueba y documentación
(`docs/modulos/ciudades.md`). Son módulos core de facto.

### Recomendación

Actualizar `ROADMAP.md → Core` agregando `ciudades` y `aglomerados`. El roadmap
debe reflejar el estado real del paquete, no quedar atrás. Cambio puramente
documental, no toca código.

---

## Módulo: identificar / coordenadas / monedas / pais / paises_limitrofes / patentes / presidentes / universidades / aeropuertos

### Qué se discutió

Ninguno de estos módulos figura en `ROADMAP.md` (ni en core, ni en opcionales,
ni en "próximas ideas").

### Estado actual

Todos existen en `src/argentina/`, están exportados desde `__init__.py`, tienen
tests, y varios tienen notebook y docs. Son parte funcional del paquete.

### Recomendación

Decidir, por cada uno, si entra a `ROADMAP.md → Core` o si conviene crear una
nueva sección "Datos de referencia" / "Catálogos" para distinguirlos de los
módulos con lógica (clean, personas, fechas). El criterio sugerido:

- Catálogos puros (CSV + lookup): `monedas`, `pais`, `paises_limitrofes`,
  `patentes`, `presidentes`, `universidades`, `aeropuertos`, `coordenadas`.
- Lógica/operaciones: `identificar`.

Sea cual sea la organización, no dejarlos sin mencionar en el roadmap.

---

## Módulo: economia

### Qué se discutió

Según la memoria del proyecto (`project_overview.md`), `argentina.economia` es
uno de los dos módulos paralelos del paquete (junto con `provincias`). El
usuario fue explícito en 2026-05-12: "yo queria que armes por un lado
argentina.provincias y por otro argentina.economia". Es un módulo de primera
clase, usa pandas/requests.

### Estado actual

`src/argentina/economia/` existe como subpaquete, tiene tests
(`test_economia.py`, `test_economia_optional.py`) y doc (`docs/modulos/economia.md`).
**Pero NO se importa en `src/argentina/__init__.py`** — no aparece en la lista
de imports ni en `__all__`. El usuario que hace `import argentina as arg` y
después `arg.economia.<algo>` falla, a menos que importe explícitamente
`from argentina import economia`.

### Recomendación

Verificar si la omisión es intencional (por ejemplo, para no forzar la carga
de pandas/requests al importar el paquete). Si lo es: documentarlo
explícitamente en `docs/modulos/economia.md` y en `README.md` con el patrón
"para usar economia, `from argentina import economia` o `import argentina.economia`".
Si no lo es: agregar `from argentina import economia` al `__init__.py` y al
`__all__`.

Esta es la inconsistencia más importante de las detectadas porque contradice
una decisión explícita y registrada del usuario.

---

## Sección: "Próximas ideas" del ROADMAP

### Qué se discutió

`ROADMAP.md → Próximas ideas` enumera: municipios, localidades, nombres,
matching, formato, clae, empresas.

### Estado actual

Ninguno implementado. Tres de ellos ya tienen propuesta concreta en
`proposals/pending/`: `matching` (01), `nombres` (03). `afip` se cubre con
02 (aunque pertenece a core, no a "próximas ideas").

Pendientes sin propuesta: `municipios`, `localidades`, `formato`, `clae`,
`empresas`.

### Recomendación

Próximas iteraciones del Research Agent: priorizar `clae` (relevante junto a
`afip` para análisis de actividades económicas) y `formato` (transversal:
puede absorber `formatear_cuit`, `formatear_dni`, formateo de teléfonos,
direcciones, montos — hoy disperso entre módulos). `municipios`/`localidades`
requieren primero validar fuente de datos oficial actualizada (INDEC o
provinciales).

---

## Resumen

- 1 inconsistencia mayor: `economia` no exportado en `__init__.py`, contra
  decisión explícita del usuario.
- 1 gap del roadmap → repo: `afip` listado, no implementado (ya propuesto).
- 11 módulos en repo no listados en roadmap (documental).
- 5 ítems en "Próximas ideas" sin propuesta concreta todavía.
