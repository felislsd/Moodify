#!/usr/bin/python3

import re

def remove_rows_ending_with_zero(input_file, output_file):
    # Define the regex pattern to match lines ending with ": 0"
    pattern = re.compile(r'.*: 0$')

    # Read the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Filter lines that do not end with ": 0"
    filtered_lines = [line for line in lines if not pattern.search(line)]

    # Write the filtered lines to the output file
    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)

# Specify the input and output file names
input_file = 'genre_counts.txt'
output_file = 'genre_counts_non_zero.txt'

# Call the function to remove rows ending with zero
remove_rows_ending_with_zero(input_file, output_file)