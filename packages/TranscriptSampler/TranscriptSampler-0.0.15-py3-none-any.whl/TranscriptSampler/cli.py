import matplotlib.pyplot as plt
import numpy
import os
import pathlib
import random, string
from random import choices
import re

import click


"""
run this file with the rather long command below on the command line in the dictionary of this file

command (only works with "pip install -e ." for now)
TranscriptSampler
(you may add further arguments, in the order specified by the click code below)

!!
This bullshit kind of entry point mechanism is not at all working, so I commented it out in the setup.py file
-> call file in normal python manner:
python3 path/to/module/filename functionname()
"""


# helper function to create random words
def randomword(length):
   letters = string.ascii_lowercase
   actual_length = numpy.random.randint(low = 3, high = length, size = 1)[0]
   return(''.join(random.choice(letters) for i in range(actual_length)))


# helper function
def dictToList(dict):
    objects = []
    weights = []
    for object, weight in sorted(dict.items()):
        objects.append(object)
        weights.append(weight)

    return(objects, weights)


# create a file with random gene names and random transcription numbers
def create_gene_file(name, directory, number):
    
    file_name = os.path.join(directory, name)
    
    with open(file_name, "a") as file:
        
        for i in range(number):
            string = "{} {} \n".format(randomword(6), numpy.random.randint(low = 10, high = 1000, size = 1)[0])
            file.write(string)
        
    return(file_name)


# convert the file with gene names and transcription numbers into a dict
def read_avg_expression(file):
    dict_transcr = {}
    with open(file, "r") as dafile:
        data = dafile.readlines()
        for i in range(len(data)):
            data[i] = data[i].strip()
            number = int(re.findall(r'\d+', data[i])[0]) # goofy
            gene = data[i].split()[0]
            dict_transcr[gene] = number

    return(dict_transcr)


# probabilistically sample from the gene transcripts
def sample_transcripts(avgs, number):
    objects, weights = dictToList(avgs)
    sample_array = choices(population = objects,
                           weights = weights,
                           k = number)
    
    unique, counts = numpy.unique(sample_array, return_counts=True)
    
    new_dict = {key : value for key, value in zip(list(unique), list(counts))}
    
    return(new_dict)
    
    
    
# write the sampled dict into a file with chosen name
@click.command()
@click.argument("raw_file_name", default = "transcripts_numbers.txt")
@click.argument("sampled_file_name", default = "sampled_transcripts.txt")
@click.argument("number_genes", default = 20)
@click.argument("number_sampled", default = 1000)
@click.argument("directory", default = str(pathlib.Path().resolve()))
def write_sample(raw_file_name, sampled_file_name, number_genes, number_sampled, directory):
    
    file_name = os.path.join(directory, sampled_file_name)
    file = create_gene_file(raw_file_name, directory, number_genes)
    number_dict = read_avg_expression(file)
    sampled_dict = sample_transcripts(number_dict, number_sampled)
    
    with open(file_name, "w") as file:
        file.write(str(sampled_dict))
        
    return(file_name)