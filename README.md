# Predicción de resistencia antimicrobiana en *Acinetobacter baumannii*

Repositorio de código y documentación para una tesis sobre un flujo bioinformático para estudiar la resistencia antimicrobiana (AMR) en *A. baumannii*. El proyecto contempla modelado de aprendizaje automático y evaluación externa con genomas latinoamericanos independientes como etapas posteriores.

## Objetivo científico

Desarrollar y evaluar un flujo reproducible que conecte genomas, características genómicas y fenotipos de susceptibilidad antimicrobiana. La pregunta central del proyecto es evaluar el desempeño predictivo y la capacidad de generalización de modelos de aprendizaje automático bajo validación interna y evaluación externa independiente.

## Estado actual y límites

- La representación genómica construida y documentada hasta esta etapa es una matriz de presencia/ausencia de clústeres proteicos.
- Esta matriz **no es una representación de 11-mers de ADN**. No se debe describir como tal ni equiparar ambas representaciones.
- El modelado final, la validación interna de los modelos y la evaluación externa con la cohorte latinoamericana deben considerarse pendientes hasta disponer de resultados reproducibles y documentados.
- La existencia de un script o de un archivo de salida no demuestra por sí sola que la etapa se haya ejecutado correctamente.
- La reconstrucción del índice de pares de modelado debe distinguirse del script histórico original mientras este no haya sido identificado.

## Datos y resultados de referencia

En la instantánea previamente documentada se registraron los siguientes valores:

| Indicador | Valor documentado |
|---|---:|
| Genomas globales | 1.299 |
| Proteínas predichas | 4.975.722 |
| Clústeres proteicos | 50.385 |
| Dimensiones de la matriz de presencia/ausencia | 1.299 × 50.385 |
| Pares genoma-antibiótico incluidos tras la auditoría | 10.122 |

Estas cifras describen una instantánea documentada del procesamiento, no una verificación nueva realizada por este script. Deben actualizarse solo después de repetir los controles y conservar evidencia reproducible. En la auditoría documentada se registraron además 11.215 pares evaluados y 1.093 excluidos; deben consultarse los logs y criterios de exclusión antes de reutilizar esos conteos en resultados científicos.

## Flujo de trabajo

1. Recuperación de genomas mediante identificadores y fuentes documentadas.
2. Predicción de proteínas con Prodigal, conservando las salidas y los logs necesarios.
3. Agrupamiento de proteínas con CD-HIT, registrando versión y parámetros.
4. Construcción de la matriz de presencia/ausencia de clústeres proteicos.
5. Auditoría de observaciones genoma-antibiótico, etiquetas binarias y exclusiones.
6. Reconstrucción del índice que relaciona observaciones fenotípicas con filas de la matriz.
7. Como etapas posteriores: definir la representación prevista para el análisis, prevenir fuga de información, entrenar y comparar modelos, realizar validación interna y evaluar una cohorte latinoamericana independiente.

Antes de repetir una etapa, confirmar los comandos, parámetros, entradas y rutas en los scripts y en la documentación.

## Scripts principales

| Script | Función |
|---|---|
| `scripts/download_genomes.py` | Recuperación de genomas a partir de identificadores. |
| `scripts/run_prodigal_batch.py` | Ejecución por lotes de Prodigal y registro de salidas. |
| `scripts/build_global_cluster_matrix.py` | Construcción de la matriz de presencia/ausencia de clústeres proteicos. |
| `scripts/audit_phenotype_pairs.py` | Auditoría de observaciones fenotípicas y etiquetas binarias. |
| `scripts/rebuild_modeling_pairs_index.py` | Reconstrucción del índice de modelado; no asumir que es el script histórico original. |

## Documentación

- [Guía de archivos y reproducibilidad](docs/GUIA_ARCHIVOS_Y_REPRODUCIBILIDAD.md): inventario de referencia y pasos para retomar el proyecto.
- [Trazabilidad](docs/TRAZABILIDAD.md): relación entre entradas, transformaciones y salidas.
- [Diccionario de datos](docs/DICCIONARIO_DATOS.md): definición de campos y estructuras.
- [Validación del índice de modelado](docs/VALIDACION_INDICE_MODELADO.md): controles y limitaciones del índice.

Los enlaces se resolverán en GitHub únicamente cuando los archivos correspondientes estén versionados y publicados.

## Reproducibilidad

Para reproducir el análisis no basta con clonar este repositorio:

1. **Código versionado:** registrar el commit utilizado.
2. **Entorno definido:** documentar versiones de Python, bibliotecas, Prodigal y CD-HIT.
3. **Datos trazables:** registrar fuentes, identificadores, fechas y criterios de inclusión/exclusión.
4. **Parámetros y registros:** conservar comandos, configuraciones, logs y conteos.
5. **Integridad:** verificar SHA-256 contra un manifiesto correspondiente a la misma versión de los archivos.
6. **Comprobación:** repetir etapas y comparar dimensiones, identificadores y salidas.
7. **Validación científica:** separar entrenamiento, validación interna y cohorte externa independiente, evitando fuga de información.

### Retomar el proyecto en otra computadora

1. Instalar Git y clonar este repositorio privado.
2. Leer este README y `docs/GUIA_ARCHIVOS_Y_REPRODUCIBILIDAD.md`.
3. Preparar las herramientas y versiones documentadas; no copiar un entorno virtual de Windows como sustituto de una instalación compatible.
4. Recuperar los datos desde fuentes documentadas o almacenamiento autorizado.
5. Verificar la integridad de los archivos y ejecutar las etapas en orden.
6. Comparar los resultados con los registros de referencia y documentar las diferencias.

**Importante:** GitHub contiene únicamente los archivos versionados. Los genomas, las proteínas, las matrices y los resultados voluminosos no se recuperan automáticamente al clonar este repositorio.

## Datos y seguridad

No subir automáticamente datos, proteínas, resultados, logs ni metadatos. Antes de publicar archivos, revisar licencia, procedencia, volumen, rutas personales y ausencia de credenciales o tokens. El `.gitignore` ayuda a reducir riesgos, pero no sustituye una revisión explícita de los archivos que se van a publicar.

## Alcance y limitaciones

Este repositorio documenta un flujo de investigación en desarrollo. No constituye por sí solo una herramienta clínica validada. El rendimiento predictivo y la generalización deben demostrarse mediante análisis apropiados, controles contra fuga de información y resultados verificables.
