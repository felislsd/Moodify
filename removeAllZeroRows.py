#!/usr/bin/python3

import re

def remove_rows_ending_with_zero(input_file, output_file):

    pattern = re.compile(r'.*: 0$')


    with open(input_file, 'r') as file:
        lines = file.readlines()


    filtered_lines = [line for line in lines if not pattern.search(line)]


    with open(output_file, 'w') as file:
        file.writelines(filtered_lines)


input_file = 'genre_counts.txt'
output_file = 'genre_counts_non_zero.txt'


remove_rows_ending_with_zero(input_file, output_file)