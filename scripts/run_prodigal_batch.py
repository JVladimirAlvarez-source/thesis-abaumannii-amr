#!/usr/bin/env python3
"""Procesamiento reproducible de genomas con Prodigal."""
import csv
import subprocess
import tempfile
from pathlib import Path

ROOT = Path.home() / "thesis-aba"
ID_FILE = ROOT / "metadata/global_genome_ids.txt"
INPUT = ROOT / "data/raw/genomes"
INTERIM = ROOT / "data/interim"
BASE = ROOT / "results/prodigal"
PROTEINS = BASE / "proteins"
GENES = BASE / "genes"
ANNOTATIONS = BASE / "annotations"
LOGS = ROOT / "logs/prodigal"
SUMMARY = ROOT / "logs/prodigal_summary.csv"
FIELDS = ["genome_id", "status", "proteins", "genes",
          "gff_features", "message"]


def count_fasta(path):
    with path.open() as handle:
        return sum(line.startswith(">") for line in handle)


def prefix_fasta(source, destination, genome_id):
    count = 0
    with source.open() as src, destination.open("w") as dst:
        for line in src:
            if line.startswith(">"):
                header = line[1:].rstrip("\r\n")
                first, sep, rest = header.partition(" ")
                dst.write(f">{genome_id}__{first}{sep}{rest}\n")
                count += 1
            else:
                dst.write(line)
    return count


def prefix_gff(source, destination, genome_id):
    count = 0
    with source.open() as src, destination.open("w") as dst:
        for line in src:
            if line.startswith("#") or not line.strip():
                dst.write(line)
                continue
            fields = line.rstrip("\r\n").split("\t")
            if len(fields) != 9:
                raise ValueError("Registro GFF con número incorrecto de columnas")
            fields[0] = f"{genome_id}__{fields[0]}"
            dst.write("\t".join(fields) + "\n")
            count += 1
    return count


