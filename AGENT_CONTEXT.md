# argentina — Agent Context

## Filosofía

- core liviano
- stdlib primero
- imports rápidos
- extras opcionales para dependencias pesadas
- no scraping frágil
- no datos personales
- no dependencias pesadas en core

## Convenciones API

- limpiar_*
- validar_*
- normalizar_*
- formatear_*
- lookup
- listar

## Core permitido

- stdlib
- csv
- json
- re
- pathlib
- importlib.resources

## Dependencias opcionales

- pandas
- requests
- geopandas
- folium
- duckdb
- pyarrow

## Objetivo

Resolver tareas repetitivas de datos argentinos.
