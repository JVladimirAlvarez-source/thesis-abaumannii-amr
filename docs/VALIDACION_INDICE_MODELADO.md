# Validación del índice de modelado

## Archivo evaluado
`results/features/modeling_pairs_index.csv`

## Resultados verificados
- Filas: 10.122.
- Genomas únicos: 1.299.
- Antibióticos: 11.
- Etiquetas binarias: 0 y 1.
- Valores ausentes: ninguno.
- Todas las filas de matriz están dentro del rango válido.
- Todos los identificadores coinciden con el orden de la matriz genómica.
- Pares genoma-antibiótico duplicados: 0.
- Todas las etiquetas coinciden con el archivo de fenotipos binarios.
- Pares sin correspondencia fenotípica: 0.

## Interpretación y límites
Los controles confirman la consistencia del índice con la matriz genómica y las etiquetas fenotípicas actuales. No validan el rendimiento predictivo ni la independencia de una cohorte externa. El procedimiento original de creación del índice sigue pendiente de documentar.

## Reproducibilidad
Las comprobaciones se ejecutaron mediante Python en la VM Azure. Se debe conservar el comando de validación y registrar el procedimiento definitivo de generación del índice.

## Reconstrucción independiente del índice

Se reconstruyeron los registros combinando `phenotype_binary_labels.csv` con `global_cluster_genome_ids.txt`, asignando `matrix_row` mediante la posición basada en cero de cada genoma.

Tras normalizar `binary_label` a entero y ordenar ambos conjuntos por `matrix_row` y `antibiotic`, los cuatro campos coinciden en las 10.122 filas: 0 filas diferentes.

El orden de las filas del archivo original no coincide con el orden reconstruido. El contenido es equivalente después de ordenar, pero no se ha recuperado el orden histórico ni identificado el script original de generación.
