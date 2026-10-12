from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "results" / "features"
LABELS = FEATURES / "phenotype_binary_labels.csv"
GENOMES = FEATURES / "global_cluster_genome_ids.txt"
OUTPUT = FEATURES / "modeling_pairs_index_rebuilt.csv"

def main():
    if OUTPUT.exists():
        raise FileExistsError(f"No se sobrescribe el archivo existente: {OUTPUT}")
    labels = pd.read_csv(LABELS, dtype={"genome_id": str, "antibiotic": str})
    genomes = pd.read_csv(GENOMES, header=None, dtype=str)[0]
    if genomes.duplicated().any():
        raise ValueError("Hay genome_id duplicados en el catálogo de filas.")
    if labels[["genome_id", "antibiotic", "binary_label"]].isna().any().any():
        raise ValueError("Hay valores ausentes en las etiquetas necesarias.")
    if labels.duplicated(["genome_id", "antibiotic"]).any():
        raise ValueError("Hay pares genoma-antibiótico duplicados en las etiquetas.")
    if not labels["binary_label"].isin([0, 1]).all():
        raise ValueError("Se encontraron etiquetas distintas de 0 y 1.")
    row_map = pd.DataFrame({"genome_id": genomes, "matrix_row": range(len(genomes))})
    missing = sorted(set(labels["genome_id"]) - set(genomes))
    if missing:
        raise ValueError(f"Genomas de las etiquetas ausentes de la matriz: {len(missing)}")
    result = labels.merge(row_map, on="genome_id", how="left", validate="many_to_one")
    result = result[["genome_id", "matrix_row", "antibiotic", "binary_label"]]
    result = result.sort_values(["matrix_row", "antibiotic"]).reset_index(drop=True)
    result.to_csv(OUTPUT, index=False)
    print(f"Índice reconstruido: {OUTPUT}")
    print(f"Filas: {len(result)} | Genomas: {result.genome_id.nunique()} | Antibióticos: {result.antibiotic.nunique()}")

if __name__ == "__main__":
    main()
