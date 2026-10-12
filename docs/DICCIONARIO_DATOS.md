# Diccionario de datos — Proyecto A. baumannii

## 1. Convenciones

- `genome_id`: identificador del genoma. Debe leerse como texto; no convertirlo a número.
- `antibiotic`: antibiótico asociado a la medición o etiqueta.
- `binary_label`: 1 = resistente; 0 = susceptible.
- Los campos originales se conservan según los metadatos de entrada.
- Una definición inferida del nombre de una columna no sustituye la documentación oficial de la fuente.

## 2. metadata/abaumannii_genomes_analytical.csv

| Columna | Significado operativo |
|---|---|
| `genome_id` | Identificador del genoma; clave para enlazar archivos y metadatos. |
| `genome_name` | Nombre descriptivo del genoma según la fuente. |
| `genome_quality` | Campo de calidad declarado en los metadatos. Interpretación exacta pendiente de documentación de origen. |
| `genome_status` | Estado declarado del genoma en la fuente. Interpretación exacta pendiente de documentación de origen. |

## 3. metadata/abaumannii_phenotypes_analytical.csv

Fuente de mediciones fenotípicas. No modificar para crear etiquetas; las decisiones se registran en archivos derivados.

| Columna | Significado operativo |
|---|---|
| `measurement` | Registro o descripción de la medición reportada. |
| `date_inserted` | Fecha de incorporación del registro. |
| `resistant_phenotype` | Categoría fenotípica reportada; se usa para la regla de clasificación. |
| `public` | Campo de visibilidad declarado por la fuente; significado exacto pendiente de confirmar. |
| `testing_standard_year` | Año del estándar de prueba reportado. |
| `taxon_id` | Identificador taxonómico declarado. |
| `measurement_value` | Valor de medición reportado. |
| `date_modified` | Fecha de modificación del registro. |
| `evidence` | Campo de evidencia reportado por la fuente; interpretación exacta pendiente. |
| `id` | Identificador del registro de medición. |
| `owner` | Campo de propietario reportado por la fuente. |
| `testing_standard` | Estándar de prueba reportado. |
| `pmid` | Identificador bibliográfico PubMed, cuando está disponible. |
| `genome_id` | Identificador del genoma asociado a la medición. Leer como texto. |
| `genome_name` | Nombre del genoma asociado a la medición. |
| `measurement_sign` | Operador o signo asociado al valor de medición. |
| `antibiotic` | Antibiótico al que corresponde la medición. |
| `_version_` | Campo de versión interno reportado por la fuente. |
| `laboratory_typing_method` | Método de tipificación reportado. |
| `measurement_unit` | Unidad de medición reportada. |
| `vendor` | Proveedor declarado, cuando está disponible. |
| `laboratory_typing_platform` | Plataforma de laboratorio reportada. |
| `laboratory_typing_method_version` | Versión del método de laboratorio reportada. |
| `source` | Fuente declarada del registro. |

La interpretación exacta de estos campos debe contrastarse con la documentación oficial de BV-BRC antes de atribuirles significados más específicos.

## 4. results/features/phenotype_pair_audit.csv

Una fila por pareja `genome_id` + `antibiotic`.

| Columna | Significado |
|---|---|
| `genome_id` | Identificador del genoma. |
| `antibiotic` | Antibiótico evaluado. |
| `categories_observed` | Categorías fenotípicas distintas encontradas en la pareja. |
| `measurement_count` | Número de mediciones agrupadas en la pareja. |
| `measurement_values` | Valores de medición distintos, concatenados. |
| `measurement_signs` | Signos de medición distintos, concatenados. |
| `measurement_records` | Registros de medición distintos, concatenados. |
| `testing_standards` | Estándares reportados, concatenados. |
| `testing_standard_years` | Años de los estándares reportados, concatenados. |
| `dates_inserted` | Fechas de incorporación encontradas, concatenadas. |
| `pmids` | PMID distintos encontrados, concatenados. |
| `contains_intermediate` | Indica si se observó la categoría Intermediate. |
| `decision` | Decisión de inclusión o exclusión aplicada por el script. |
| `binary_label` | 1 para Resistant, 0 para Susceptible; vacío para parejas excluidas. |

Los valores concatenados resumen los registros originales; no representan una nueva medición ni resuelven discrepancias.

## 5. results/features/phenotype_binary_labels.csv

Contiene únicamente parejas incluidas con categorías concordantes.

- `INCLUDED_R`: todas las categorías observadas son Resistant; etiqueta 1.
- `INCLUDED_S`: todas las categorías observadas son Susceptible; etiqueta 0.
- Parejas con Intermediate o categorías discordantes se excluyen del conjunto binario.

Conservar la unidad de análisis genoma-antibiótico: un genoma puede tener etiquetas para varios antibióticos.

## 6. results/features/phenotype_exclusions.csv

Contiene parejas excluidas y la razón almacenada en `decision`. Sirve para auditar las exclusiones sin eliminar los registros de la fuente original.

## 7. results/features/modeling_pairs_index.csv

| Columna | Significado |
|---|---|
| `genome_id` | Identificador que enlaza la etiqueta con el genoma. |
| `matrix_row` | Índice de fila en la matriz global de presencia/ausencia; índice basado en cero. |
| `antibiotic` | Antibiótico para el que aplica la etiqueta. |
| `binary_label` | Etiqueta binaria: 1 resistente, 0 susceptible. |

La etiqueta no debe utilizarse como característica predictora.

## 8. Matriz global de características

Archivo: `results/features/global_cluster_presence_absence.npz`.

- Filas: genomas globales.
- Columnas: clústeres de proteínas de CD-HIT.
- Valor 1: el genoma tiene al menos una proteína miembro del clúster.
- Valor 0: ausencia del clúster, implícita en la matriz dispersa.
- Formato: matriz binaria dispersa CSR.
- Dimensiones documentadas: 1.299 × 50.385.

`results/features/global_cluster_genome_ids.txt` relaciona el orden de filas con `genome_id`.

`results/features/global_cluster_ids.tsv` contiene:
- `column_index`: índice de columna basado en cero.
- `cluster_id`: identificador del clúster.

No cambiar el orden de filas o columnas sin regenerar y validar los archivos de correspondencia.

## 9. Límites de interpretación

- Un clúster CD-HIT no equivale automáticamente a un gen funcional u ortólogo.
- Las etiquetas representan las categorías presentes en los metadatos y las reglas de auditoría aplicadas.
- Este diccionario describe el procesamiento registrado; no sustituye la documentación de la fuente original.
- La cohorte latinoamericana externa debe permanecer independiente del desarrollo del catálogo y de los modelos.
