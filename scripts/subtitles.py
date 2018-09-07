#!/usr/bin/env python
import sys

input_file = open(sys.argv[1]).readlines()
output_file = open(sys.argv[2], 'w')

for line in input_file:
    start_index = line.find('{*}')

    if start_index == -1:
        output_file.write(line)
    else:
        change = True
        while change:
            temp = line[start_index + 3:]
            med_index = temp.find('{*')
            if med_index != -1:
                old_text = temp[:med_index]
                end_index = temp.find('}')
                if end_index != -1:
                    new_text = temp[med_index + 2:end_index]

                    temp = new_text + temp[med_index:med_index+2] + old_text + temp[end_index:]

                    line = line[:start_index + 3] + temp
                    temp = temp[end_index + 1:]

                    start_index = start_index + end_index + 1
                    next_synt = temp.find("{*}")
                    start_index = start_index + next_synt + 3

                    change = False if next_synt == -1 else True
                else:
                    change = False
            else:
                change = False

        output_file.write(line)

output_file.close()
