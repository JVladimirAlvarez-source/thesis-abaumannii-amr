from pathlib import Path
import pandas as pd

ROOT = Path.home() / "thesis-aba"
SRC = ROOT / "metadata/abaumannii_phenotypes_analytical.csv"
OUT = ROOT / "results/features"
OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SRC, dtype={"genome_id": str}, low_memory=False)
for c in ["genome_id", "antibiotic", "resistant_phenotype"]:
    df[c] = df[c].astype("string").str.strip()

keys = ["genome_id", "antibiotic"]
missing = df[df[keys + ["resistant_phenotype"]].isna().any(axis=1)].copy()
missing.to_csv(OUT / "phenotype_records_missing_keys.csv", index=False)

valid = df.dropna(subset=keys + ["resistant_phenotype"]).copy()
rows = []

def values(group, col):
    vals = group[col].dropna().astype(str).str.strip()
    return " | ".join(sorted(set(v for v in vals if v)))

for (gid, antibiotic), g in valid.groupby(keys, sort=True):
    cats = set(g["resistant_phenotype"])
    has_i = "Intermediate" in cats

    if cats == {"Resistant"}:
        reason, label = "INCLUDED_R", 1
    elif cats == {"Susceptible"}:
        reason, label = "INCLUDED_S", 0
    elif len(cats) > 1 and has_i:
        reason, label = "EXCLUDED_DISCORDANT_AND_INTERMEDIATE", None
    elif len(cats) > 1:
        reason, label = "EXCLUDED_DISCORDANT", None
    elif has_i:
        reason, label = "EXCLUDED_INTERMEDIATE", None
    else:
        reason, label = "EXCLUDED_UNSUPPORTED_CATEGORY", None

    rows.append({
        "genome_id": gid,
        "antibiotic": antibiotic,
        "categories_observed": " | ".join(sorted(cats)),
        "measurement_count": len(g),
        "measurement_values": values(g, "measurement_value"),
        "measurement_signs": values(g, "measurement_sign"),
        "measurement_records": values(g, "measurement"),
        "testing_standards": values(g, "testing_standard"),
        "testing_standard_years": values(g, "testing_standard_year"),
        "dates_inserted": values(g, "date_inserted"),
        "pmids": values(g, "pmid"),
        "contains_intermediate": has_i,
        "decision": reason,
        "binary_label": label,
    })

audit = pd.DataFrame(rows)
audit.to_csv(OUT / "phenotype_pair_audit.csv", index=False)
audit[audit["decision"].str.startswith("EXCLUDED")].to_csv(
    OUT / "phenotype_exclusions.csv", index=False
)
audit[audit["decision"].isin(["INCLUDED_R", "INCLUDED_S"])].to_csv(
    OUT / "phenotype_binary_labels.csv", index=False
)

summary = audit.groupby(["antibiotic", "decision"]).size().unstack(fill_value=0)
summary["TOTAL_PAIRS"] = summary.sum(axis=1)
summary.to_csv(OUT / "phenotype_audit_summary.csv")

print("Parejas auditadas:", len(audit))
print("Parejas binarias incluidas:", int(audit["binary_label"].notna().sum()))
print("Parejas excluidas:", int(audit["decision"].str.startswith("EXCLUDED").sum()))
print("Registros con campos clave ausentes:", len(missing))
print("Antibióticos:", audit["antibiotic"].nunique())
print("Resumen por antibiótico:")
print(summary.to_string())
print("Archivos guardados en:", OUT)
