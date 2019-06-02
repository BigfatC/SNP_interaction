#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: SNPID2POS.py
@time: 19-5-30 下午11:27
"""
import json
import requests, sys, re
import argparse

parser = argparse.ArgumentParser(description="Annotation of Variations.")
parser.add_argument("afp", help = "Annotation File Path URL",
                    default = "./Annotation/")
parser.add_argument("-f", "--file", help ="Input File")
parser.add_argument("-t","--type",type=int,choices=[0,1],
                    help = "Type of Input File: 0 positional 1 id ;default 0",
                    default = 0)
args = parser.parse_args()

AnnotationURL = args.afp
FilePath = args.file
TypeofFile = args.type
MidianPath = "Position_of_snp.txt"
Mid = open(MidianPath,'w+')

# Important Annotation file position
SNPid_URL = AnnotationURL + "snpid2pos.txt"

### Transfer SNP rs id to its position
def SNPID2POS(SNPID):
    temp_file = open(SNPid_URL)
    lens = len(SNPID)
    #print(lens)
    count = 0
    try:
        for oneline in temp_file:
            for i in range(lens):
                if (re.search(SNPID[i],oneline)):
                    array = re.split('\s+',oneline)
                    if array[3] == SNPID[i]:
                        query_region = re.split('\W+',oneline)
                        region = query_region[0].strip('chr')+":"+ \
                                 query_region[1]+"-"+query_region[2]
                        count += 1
                        print(region,file=Mid)
                if count == lens:
                    return
    finally:
        temp_file.close()

def main():
    inputfile = open(FilePath)
    tempid = []
    for oneline in inputfile:
        oneline = oneline.strip()
        # First Input the gene information
        tempid.append(oneline)
    #print(tempid[1])
    SNPID2POS(tempid)

    Mid.close()

if __name__ == "__main__":
    sys.exit(main())