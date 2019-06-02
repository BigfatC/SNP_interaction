#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: Gene2Pathway.py
@time: 19-6-2 下午10:18
"""
import json
import requests, sys, re
import argparse

parser = argparse.ArgumentParser(description="Genes to Pathway Annotations")
parser.add_argument("afp", help = "Annotation File Path URL",
                    default = "./Annotation/")
parser.add_argument("-f", "--file", help ="Input File")
parser.add_argument("-o", "--out", help ="Output File")
args = parser.parse_args()

input = args.file
output = args.out
AnnotationURL = args.afp
inpf=open(input,'r')
outf=open(output,'w+')



def TraversingFile(gene1,gene2,AnnoURL):
    AnnoFile = open(AnnotationURL + AnnoURL)
    for oneline in AnnoFile:
        array = re.split('\t+',oneline)
        for i in range(2,len(array)):
            if gene1 == array[i]:
                for j in range(2,len(array)):
                    if gene2 == array[j]:
                        temp = oneline.replace("\n","")
                        array = re.split('\s+',temp)
                        print("{0}\t{1}".format(array[0],array[1]),file = outf)
    AnnoFile.close()

def pathwayontology(gene1,gene2):
    TraversingFile(gene1,gene2,"reactome_gg.txt")
    TraversingFile(gene1,gene2,"go_gg.txt")
    TraversingFile(gene1,gene2,"kegg_gg.txt")

def main():
    lines = inpf.readlines()
    inpf.close()
    for i in range(len(lines)):
        for j in range(len(lines)):
            gene1  = lines[i].strip()
            gene2  = lines[j].strip()
            print(">"+gene1+"&"+gene2,file=outf)
            pathwayontology(gene1,gene2)

if __name__ == "__main__":
    sys.exit(main())
