# Human Genome Atlas · 人类基因组知识地图

An interactive Chinese-language educational atlas for human reference genome T2T-CHM13v2.0 / UCSC hs1.

## Explore

- Open [index.html](./index.html) for the chromosome map, gene-function teaching cases and on-demand base sequence reader.
- 25 reference sequences: chromosomes 1–22, X, HG002-derived Y and mitochondrial reference; 3,117,292,070 bases.
- The atlas starts offline. Real online sequence requests require UCSC; local full FASTA requires an uncompressed file and matching .fai. Only 19 gene-function examples are bundled, not all annotated genes.

## Reproducible data mirror

- [Pinned data catalog](data/catalog.json) and [integrity-check script](scripts/verify_data.py).
- Run [Mirror verified T2T-CHM13v2.0 reference](../../actions/workflows/mirror-genome.yml) manually from GitHub Actions.
- The workflow downloads exactly: hs1.fa.gz (about 930MB), hs1.chrom.sizes.txt, hs1.ncbiRefSeq.gtf.gz (about 37MB).
- Source MD5 verification, full streamed FASTA base-length audit and GTF format check are mandatory before publication.
- On success, GitHub Release t2t-chm13v2.0-data-v1 contains these files plus SHA256SUMS and DATA_PROVENANCE.json. An existing release is never silently overwritten.
- HPRC is linked rather than fully mirrored. Do not upload any private personal DNA data to this public repository.

## Optional public site

GitHub repo Settings → Pages → Build and deployment → Deploy from a branch → main / (root) → Save. Once deployed: https://vin-cent-v.github.io/human-genome-atlas/

## Provenance and scientific accuracy

- [T2T CHM13 project](https://github.com/marbl/CHM13)
- [UCSC hs1 assembly](https://genome.ucsc.edu/cgi-bin/hgGateway?db=hs1)
- [UCSC hs1 downloads](https://hgdownload.soe.ucsc.edu/goldenPath/hs1/bigZips/)
- [NCBI assembly GCA_009914755.4](https://www.ncbi.nlm.nih.gov/datasets/genome/GCA_009914755.4/)
- [HPRC data](https://www.humanpangenome.org/data/)

The T2T consortium's released reference genome data are CC0. That does not automatically license this separately authored HTML code and teaching text as CC0. Preserve source attribution and check all upstream licenses. This is science education, not a clinical diagnostic tool.
