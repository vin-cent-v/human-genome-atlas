#!/usr/bin/env python3
"""Verify one pinned T2T-CHM13v2.0 data snapshot before publishing a Release.
Uses Python standard library only. Never silently upgrades assembly versions.
"""
from __future__ import annotations

import datetime
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

REFERENCE = "T2T-CHM13v2.0 / UCSC hs1"
ASSEMBLY = "GCA_009914755.4"
BASE = "https://hgdownload.soe.ucsc.edu/goldenPath/hs1/bigZips/"
EXPECTED_MD5 = {
    "hs1.fa.gz": "a493d5402cc86ecc3f54f6346d980036",
    "hs1.chrom.sizes.txt": "12669b911f5cf251c2e83f8240c1c74a",
    "hs1.ncbiRefSeq.gtf.gz": "bd7063efcbfed4774d9be42db8173a6e",
}
SOURCES = {
    "hs1.fa.gz": BASE + "hs1.fa.gz",
    "hs1.chrom.sizes.txt": BASE + "hs1.chrom.sizes.txt",
    "hs1.ncbiRefSeq.gtf.gz": BASE + "genes/hs1.ncbiRefSeq.gtf.gz",
}
TOTAL_BASES = 3_117_292_070
EXPECTED_CONTIGS = 25
BASES = re.compile(rb"^[ACGTNacgtn]+$")


def check_hashes(path: Path) -> dict:
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(8 * 1024 * 1024):
            md5.update(block)
            sha256.update(block)
    expected = EXPECTED_MD5[path.name]
    actual = md5.hexdigest()
    if actual != expected:
        raise ValueError(f"{path.name}: checksum mismatch: {actual} != {expected}")
    return {"name": path.name, "bytes": path.stat().st_size,
            "md5": actual, "sha256": sha256.hexdigest(),
            "source_url": SOURCES[path.name]}


def check_chromosomes(path: Path) -> dict[str, int]:
    lengths = {}
    for row in path.read_text("utf-8").splitlines():
        if not row.strip():
            continue
        fields = row.split("\t")
        if len(fields) != 2:
            raise ValueError("Invalid chromosome size row")
        name, raw_length = fields
        if name in lengths or not re.fullmatch(r"chr(?:[1-9]|1[0-9]|2[0-2]|X|Y|M)", name):
            raise ValueError(f"Unexpected or repeated contig {name}")
        lengths[name] = int(raw_length)
    if len(lengths) != EXPECTED_CONTIGS or sum(lengths.values()) != TOTAL_BASES:
        raise ValueError("Expected 25 sequences totaling 3,117,292,070 bp")
    if lengths["chrM"] != 16569 or lengths["chrY"] != 62460029:
        raise ValueError("Unexpected mitochondrial or Y length")
    return lengths


def check_fasta(path: Path, lengths: dict[str, int]) -> None:
    """Stream through the entire gzipped FASTA without writing a 3.1GB temp copy."""
    observed = {}
    current = None
    with gzip.open(path, "rb") as handle:
        for raw in handle:
            line = raw.strip()
            if not line:
                continue
            if line.startswith(b">"):
                name = line[1:].split()[0].decode("ascii")
                if name not in lengths or name in observed:
                    raise ValueError(f"Unexpected/duplicate FASTA contig: {name}")
                current = name
                observed[name] = 0
            else:
                if current is None or BASES.fullmatch(line) is None:
                    raise ValueError(f"Invalid DNA sequence line in {current}")
                observed[current] += len(line)
    if observed != lengths:
        diff = {k: [lengths.get(k), observed.get(k)]
                for k in set(lengths) | set(observed)
                if lengths.get(k) != observed.get(k)}
        raise ValueError(f"FASTA versus chromosome-length disagreement: {diff}")


def check_gtf(path: Path) -> None:
    """MD5 is authoritative; this adds a lightweight file-format sanity check."""
    found = False
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) == 9 and fields[2] in {"gene", "transcript", "exon"}:
                found = True
                break
    if not found:
        raise ValueError("GTF does not contain a recognizable annotation record")


def main() -> int:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
    if not folder.is_dir():
        raise FileNotFoundError(folder)
    metadata = [check_hashes(folder / filename) for filename in EXPECTED_MD5]
    lengths = check_chromosomes(folder / "hs1.chrom.sizes.txt")
    check_fasta(folder / "hs1.fa.gz", lengths)
    check_gtf(folder / "hs1.ncbiRefSeq.gtf.gz")
    sums = "".join(f"{item['sha256']}  {item['name']}\n" for item in metadata)
    (folder / "SHA256SUMS").write_text(sums, encoding="utf-8")
    provenance = {
        "schema": "human-genome-atlas.provenance.v1",
        "reference": REFERENCE,
        "assembly_accession": ASSEMBLY,
        "contigs": len(lengths),
        "bases": sum(lengths.values()),
        "verified_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "verification": "Pinned MD5 of source files, full streamed FASTA/base count, and GTF format",
        "files": metadata,
        "source_checksum_list": BASE + "md5sum.txt",
        "annotation_checksum_reference":
            "https://grr.seqpipe.org/hs1/gene_models/ncbiRefSeq_20250529/index.html",
    }
    (folder / "DATA_PROVENANCE.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"PASS: {REFERENCE}, {len(lengths)} contigs, {sum(lengths.values()):,} bases")
    for item in metadata:
        print(f"PASS: {item['name']} ({item['bytes']:,} bytes, MD5={item['md5']})")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
