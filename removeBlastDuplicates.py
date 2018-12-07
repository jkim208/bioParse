#!/usr/bin/env python3
import argparse  # command line options
import sys

# Title: removeBlastDuplicates.py
# Created: 9-Nov-2018

# Context:  My original record file is supposed to have 10 entries for each transcript (top 10 blast hits). However,
#           I ran the blast on the wrong setting by defining max_target_seqs instead of max_hsps.
#           For reference:
#               Setting -max_target_seqns to 1 will give only 1 subject/hit but several HSPs if they are present.
#               Setting -max_hsps to 1 will give only 1 HSP per subject but for all subject/hits in the database.
#               Example test case from blastn.final:
#               TRINITY_DN117148_c1_g2_i1       gi|1353793160|gb|CP027070.1|    Bos mutus isolate yakQH1 chromosome 2

# Goal: Go through each record in the file and remove all duplicate hits (with respect to gi accession)


def extract_ids(line):

    line_split = line.rstrip().split('\t')
    ids = (line_split[0], line_split[1])

    return ids


def read_and_write_txt(input, output):
    try:
        input_fh = open(input, 'r')
    except IOError:
        print("Could not open input file for reading. Ending program...")
        sys.exit()

    output_fh = open(output, 'w')
    ref_id1 = ''
    ref_id2 = ''
    counter = 0
    for line in input_fh:
        ids = extract_ids(line)
        if counter == 0:
            ref_id1 = ids[0]  # Trinity transcript name
            ref_id2 = ids[1]  # GI accession number of hit sequence
            counter += 1
            output_fh.write(line)
        else:
            if ids[0] == ref_id1 and ids[1] == ref_id2:  # Scenario where query record matches the "reference"
                # This record is redundant. Do not write to fh. Skip it.
                continue
            else:
                counter += 1
                # This record will replace the previous reference.
                ref_id1 = ids[0]  # Trinity transcript name
                ref_id2 = ids[1]  # GI accession number
                output_fh.write(line)

    print("This program wrote", counter, "blast records to", output)

    input_fh.close()
    output_fh.close()

    return


def main():
    # Main function
    parser = argparse.ArgumentParser(description='')
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument("-input", help='file containing blast output', required=True, metavar='')
    required_group.add_argument("-output", help='output file path', required=True, metavar='')

    args = parser.parse_args()

    read_and_write_txt(input=args.input, output=args.output)

    return


if __name__ == "__main__":
    main()