def load_summary():
    if not SUMMARY.is_file():
        return []
    with SUMMARY.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_summary(rows):
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    temporary = SUMMARY.with_suffix(".csv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        handle.flush()
    temporary.replace(SUMMARY)


def process_genome(genome_id):
    source = INPUT / f"{genome_id}.fasta"
    outputs = (
        PROTEINS / f"{genome_id}.faa",
        GENES / f"{genome_id}.fna",
        ANNOTATIONS / f"{genome_id}.gff",
    )

    if not source.is_file() or source.stat().st_size == 0:
        return {"genome_id": genome_id, "status": "ERROR_INPUT",
                "proteins": "", "genes": "", "gff_features": "",
                "message": "Entrada ausente o vacía"}

    if any(path.exists() for path in outputs):
        if all(path.is_file() and path.stat().st_size > 0 for path in outputs):
            np, ng = count_fasta(outputs[0]), count_fasta(outputs[1])
            with outputs[2].open() as f:
                records = [line.rstrip("\r\n").split("\t")
                           for line in f if line.strip() and not line.startswith("#")]
            valid_gff = all(len(r) == 9 and r[0].startswith(genome_id + "__")
                            for r in records)
            valid_fasta = all(
                all(not line.startswith(">") or line[1:].startswith(genome_id + "__")
                    for line in path.open())
                for path in outputs[:2]
            )
            if np > 0 and np == ng == len(records) and valid_gff and valid_fasta:
                return {"genome_id": genome_id, "status": "SKIPPED_COMPLETE",
                        "proteins": str(np), "genes": str(ng),
                        "gff_features": str(len(records)),
                        "message": "Salidas existentes validadas; no se modificaron"}
        return {"genome_id": genome_id, "status": "ERROR_PARTIAL_OUTPUT",
                "proteins": "", "genes": "", "gff_features": "",
                "message": "Salidas parciales o inválidas; no se modificaron"}

    with tempfile.TemporaryDirectory(
        prefix=f"prodigal_{genome_id}_", dir=INTERIM
    ) as tmpdir:
        tmp = Path(tmpdir)
        raw_faa, raw_fna, raw_gff = (
            tmp / "raw.faa", tmp / "raw.fna", tmp / "raw.gff"
        )
        command = [
            "prodigal", "-i", str(source),
            "-a", str(raw_faa), "-d", str(raw_fna),
            "-o", str(raw_gff), "-f", "gff",
            "-p", "single", "-q",
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        (LOGS / f"{genome_id}.log").write_text(
            f"COMMAND: {' '.join(command)}\n"
            f"RETURN_CODE: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}\n",
            encoding="utf-8",
        )

        if result.returncode != 0:
            return {"genome_id": genome_id, "status": "ERROR_PRODIGAL",
                    "proteins": "", "genes": "", "gff_features": "",
                    "message": f"Código {result.returncode}; revisar log"}

        if not all(path.is_file() and path.stat().st_size > 0
                   for path in (raw_faa, raw_fna, raw_gff)):
            return {"genome_id": genome_id, "status": "ERROR_EMPTY_OUTPUT",
                    "proteins": "", "genes": "", "gff_features": "",
                    "message": "Una o más salidas están vacías"}

        staged_faa, staged_fna, staged_gff = (
            tmp / "final.faa", tmp / "final.fna", tmp / "final.gff"
        )
        try:
            n_proteins = prefix_fasta(raw_faa, staged_faa, genome_id)
            n_genes = prefix_fasta(raw_fna, staged_fna, genome_id)
            n_features = prefix_gff(raw_gff, staged_gff, genome_id)
        except Exception as exc:
            return {"genome_id": genome_id, "status": "ERROR_FORMAT",
                    "proteins": "", "genes": "", "gff_features": "",
                    "message": str(exc)}

        if not n_proteins or not n_genes or not n_features:
            return {"genome_id": genome_id, "status": "ERROR_EMPTY_ANNOTATION",
                    "proteins": str(n_proteins), "genes": str(n_genes),
                    "gff_features": str(n_features),
                    "message": "Alguna salida no contiene registros"}

        for staged, final in zip(
            (staged_faa, staged_fna, staged_gff), outputs
        ):
            if final.exists():
                return {"genome_id": genome_id, "status": "ERROR_OUTPUT_EXISTS",
                        "proteins": "", "genes": "", "gff_features": "",
                        "message": "Destino existente; no se sobrescribió"}

        for staged, final in zip(
            (staged_faa, staged_fna, staged_gff), outputs
        ):
            staged.replace(final)

        return {"genome_id": genome_id, "status": "OK",
                "proteins": str(n_proteins), "genes": str(n_genes),
                "gff_features": str(n_features), "message": ""}


def main():
    for directory in (PROTEINS, GENES, ANNOTATIONS, LOGS):
        directory.mkdir(parents=True, exist_ok=True)

    if not ID_FILE.is_file():
        print(f"ERROR: no existe {ID_FILE}")
        return 2

    genome_ids = ID_FILE.read_text().splitlines()
    if (not genome_ids or any(not gid.strip() for gid in genome_ids)
            or len(genome_ids) != len(set(genome_ids))):
        print("ERROR: lista vacía, con líneas vacías o IDs duplicados")
        return 2

    rows_by_id = {
        row["genome_id"]: row for row in load_summary()
        if row.get("genome_id")
    }

    for i, genome_id in enumerate(genome_ids, start=1):
        row = process_genome(genome_id)
        rows_by_id[genome_id] = row
        save_summary(list(rows_by_id.values()))
        print("[{}/{}] {}: {}".format(
            i, len(genome_ids), genome_id, row["status"]
        ), flush=True)

    counts = {}
    for gid in genome_ids:
        status = rows_by_id[gid]["status"]
        counts[status] = counts.get(status, 0) + 1

    print("\\nResumen:")
    for status, number in sorted(counts.items()):
        print("{}: {}".format(status, number))
    print("CSV: {}".format(SUMMARY))
    return 0 if all(
        rows_by_id[gid]["status"] in ("OK", "SKIPPED_COMPLETE")
        for gid in genome_ids
    ) else 1

if __name__ == "__main__":
    raise SystemExit(main())
