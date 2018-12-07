#!/usr/bin/env python3
import argparse  # command line options

# Title: filterFastaById.py
# Created: 7-Dec-2018

# Context:      I have RNA-seq nanopore long reads of a Vargula organism that are corrected (by canu) and clustered
#               (by CD-HIT-EST). Via blastn, I discovered hits from E.coli that can be safely assumed to be
#               contamination. I have already identified a set of 3000 ids that correspond to E.coli sequences.
#               I need to find these ids in the clustered reads fasta and remove them.


def process_fasta(in_fasta, out, target):
    # Process fasta file by filtering out records matching target IDs of interest and recording the remaining records
    write_seq = False
    with open(out, 'w') as outfile:
        with open(in_fasta, 'r') as f:
            for count, line in enumerate(f):  # Read line by line while keeping track of line number
                if count % 2 == 0:  # Header line: Line number is even (includes first line which is a header)
                    line_split = line.rstrip().split()
                    fasta_id = line_split[0].replace('>', '')  # remove the '>' symbol that starts a fasta header
                    if fasta_id not in target:  # check if fasta_id matches with an E.coli id. If not, keep record
                        outfile.write(line)
                        write_seq = True
                else:  # Sequence line: Line number is odd in a fasta file
                    if write_seq == True:
                        outfile.write(line)
                        write_seq = False

    return


def read_target_file(target):
    # Read in target file containing record ids and save as a list
    target_ids = []
    with open(target, 'r') as target_fh:
        for target_id in target_fh:
            target_ids.append(target_id.rstrip())  # Each line in the target file is an id. Save these ids.

    return target_ids


def main():
    # Main function
    parser = argparse.ArgumentParser(description='')
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument("-fasta", help='Fasta with clustered reads and their ids', required=True, metavar='')
    required_group.add_argument("-target", help='List of ids associated with filter target', required=True, metavar='')
    required_group.add_argument("-out", help='Output file path', required=True, metavar='')

    args = parser.parse_args()

    target_ids = read_target_file(target=args.target)
    process_fasta(in_fasta=args.fasta, out=args.out, target=target_ids)

    return


if __name__ == "__main__":
    main()





