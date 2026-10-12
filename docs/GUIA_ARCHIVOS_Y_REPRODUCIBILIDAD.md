# Guía de archivos y reproducibilidad

## Propósito

Esta guía ayuda a identificar qué documentación y código se encuentran en el repositorio y qué elementos deben recuperarse por separado. No sustituye la revisión de los scripts ni demuestra que todas las etapas se hayan ejecutado correctamente.

## Estructura principal

- `scripts/`: scripts de descarga, procesamiento y auditoría.
- `docs/`: documentación metodológica, diccionario de datos, trazabilidad y validaciones.
- `data/`, `metadata/`, `proteins/`, `results/` y `logs/`: pueden contener datos, productos intermedios, resultados y registros locales. No deben publicarse en bloque.
- `README.md`: resumen del proyecto, estado científico y pasos de reproducibilidad.

## Scripts documentados

| Archivo | Uso descrito |
|---|---|
| `scripts/download_genomes.py` | Recuperar genomas a partir de identificadores. |
| `scripts/run_prodigal_batch.py` | Ejecutar Prodigal por lotes y registrar salidas. |
| `scripts/build_global_cluster_matrix.py` | Construir la matriz de presencia/ausencia de clústeres proteicos. |
| `scripts/audit_phenotype_pairs.py` | Auditar pares genoma-antibiótico y etiquetas binarias. |
| `scripts/rebuild_modeling_pairs_index.py` | Reconstruir el índice de pares de modelado; no asumir que reproduce el script histórico original. |

Verifica la presencia de cada archivo en la versión clonada antes de ejecutarlo.

## Reproducibilidad mínima

1. Registrar el commit de Git y la versión de cada script ejecutado.
2. Documentar versiones de Python, paquetes, Prodigal y CD-HIT.
3. Registrar las fuentes y los identificadores de genomas, así como los criterios de inclusión y exclusión.
4. Conservar parámetros, logs, tablas de resumen y huellas SHA-256 cuando correspondan.
5. Repetir las comprobaciones de dimensiones, identificadores y conteos.
6. No declarar completado el modelado ni la validación externa hasta contar con resultados y registros verificables.

## Datos no versionados

Un clon de Git no recupera los archivos locales ignorados o no versionados. Los datos deben obtenerse desde fuentes documentadas o almacenamiento autorizado y comprobarse por integridad. No ejecutar `git add .` como atajo para publicar el proyecto.

## Representación y alcance científico

La matriz actualmente documentada representa presencia/ausencia de clústeres proteicos; no representa 11-mers de ADN. Cualquier análisis futuro basado en 11-mers debe implementarse y documentarse como una etapa diferente. La evaluación externa con genomas latinoamericanos debe permanecer separada de los datos utilizados para entrenar y seleccionar modelos.
