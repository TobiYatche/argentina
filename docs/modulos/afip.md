# AFIP

`argentina.afip` provee acceso offline a los datos AFIP **estables** y
reexporta las funciones de CUIT/CLAE que ya viven en otros módulos.

## Alcance: qué incluye

- Alícuotas de IVA vigentes (Ley 23.349 + modificatorias): general 21 %,
  reducida 10,5 %, especial 27 %.
- Reexports de validación/formateo de CUIT (de `arg.personas`).
- Reexports de lookup/búsqueda de CLAE (de `arg.clae`).

## Alcance: qué NO incluye (deliberadamente)

- **Categorías de Monotributo**: cambian por resolución general (a
  veces varias veces al año por inflación). Embeberlas sin un proceso
  explícito de actualización corre el riesgo de devolver datos
  desactualizados silenciosamente. Para valores vigentes, consultar
  AFIP directamente.
- **Mínimo no imponible de Ganancias**: misma razón.

Cuando se decida incorporarlas con un proceso de actualización claro
(por ejemplo, un extra opcional con descarga manual), se agregan.

## IVA

```python
import argentina as arg

arg.afip.alicuotas_iva()
# {'general': 0.21, 'reducida': 0.105, 'especial': 0.27}

# Constante pública si se necesita por importación
arg.afip.ALICUOTAS_IVA
```

## CUIT (reexports)

```python
arg.afip.validar_cuit("20-12345678-6")
arg.afip.limpiar_cuit("20.12345678.6")
arg.afip.formatear_cuit("20123456786")
arg.afip.tipo_cuit("30123456789")  # 'persona_juridica'
```

La **implementación canónica vive en** [`argentina.personas`](personas.md).
`afip.*` solo delega, sin reimplementar. Si la canónica cambia, los
reexports reflejan el cambio inmediatamente.

## CLAE (reexports)

```python
arg.afip.clae_lookup("620100")
arg.afip.clae_buscar("informática")
```

La implementación canónica vive en [`argentina.clae`](clae.md).

## Filosofía

- Sin dependencias externas.
- Sin internet, sin scraping.
- Sin embeber datos que envejecen rápido sin un proceso de
  actualización: mejor que `afip` falte una tabla a que devuelva la
  vieja silenciosamente.
- Reusa implementaciones canónicas (`personas`, `clae`); no duplica.
