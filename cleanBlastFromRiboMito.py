#!/usr/bin/env python3
import argparse  # command line options
import sys

# Title: cleanBlastFromRiboMito.py
# Created: 7-Nov-2018

# Goal: Remove all Blast transcript records associated with ribosomal or mitochondrial genes (via simple match
#       Keep the remaining transcript records in a new output file


def extract_significant_record(line, descriptionCol):

    line_split = line.rstrip().split('\t')
    junk = False

    # match to where the description should be. Subtract by 1 since python starts indices at 0
    match_obj1 = line_split[descriptionCol - 1]

    if match_obj1:

        if "ribosomal" in match_obj1 or "mitochondrial" in match_obj1 or "mitochondrion" in match_obj1:
            junk = True

    else:
        print("Description missing")

    return junk


def read_and_write_txt(input, descriptionCol, output):

    try:
        input_fh = open(input, 'r')
    except IOError:
        print("Could not open input file for reading. Ending program...")
        sys.exit()

    output_fh = open(output, 'w')

    lineCount_output = 0
    lineCount_input = 0

    for line in input_fh:

        junk = extract_significant_record(line, descriptionCol)

        if junk is False:
            output_fh.write(line)
            lineCount_output += 1

        lineCount_input += 1

    input_fh.close()
    output_fh.close()

    print("The input file had ", str(lineCount_input), " line(s).")
    print("The output file now has ", str(lineCount_output), " line(s).")
    print(str(lineCount_input - lineCount_output), " line(s) were associated with mitochondrial or ribosomal genes.")

    return


def main():
    # Main function
    parser = argparse.ArgumentParser(description='')
    required_group = parser.add_argument_group('required arguments')
    required_group.add_argument("-input", help='file containing blast output', required=True, metavar='')
    required_group.add_argument("-output", help='output file path', required=True, metavar='')
    required_group.add_argument("-descriptionCol", help='Column number containing the description of the '
                                                        'transcript. 1 = first column.',
                                required=True, metavar='', type = int)
    args = parser.parse_args()

    read_and_write_txt(input=args.input, output=args.output, descriptionCol=args.descriptionCol)

    return


if __name__ == "__main__":
    main()
