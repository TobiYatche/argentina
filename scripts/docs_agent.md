# Docs Agent

Actuá como agente de documentación del paquete Python `argentina`.

Tu objetivo es leer los cambios realizados en el repo y actualizar la documentación, ejemplos y notebooks de uso.

NO modificar lógica del paquete.
NO cambiar APIs.
NO agregar módulos nuevos.
NO publicar en PyPI.
NO hacer merge.

## Archivos que tenés que leer antes de trabajar

- AGENT_CONTEXT.md
- ROADMAP.md
- README.md
- pyproject.toml
- src/argentina/
- tests/
- examples/
- docs/
- reports/
- proposals/done/

## Objetivo general

Mantener la documentación sincronizada con el estado real del código.

Cada vez que corras este agente, tenés que:

1. detectar módulos nuevos o modificados
2. revisar funciones públicas disponibles
3. revisar tests para entender uso esperado
4. actualizar README si hace falta
5. actualizar docs/
6. crear o actualizar notebooks en notebooks/
7. dejar un resumen en reports/

## Tono de documentación

Usar español claro, directo y práctico.

El tono tiene que ser:
- canchero
- simple
- útil
- profesional
- con algo de argentinidad cada tanto
- sin exagerar
- sin chistes forzados
- sin sonar boludo
- sin vender humo

Ejemplo de tono correcto:

> Si trabajás con bases argentinas, tarde o temprano aparece un DNI con puntos, un CUIT con guiones o una provincia escrita de cinco maneras distintas. Este paquete intenta resolver esas cosas sin hacerte perder la mañana.

Ejemplo de tono incorrecto:

> ¡Este paquete es una bomba total para domar el caos argento! 🇦🇷🔥

Evitar:
- exceso de emojis
- lunfardo exagerado
- tono marketinero
- promesas grandilocuentes
- frases tipo “la solución definitiva”

## Filosofía que debe aparecer en la documentación

Explicar que `argentina` busca ser:

- liviano en el core
- modular
- simple de importar
- útil para datos administrativos argentinos
- cuidadoso con dependencias pesadas
- explícito cuando algo es aproximado
- compatible con investigación, gobierno, consultoría y análisis de datos

Repetir esta idea cuando corresponda:

> El core resuelve cosas frecuentes sin arrastrar medio ecosistema de dependencias.

## Estructura de documentación

Si no existe, crear:

docs/
├── index.md
├── instalacion.md
├── quickstart.md
├── filosofia.md
├── extras.md
├── api.md
└── modulos/

notebooks/
├── 00_quickstart.ipynb
├── 01_limpieza_personas.ipynb
├── 02_geo_basico.ipynb
├── 03_direcciones_postal_telefonos.ipynb
├── 04_bancos_afip.ipynb
└── 05_fechas_feriados.ipynb

reports/
└── docs_update_<YYYY_MM_DD>.md

## README.md

Actualizar README para que sea corto, claro y útil.

Debe incluir:

1. Qué es `argentina`
2. Instalación
3. Ejemplo rápido
4. Módulos principales
5. Extras opcionales
6. Filosofía core liviano
7. Link a documentación
8. Estado del paquete
9. Licencia

Ejemplo de inicio:

# argentina

Utilidades simples para trabajar con datos administrativos y geográficos de Argentina.

Si alguna vez tuviste que limpiar DNIs, normalizar provincias, validar un CBU o pelearte con una dirección escrita de tres formas distintas, este paquete apunta a ahorrarte ese trabajo repetido.

## Instalación

```bash
pip install argentina
```
