# TITLE: Calculate weekly diversity.

import calc_hamdist_pop
import yaml
import pandas as pd
from datetime import timedelta
import csv
import tqdm

# Parse configurations: date range
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)
path_to_data = config['path_to_data']
min_date = config['min_date']
max_date = config['max_date']
country = config['country']

# Import genome IDs to analyze
ids = pd.read_csv("temp/subsampled_ids.csv")

# Import dictionary with mutations by sample
mut_dat_dict = calc_hamdist_pop.load_mut_dat_dict()

# Import metadata for genome dates
metadata = pd.read_csv(path_to_data + "/metadata_snpeff_tidy_" + str.replace(country, " ", "_") + ".tsv", low_memory=False, sep='\t')
metadata['Collection date'] = pd.to_datetime(metadata['Collection date'])
metadata = metadata[metadata['id'].isin(ids['id'])]


def get_ids_binned_weekly():
    ids_by_week = {}
    metadata['week'] = metadata['Collection date'].map(lambda x: pd.Timestamp.isocalendar(x)[1])
    metadata['year'] = metadata['Collection date'].map(lambda x: pd.Timestamp.isocalendar(x)[0])
    for index, row in metadata.iterrows():
        year_week = (row['year'], row['week'])
        id = row['id']
        if year_week not in ids_by_week:
            ids_by_week[year_week] = [id]
        else:
            ids_by_week[year_week].append(id)
    return ids_by_week


def get_ids_binned_roll_weekly():
    ids_by_week = {}
    for index, row in metadata.iterrows():
        start_date = row['Collection date']
        id = row['id']
        for i in range(0,7):
            date = start_date + timedelta(days=i)
            if date not in ids_by_week:
                ids_by_week[date] = [id]
            else:
                ids_by_week[date].append(id)
    return ids_by_week


# Create a dictionary with ids by week
ids_by_week = get_ids_binned_roll_weekly()

# For each week, calculate diversity
diversity_by_time = {}
for year_week, ids in tqdm.tqdm(ids_by_week.items()):
    if len(ids) > 1:
        diversity_by_time[year_week] = calc_hamdist_pop.get_pop_pairwise_hamdist(pop_ids=map(str, ids), mut_dat_dict=mut_dat_dict)
    else:
        diversity_by_time[year_week] = None

# Write out to file
with open("temp/diversity_by_time.csv", "w") as diversity_outfile:
    writer = csv.writer(diversity_outfile)
    writer.writerow(['date', 'diversity_measure'])
    for date, diversity in diversity_by_time.items():
        writer.writerow([date, diversity])

print("Finished!")
