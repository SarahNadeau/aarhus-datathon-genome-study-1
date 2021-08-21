# TITLE: Subset sequences.
# INPUT: Sequence data provided by datathon organizers.
# OUTPUT: List of sequence identifiers.

import yaml
import pandas as pd

# Take user input: countries, lineages, date range, weekly proportion of cases to take.
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
print(config)

# Read sequence metadata.
metadata = pd.read_csv(config['path_to_data'] + "/metadata_snpeff_tidy_Denmark.tsv", sep='\t')
print(metadata.head(1))

# Import case count data
case_count_data = pd.read_csv(config['path_to_data'] + "/owid-covid-data.csv")
print(case_count_data.head(1))

# Output list of sequence identifiers.

