# Trazabilidad de procedimientos y resultados

Este registro conecta los datos de entrada, los scripts, los productos generados y las evidencias de ejecución. Las rutas son relativas a `~/thesis-aba/`.

| Etapa | Entrada principal | Script o herramienta | Salidas principales | Evidencia |
|---|---|---|---|---|
| Descarga de genomas | `metadata/global_genome_ids.txt` | `scripts/download_genomes.py` y API BV-BRC | `data/raw/genomes/*.fasta` | `logs/download_genomes.log` |
| Predicción de proteínas | Genomas FASTA | `scripts/run_prodigal_batch.py`, Prodigal 2.6.3 | `results/prodigal/proteins/*.faa`, `genes/*.fna`, `annotations/*.gff` | `logs/prodigal_summary.csv`, `logs/prodigal/*.log` |
| Catálogo de proteínas | `data/interim/global_proteins_all.faa` | CD-HIT 4.8.1 | `results/cdhit/global_proteins_c80_a80.faa` y archivo `.clstr` | `logs/cdhit_global_c80_a80.log` |
| Matriz genómica | Archivo `.clstr` y lista de genomas | `scripts/build_global_cluster_matrix.py` | `results/features/global_cluster_presence_absence.npz`, archivos de correspondencia y resumen | `logs/build_global_cluster_matrix_run.log` |
| Auditoría fenotípica | `metadata/abaumannii_phenotypes_analytical.csv` | `scripts/audit_phenotype_pairs.py` | Auditoría, etiquetas binarias, exclusiones y resumen | `logs/audit_phenotype_pairs.log` |
| Índice para modelado | Etiquetas binarias y orden de filas de la matriz | Reconstrucción reproducible: scripts/rebuild_modeling_pairs_index.py; script histórico original no identificado | `results/features/modeling_pairs_index.csv` | Verificaciones registradas en la sesión de trabajo |

## Resultados de referencia

- Genomas globales: 1.299.
- Proteínas predichas: 4.975.722.
- Clústeres CD-HIT: 50.385.
- Matriz global: 1.299 × 50.385.
- Presencias únicas genoma-clúster: 4.902.642.
- Parejas genoma-antibiótico auditadas: 11.215.
- Parejas binarias incluidas: 10.122.
- Parejas excluidas: 1.093.

## Precauciones

- No confundir el catálogo piloto con el catálogo global.
- Preservar los identificadores de genoma como texto.
- No mezclar las etiquetas fenotípicas con las características predictoras.
- No incorporar la cohorte latinoamericana externa al catálogo global durante el desarrollo.
- La creación del índice de modelado aún requiere identificar y registrar el script exacto utilizado.
- Esta tabla es una primera versión: las rutas y cifras deben contrastarse con los archivos y registros conservados.
