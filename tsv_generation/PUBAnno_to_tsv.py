import sys
import json
import csv
import os
from os.path import isfile, join


"""
This script reads a folder of PUBAnnotated json files (dir_path)
to convert to test.tsv file with tokens ready for Relation extraction.

The obj in the pubannotations needs to be correctly named according to 
Relation extraction tokens (gene, desease etc.) or it needs to be taken care of in the get_text_with_token-function
"""

def get_text_with_token(json_file):
    data = json.load(json_file)
    for denotation in reversed(data['denotations']):    #Reversed so changes dont 
        start = denotation['span']['begin']     #Start index of entity
        end = denotation['span']['end']         #End index of entity
        data['text'] = data['text'][:start] + '@' + denotation['obj'].upper() + '$ ' + data['text'][end:]   #replace entity with @"obj"$
    return data['text']


dir_path = '../output_generation/test_folder/'

with open('../output_generation/test_folder/generated_test.tsv', 'w') as out_file:
    index = 0
    out_file.write('index\tsentence\tlabel\n')      #First row of test.tsv file
    for json_file_name in os.listdir(dir_path):     #Loop through all json files in directory
        with open(dir_path + json_file_name) as json_file:
            sentences = get_text_with_token(json_file).split(' . ') #split on " . " to divide running text into sentences
            for sentence in sentences:
                out_file.write(str(index) + '\t' + sentence + '\t' + '1\n') #write to file according to format of test.tsv for RE
                index += 1  #increase index for each row/sentence sentence




"""
with open('generated_test.tsv', 'w') as out_file:
    with open(../ + 'meta_subset_100.csv') as meta_data_file:
"""