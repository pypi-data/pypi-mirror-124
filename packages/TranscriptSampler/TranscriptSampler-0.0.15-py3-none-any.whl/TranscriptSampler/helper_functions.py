import matplotlib.pyplot as plt
import numpy
import os
import pathlib
import random, string
from random import choices
import re


# helper function to create random words
def randomword(length):
   letters = string.ascii_lowercase
   actual_length = numpy.random.randint(low = 3, high = length, size = 1)[0]
   return ''.join(random.choice(letters) for i in range(actual_length))


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
    

def plot_rotated(x, y):
    plt.rcdefaults()
    fig, ax = plt.subplots()
    y_pos = numpy.arange(len(x))
    number = y

    ax.barh(y_pos, number, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(x)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('# of gene transcripts')

    plt.show()
    
    
# write the sampled dict into a file with chosen name
def write_sample(dic, directory, name):
    
    file_name = os.path.join(directory, name)
    
    with open(file_name, "w") as file:
        file.write(dic)
        
    return(file_name)
    
    
    
# create file
def get_gene_file(raw_file_name, directory, number_genes):
    gene_file = create_gene_file(raw_file_name, directory, number_genes)
    return(gene_file)

# get the dict containing the data
def get_average_expression(raw_file_name, directory, number_genes):
    avg_dict = read_avg_expression(get_gene_file(raw_file_name, directory, number_genes))
    return(avg_dict)

# sample transcripts from genes
def get_sample_transcripts(raw_file_name, directory, number_genes, number_sampled):
    sampled_dict = sample_transcripts(get_average_expression(raw_file_name, directory, number_genes), number_sampled)
    return(sampled_dict)

# write the sampled dict into a file with chosen name
@click.command()
@click.argument("raw_file_name", default = "transcripts_numbers.txt")
@click.argument("sampled_file_name", default = "sampled_transcripts.txt")
@click.argument("number_genes", default = 20)
@click.argument("number_sampled", default = 1000)
def get_sampled_file(raw_file_name,
                     sampled_file_name,
                     number_genes,
                     number_sampled):
    final_file = write_sample(str(get_sample_transcripts(raw_file_name, directory, number_genes, number_sampled)),
                              directory,
                              sampled_file_name)
    print("fischkopf")
    return(final_file)