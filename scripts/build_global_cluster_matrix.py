#!/usr/bin/env python3
"""Build a binary genome-by-protein-cluster matrix from CD-HIT membership."""
from pathlib import Path
import re
import sys

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, save_npz

ROOT = Path.home() / "thesis-aba"
CLSTR = ROOT / "results/cdhit/global_proteins_c80_a80.faa.clstr"
GENOME_IDS = ROOT / "metadata/global_genome_ids.txt"
OUT = ROOT / "results/features"
LOG = ROOT / "logs/build_global_cluster_matrix.log"

def main():
    expected = [x.strip() for x in GENOME_IDS.open() if x.strip()]
    if len(expected) != len(set(expected)):
        raise ValueError("El listado de genomas contiene IDs duplicados.")
    genome_to_row = {gid: i for i, gid in enumerate(expected)}

    cluster_ids = []
    rows, cols = [], []
    current_cluster = None
    members = 0
    malformed = 0
    unexpected = set()
    seen_genomes = set()

    member_pattern = re.compile(r">([^_\s]+)__")

    with CLSTR.open() as handle:
        for line in handle:
            if line.startswith(">Cluster "):
                current_cluster = line.strip().split()[-1]
                cluster_ids.append(current_cluster)
                continue

            if ">" not in line:
                continue

            members += 1
            match = member_pattern.search(line)
            if match is None or current_cluster is None:
                malformed += 1
                continue

            gid = match.group(1)
            if gid not in genome_to_row:
                unexpected.add(gid)
                continue

            seen_genomes.add(gid)
            rows.append(genome_to_row[gid])
            cols.append(len(cluster_ids) - 1)

    if malformed:
        raise ValueError(f"Miembros no interpretables: {malformed}")
    if unexpected:
        raise ValueError(f"Genomas inesperados: {len(unexpected)}")
    if seen_genomes != set(expected):
        missing = set(expected) - seen_genomes
        raise ValueError(f"Genomas esperados ausentes: {len(missing)}")
    if len(cluster_ids) != 50385:
        raise ValueError(f"Número inesperado de clústeres: {len(cluster_ids)}")
    if members != 4975722:
        raise ValueError(f"Número inesperado de proteínas miembro: {members}")

    matrix = coo_matrix(
        (np.ones(len(rows), dtype=np.uint8), (rows, cols)),
        shape=(len(expected), len(cluster_ids)),
        dtype=np.uint8,
    ).tocsr()
    matrix.sum_duplicates()
    matrix.data[:] = 1
    matrix.eliminate_zeros()

    OUT.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)

    matrix_path = OUT / "global_cluster_presence_absence.npz"
    genome_path = OUT / "global_cluster_genome_ids.txt"
    cluster_path = OUT / "global_cluster_ids.tsv"
    summary_path = OUT / "global_cluster_matrix_summary.txt"

    save_npz(matrix_path, matrix, compressed=True)
    genome_path.write_text("\n".join(expected) + "\n")
    pd.DataFrame({
        "column_index": np.arange(len(cluster_ids)),
        "cluster_id": cluster_ids,
    }).to_csv(cluster_path, sep="\t", index=False)

    summary = [
        f"genomes={matrix.shape[0]}",
        f"clusters={matrix.shape[1]}",
        f"protein_members={members}",
        f"unique_genome_cluster_pairs={matrix.nnz}",
        f"matrix_density={matrix.nnz / (matrix.shape[0] * matrix.shape[1]):.8f}",
        f"matrix_format=CSR sparse binary",
        f"identity_threshold=0.80",
        f"global_identity=1",
        f"shorter_sequence_coverage=0.80",
        f"longer_sequence_coverage=0.80",
        f"external_LATAM_genomes_in_catalog=0",
    ]
    summary_path.write_text("\n".join(summary) + "\n")

    with LOG.open("w") as log:
        log.write("\n".join(summary) + "\n")
        log.write(f"matrix_file={matrix_path}\n")
        log.write(f"genome_ids_file={genome_path}\n")
        log.write(f"cluster_ids_file={cluster_path}\n")

    print("Matriz creada y validada.")
    print("Dimensiones:", matrix.shape)
    print("Presencias únicas genoma-clúster:", matrix.nnz)
    print("Densidad:", f"{matrix.nnz / (matrix.shape[0] * matrix.shape[1]):.8f}")
    print("Archivo:", matrix_path)
    print("Resumen:", summary_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
