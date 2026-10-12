import csv
import json
import time
import urllib.request
from pathlib import Path

BASE = Path.home() / "thesis-aba"
IDS_FILE = BASE / "metadata/global_genome_ids.txt"
OUTDIR = BASE / "data/raw/genomes"
OUTDIR.mkdir(parents=True, exist_ok=True)

with IDS_FILE.open() as f:
    ids = [x.strip() for x in f if x.strip()]

def fetch(url):
    last_error = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "thesis-aba-genome-pipeline/1.0"}
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            time.sleep(2 ** attempt)
    raise last_error

def fasta_stats(data):
    text = data.decode("utf-8")
    headers = 0
    bases = 0
    invalid = 0
    alphabet = set("ACGTNRYKMSWBDHVX")
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            headers += 1
        else:
            seq = line.upper()
            bases += len(seq)
            if any(c not in alphabet for c in seq):
                invalid += 1
    return headers, bases, invalid

downloaded = 0
skipped = 0
errors = 0
total = len(ids)

print(f"IDs en la lista: {total}", flush=True)

for index, gid in enumerate(ids, 1):
    target = OUTDIR / f"{gid}.fasta"
    temp = OUTDIR / f"{gid}.fasta.tmp"

    try:
        meta_url = (
            "https://www.bv-brc.org/api/genome/?"
            f"eq(genome_id,{gid})"
            "&select(genome_id,genome_length)"
            "&http_accept=application/json"
        )
        metadata = json.loads(fetch(meta_url))
        if not metadata or int(metadata[0]["genome_id"].split(".")[0]) < 0:
            raise ValueError("metadatos no válidos")
        expected = int(metadata[0]["genome_length"])

        if target.is_file():
            h, b, bad = fasta_stats(target.read_bytes())
            if h > 0 and b == expected and bad == 0:
                skipped += 1
                print(f"[{index}/{total}] VALIDADO, se conserva: {gid}", flush=True)
                continue

        seq_url = (
            "https://www.bv-brc.org/api/genome_sequence/?"
            f"eq(genome_id,{gid})&limit(10000)"
            "&http_accept=application/dna+fasta"
        )
        data = fetch(seq_url)
        h, b, bad = fasta_stats(data)

        if h == 0 or b != expected or bad != 0:
            raise ValueError(
                f"FASTA no válido: contigs={h}, bases={b}, "
                f"esperadas={expected}, líneas/caracteres inválidos={bad}"
            )

        temp.write_bytes(data)
        temp.replace(target)
        downloaded += 1
        print(
            f"[{index}/{total}] OK {gid}: {b:,} nt; {h} contigs",
            flush=True
        )

    except Exception as exc:
        temp.unlink(missing_ok=True)
        errors += 1
        print(f"[{index}/{total}] ERROR {gid}: {exc}", flush=True)

    time.sleep(0.25)

print("\n===== RESUMEN FINAL =====", flush=True)
print(f"IDs procesados: {total}", flush=True)
print(f"Archivos nuevos validados: {downloaded}", flush=True)
print(f"Archivos existentes validados: {skipped}", flush=True)
print(f"Errores: {errors}", flush=True)
print(f"Directorio: {OUTDIR}", flush=True)
