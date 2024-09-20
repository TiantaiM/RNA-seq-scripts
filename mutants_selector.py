# This script select sncRNA mutant reads from a taildata csv file

import csv
import argparse
import re


def arg_parser():
    parser = argparse.ArgumentParser(description="Counting unique or multi_aligned mutants \
                                 from a taildata csv file. Highly specific to JLA taildata pipeline.")
    parser.add_argument('-E', type=str, dest='experiment_manifest', help="List of experiments")
    parser.add_argument('-G', type=str, dest="gene_manifest", help="List of genes")
    # parser.add_argument("OutFile")
    # parser.add_argument("OutFile_multi")
    return parser.parse_args()

def read_exp_manifest(exp_file):
    with open (exp_file, 'r') as exp:
        next(exp)
        exp_list = {}
        for line in exp:
            line = line.strip().split(',')
            exp_list[line[0]] = line[1]
    return exp_list

def read_gene_manifest(gene_file):
    with open (gene_file, 'r') as gene:
        next(gene)
        gene_list = {}
        for line in gene:
            line = line.strip().split(',')
            gene_list[line[0]] = line[1]
    return gene_list

def select_mutants(exp_list, gene_list):
    for exp_id, exp_name in exp_list.items():
        for gene_id, gene_name in gene_list.items():
            with open (f'{exp_name}', 'r') as in_file, \
            open(f'{exp_id}_{gene_name}_counts_summary.csv','w') as out_file, \
            open(f'{exp_id}_{gene_name}_multi_counts_summary.csv','w') as out_file_multi:
                reader = csv.reader(in_file)
                writer = csv.writer(out_file)
                writer_multi = csv.writer(out_file_multi)
                header = next(reader)
                writer.writerow(header)
                writer_multi.writerow(header)
                for row in reader:
                    if re.search(gene_id, row[2]):
                        if len(row[2].split(',')) == 1:
                            writer.writerow(row)
                        else:
                            writer_multi.writerow(row)

############# main #############

args = arg_parser()
exp_list = read_exp_manifest(args.experiment_manifest)
gene_list = read_gene_manifest(args.gene_manifest)
select_mutants(exp_list, gene_list)

if __name__ == "__main__":
    pass


