import matplotlib.pyplot as plt
import numpy
import os
import pathlib
import random, string
from random import choices
import re

from helper_functions import randomword, dictToList, create_gene_file, read_avg_expression, sample_transcripts, write_sample


class TranscriptSampler:
    
    raw_file_name = "genes_numbers.txt"
    sampled_file_name = "affe.txt"
    number_genes = 20
    number_sampled = 1000

    
    def __init__(self, raw_file_name, sampled_file_name, number_genes, number_sampled):
        self.raw_file_name = raw_file_name
        self.sampled_file_name = sampled_file_name
        self.number_genes = number_genes
        self.number_sampled = number_sampled
        self.directory = str(pathlib.Path().resolve())
    
    # create file
    def get_gene_file(self):
        self.gene_file = create_gene_file(self.raw_file_name, self.directory, self.number_genes)
        return(self.gene_file)

    # get the dict containing the data
    def get_average_expression(self):
        self.avg_dict = read_avg_expression(self.get_gene_file())
        return(self.avg_dict)

    # sample transcripts from genes
    def get_sample_transcripts(self):
        self.sampled_dict = sample_transcripts(self.get_average_expression(), self.number_sampled)
        return(self.sampled_dict)
    
    # write the sampled dict into a file with chosen name
    def get_sampled_file(self):
        self.final_file = write_sample(str(self.get_sample_transcripts()), self.directory, self.sampled_file_name)
        return(self.final_file)
    
    

    
transcripts = TranscriptSampler(raw_file_name = "genes_numbers.txt",
                                sampled_file_name = "affe.txt",
                                number_genes = 20,
                                number_sampled = 1000)

