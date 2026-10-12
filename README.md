# Predicción de resistencia antimicrobiana en Acinetobacter baumannii

Proyecto de tesis sobre el desarrollo reproducible de una metodología de
bioinformática y aprendizaje automático para estudiar la predicción de
fenotipos de resistencia antimicrobiana a partir de genomas bacterianos.

## Estado del proyecto

La fase documentada incluye procesamiento de genomas, predicción de proteínas,
agrupamiento con CD-HIT, construcción de una matriz de presencia/ausencia de
clústeres proteicos y auditoría de pares genoma-antibiótico.

La cohorte latinoamericana independiente y la evaluación externa deben
documentarse como etapas separadas. No se afirma aquí que los modelos finales
o la validación externa ya estén completados.

## Datos y resultados de referencia

En la instantánea auditada se registraron:

- 1.299 genomas globales.
- 4.975.722 proteínas predichas.
- 50.385 clústeres de proteínas.
- Una matriz de presencia/ausencia de 1.299 × 50.385.
- 10.122 pares genoma-antibiótico con etiquetas binarias tras la auditoría.

Estas cifras describen el estado registrado del procesamiento y deben
actualizarse solo cuando existan nuevas verificaciones reproducibles.

## Organización

- `scripts/`: scripts de procesamiento y auditoría.
- `docs/`: diccionario de datos, trazabilidad y validaciones.
- `data/`, `metadata/`, `proteins/`, `results/` y `logs/`: datos y productos
  locales excluidos de la publicación ordinaria mediante `.gitignore`.

## Reproducibilidad y límites

Las instrucciones y dependencias deben verificarse en un entorno limpio antes
de declarar el flujo completamente reproducible. La reconstrucción del índice
de modelado debe distinguirse del script histórico original mientras este no
haya sido identificado.

Los genomas y los resultados voluminosos no se distribuyen en este repositorio.
Antes de compartir datos derivados, deben comprobarse su procedencia y sus
condiciones de redistribución.

## Tecnologías registradas

Python, Prodigal y CD-HIT. Las versiones y dependencias deben consultarse en
la documentación del proyecto y validarse antes de reproducir cada etapa.
