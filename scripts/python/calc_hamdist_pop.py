#!/usr/bin/env python3
import sys
import os
import argparse
import statistics

#Usage: python calc_hamdist_pop.py mutations_parsed.tsv subsampled_ids.txt

#Function for calculating the hamming distance between two seqs. Simply calculates the number of SNPs that are not shared between the two genomes
def get_pairwise_hamdist(seq1,seq2):
    seq1_list = seq1.split(";")
    seq2_list = seq2.split(";")
    mut_diff = dict()
    for mut in seq1_list:
        if mut not in seq2_list:
            mut_diff[mut] = 1
    for mut in seq2_list:
        if mut not in seq1_list:
            mut_diff[mut] = 1
    tot_diff = len(mut_diff)
    return(tot_diff)

def get_pop_pairwise_hamdist(pop_ids):
    mut_dat_pop = {key: mut_dat_dict[key] for key in pop_ids} #Subset for mut-data corresponding to population
    pop_id_list = list(mut_dat_pop.keys())
    all_dist = list()
    for id1 in pop_id_list:
        for id2 in pop_id_list:
            if int(id1) < int(id2): 
                ham_dist = get_pairwise_hamdist(mut_dat_pop[id1],mut_dat_pop[id2])
                all_dist.append(ham_dist)          
    pop_dist_mean = statistics.mean(all_dist)
    return(pop_dist_mean)

id_list = ["1023555","1023556","1023557","1023558"]

#Open parsed mutations file, and store data in dictionary
fh_file = open(sys.argv[1])
mut_dat_dict = dict() #id - mut_string
line_count = 0
for line in fh_file:
    line = line.strip()    
    if line_count == 0:
        line_count += 1
    else:
        split_line = line.split("\t")
        id = split_line[0]
        mut_string = split_line[1]
        mut_dat_dict[id] = mut_string
fh_file.close()

#Open temp-file containing subset ids for population diversity calculation


get_pop_pairwise_hamdist(id_list)
temp = get_pop_pairwise_hamdist(id_list)
print(temp)
#print(temp)
