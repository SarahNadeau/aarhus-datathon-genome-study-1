#!/bin/bash
set -euo pipefail

# TITLE: Run the pipeline

mkdir -p temp

# Parse the mutations file into a per-sample dictionary of nucleotide mutations
python scripts/python/parse_mutations_file.py \
-m data/mutations_snpeff_annotated_tidy_Switzerland.tsv \
-o temp/parsed_mut_210821.tsv

# Select genome IDs to analyze based on confirmed case data and parameters in config.yaml
python scripts/python/subset_sequences.py

# Calculate weekly diversity based on selected genome IDs
python scripts/python/calc_diversity.py
