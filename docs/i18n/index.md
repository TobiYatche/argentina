# Idiomas / Languages / 言語 / 언어 / Языки / اللغات

`argentina` se diseña y documenta principalmente en español argentino. Como
el paquete puede ser útil para gente de fuera de Argentina (investigación
comparada, trabajo regional, sector privado internacional), mantenemos un
README traducido en 10 idiomas además del original.

> Las traducciones cubren el README (instalación, ejemplo rápido, módulos,
> filosofía). La documentación detallada en `docs/modulos/`, los notebooks
> y la API reference siguen en español. Si necesitás algo puntual en otro
> idioma, abrí un issue.

## Disponibles

| Idioma | Código | Archivo |
|---|---|---|
| 🇪🇸 Español (original) | `es` | [README.md](https://github.com/tobiasyatche/argentina#readme) |
| 🇬🇧 English | `en` | [en/README.md](en/README.md) |
| 🇧🇷 Português | `pt` | [pt/README.md](pt/README.md) |
| 🇫🇷 Français | `fr` | [fr/README.md](fr/README.md) |
| 🇮🇹 Italiano | `it` | [it/README.md](it/README.md) |
| 🇩🇪 Deutsch | `de` | [de/README.md](de/README.md) |
| 🇨🇳 中文 (简体) | `zh` | [zh/README.md](zh/README.md) |
| 🇯🇵 日本語 | `ja` | [ja/README.md](ja/README.md) |
| 🇰🇷 한국어 | `ko` | [ko/README.md](ko/README.md) |
| 🇷🇺 Русский | `ru` | [ru/README.md](ru/README.md) |
| 🇸🇦 العربية | `ar` | [ar/README.md](ar/README.md) |

## ¿Cómo se mantienen sincronizadas?

El README español es la **fuente de verdad**. Cuando cambia, el agente de
documentación re-traduce los otros 10. Si encontrás una desincronización o
un error de traducción, abrí un issue indicando idioma y línea.

## ¿Por qué solo el README?

Para no acumular deuda de docs:

- El README cubre el 80% de lo que un usuario nuevo necesita: para qué
  sirve, cómo se instala, ejemplo rápido, qué hay en el paquete.
- La documentación detallada de cada módulo se actualiza muy seguido
  (cada release suma o ajusta funciones). Mantener 10 versiones
  sincronizadas en `docs/modulos/` sería un costo enorme con poco
  retorno.
- Los nombres de las funciones y los identificadores en los ejemplos son
  los mismos en todos los idiomas — `arg.provincias.lookup` se entiende
  en cualquier idioma una vez que sabés qué hace.

Si querés ayudar a expandir alguna traducción (por ejemplo, traducir
`quickstart.md` a tu idioma), abrí un PR.
