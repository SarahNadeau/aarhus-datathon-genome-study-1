# TITLE: Subsample sequences.
# INPUT: Sequence metadata from GISAID provided by datathon organizers, OWID full dataset.
# OUTPUT: List of sequence identifiers.

import os
import yaml
import pandas as pd
import numpy as np

# Creat temp directory to store intermediate results
try:
    os.mkdir("temp")
except FileExistsError:
    pass

# Parse configurations: country, lineages, date range, weekly proportion of cases to take.
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
path_to_data = config['path_to_data']
country = config['country']
country_code = config['country_code']
pangolin_lineages = config['pangolin_lineages']
min_date = config['min_date']
max_date = config['max_date']
subsampling_proportion = config['subsampling_proportion']

# Import sequence metadata.
metadata = pd.read_csv(path_to_data + "/metadata_snpeff_tidy_" + str.replace(country, " ", "_") + ".tsv", low_memory=False, sep='\t')

# Import case count data
case_count_data = pd.read_csv(path_to_data + "/owid-covid-data.csv")

# Import mutations file
mutations = pd.read_csv(path_to_data + "/mutations_snpeff_annotated_tidy_" + str.replace(country, " ", "_") + ".tsv", sep='\t')

# Filter case count data by country, date range
case_count_data['date'] = pd.to_datetime(case_count_data['date'])
case_count_data = case_count_data[case_count_data['iso_code'] == country_code]
case_count_data = case_count_data[case_count_data['date'] <= pd.to_datetime(max_date)]
case_count_data = case_count_data[case_count_data['date'] >= pd.to_datetime(min_date)]

# Filter genome metadata by country, date range, host, presence in mutation data
metadata['Collection date'] = pd.to_datetime(metadata['Collection date'])
metadata = metadata[metadata['country'] == country]
metadata = metadata[metadata['Collection date'] <= pd.to_datetime(max_date)]
metadata = metadata[metadata['Collection date'] >= pd.to_datetime(min_date)]
metadata = metadata[metadata['Host'] == 'Human']
metadata = metadata[metadata['id'].isin(mutations['id'])]

# Calculate upper-bound number of sequences to take per week
metadata['week'] = metadata['Collection date'].map(lambda x: pd.Timestamp.isocalendar(x)[1])
metadata['year'] = metadata['Collection date'].map(lambda x: pd.Timestamp.isocalendar(x)[0])
case_count_data['week'] = case_count_data['date'].map(lambda x: pd.Timestamp.isocalendar(x)[1])
case_count_data['year'] = case_count_data['date'].map(lambda x: pd.Timestamp.isocalendar(x)[0])

# Generate set of year, week tuples from filtered metadata
year_weeks = set()
for index, row in metadata.iterrows():
    year_weeks.add((row['year'], row['week']))

# Subsample genomes based on confirmed cases per year, week
sampled_ids = []
subsampling_outfile = open("temp/subsampling_summary.csv", "w")
subsampling_outfile.write('year,week,n_cases,n_genomes_total,n_genomes_sampled_total,n_genomes_analyzed_focal_lineages\n')
for year_week in year_weeks:
    # Get number of cases that week
    case_counts = case_count_data[case_count_data['year'] == year_week[0]]
    case_counts = case_counts[case_counts['week'] == year_week[1]]
    n_cases = case_counts['new_cases'].sum()

    # Get genomes from that week
    genomes = metadata[metadata['year'] == year_week[0]]
    genomes = genomes[genomes['week'] == year_week[1]]
    n_genomes_total = genomes.shape[0]

    # Sample from all genomes based on cases
    genomes = genomes.sample(frac=1)  # shuffle genomes
    n_to_sample = int(np.floor(min(n_genomes_total, n_cases * subsampling_proportion)))
    genomes = genomes.head(n_to_sample)
    n_genomes_sampled_total = genomes.shape[0]

    # Select only genomes from lineage(s) of interest
    genomes = genomes[genomes['pangolin_lineage'].isin(pangolin_lineages)]
    n_genomes_analyzed_focal_lineages = genomes.shape[0]
    sampled_ids = sampled_ids + genomes['id'].astype('string').tolist()

    subsampling_outfile.write('{},{},{},{},{},{}\n'.format(
        year_week[0],
        year_week[1],
        n_cases,
        n_genomes_total,
        n_genomes_sampled_total,
        n_genomes_analyzed_focal_lineages))

subsampling_outfile.close()

# Output list of sequence identifiers.
ids_outfile = open("temp/subsampled_ids.csv", "w")
ids_outfile.write("id\n")
ids_outfile.write('\n'.join(sampled_ids))
ids_outfile.close()

print("Finished subsampling genome ids!")