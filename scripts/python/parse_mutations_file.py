#!/usr/bin/env python3
import sys
import os
import argparse
from datetime import datetime
import os.path
from os import path
import statistics

#Example usage: python parse_mutations_file.py -m mutations_snpeff_annotated_tidy_Denmark.tsv -o parsed_mut_210821.tsv


#Function for parsing out nucleotide substitutions per id from mutations-file
def format_data(file):
    mut_dict = dict()
    try:
        fh_file = open(file)
    except:
        print("cant open mutation-file, exiting script!")
        exit()
    line_count = 0
    for line in fh_file:
        split_line = line.split("\t")
        if line_count == 0:
            line_count += 1
        else:
            id = split_line[0]
            if id not in mut_dict:
                mut_dict[id] = dict()
            position = split_line[2]
            ref_base = split_line[3]
            variant_base = split_line[4]
            mut_string = ref_base + position + variant_base
            if mut_string not in mut_dict[id]:
                mut_dict[id][mut_string] = 1
    return(mut_dict)
       
    
#Read user arguments
parser = argparse.ArgumentParser()
parser.add_argument('-m', metavar="mutations_file", required=True, help="Name of file with mutation data")
parser.add_argument('-o', metavar="outfile", required=True, help="Name of outfile")
args = vars(parser.parse_args())
if (args['m']):
    mut_file = args['m']
if (args['o']):
    outfile = args['o']
    

data_parsed = format_data(mut_file)
fh_out = open(outfile,'w')
fh_out.write("ID\tmut\n")
for id in data_parsed.keys():
    id_mut = list(data_parsed[id].keys())
    mut_str = ";".join(id_mut)
    line_out = list()
    line_out.append(id)
    line_out.append(mut_str)
    line_out_str = "\t".join(line_out)
    fh_out.write(line_out_str + "\n")
fh_out.close()
    