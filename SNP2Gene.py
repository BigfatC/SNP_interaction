#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: SNP2Gene.py
@time: 19-5-30 下午10:11
"""
import json
import requests, sys, re
import argparse

parser = argparse.ArgumentParser(description="Annotation of Variations.")
parser.add_argument("afp", help = "Annotation File Path URL",
                    default = "./Annotation/")
parser.add_argument("-f", "--file", help ="Input File")
parser.add_argument("-o", "--output", help ="Output File")

parser.add_argument("-t","--type",type=int,choices=[0,1],
                    help = "Type of Input File: 0 positional 1 id ;default 0",
                    default = 0)
args = parser.parse_args()

AnnotationURL = args.afp
FilePath = args.file
TypeofFile = args.type
OutputPath = "Gene_nect.txt"
MidianPath = args.output
Output = open(OutputPath,'w+')
Mid = open(MidianPath,'w+')

# Important Annotation file position
SNPid_URL = AnnotationURL + "snpid2pos.txt"



# Transfer symbol on other databases to ensembl id
def symbol2eid(symbolname):
    server = "https://rest.ensembl.org"+"/xrefs/symbol/homo_sapiens/"+symbolname+"?"
    r = requests.get(server, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.json()
    print(repr(decoded))

# Transfer ensemble id to features
# You can select feature from gene,motif,cds
def id2feature(idnum , ext):
    server = "https://rest.ensembl.org/overlap/id/"+idnum+"?feature="
    for i in range(len(ext)):
        r = requests.get(server+ext[i],headers={"Content-Type" : "application/json"})
        if not r.ok:
            r.raise_for_status()
            sys.exit()
        decoded = r.json()
        print(repr(decoded))

def region2feature(region , ext):
    """
    Input the position in genome and get its feature like genes/trancripts/promoter etc
    :param region: POS like 17:17459678-17459699
    :param ext: The Feature You wanna to discover
    :return: The Feature that u got, the format of individual annotation is divided by ">"
    """
    server = "https://rest.ensembl.org/overlap/region/human/"+region +"?"
    for i in range(len(ext)):
        server = server + "feature=" + ext[i] + ";"

    server = server[:-1]
    #print(server)
    r = requests.get(server,headers={"Content-Type" : "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.content.decode()
    dict_decoded = json.loads(decoded)
    if len(dict_decoded):
        len_dict = len(dict_decoded)
        for i in range(len_dict):
            if dict_decoded[i]['feature_type'] == "gene":
                ID = dict_decoded[i]['gene_id']
                start = dict_decoded[i]['start']
                end = dict_decoded[i]['end']
                name = dict_decoded[i]['external_name']
                biotype = dict_decoded[i]['biotype']
                chr = dict_decoded[i]['seq_region_name']
                des = dict_decoded[i]['description']
                print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}".\
                      format(ID,name,chr,start,end,biotype,des),file = Output)
                return(name)

            if dict_decoded[i]['feature_type'] == "regulatory":
                ID = dict_decoded[i]['id']
                chr = dict_decoded[i]['seq_region_name']
                start = dict_decoded[i]['start']
                end = dict_decoded[i]['end']
                des = dict_decoded[i]['description']
                feature_type = dict_decoded[i]['feature_type']
                print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".\
                      format(ID,chr,start,end,feature_type,des),file = Output)
                return(None)
    else:
        print("No match")

def gene2generelate(gene1,gene2):
    """
    Using String Database to get the gene-gene interaction
    :param gene1: The first gene
    :param gene2: The corresponding second gene
    :return:
    """
    server = "https://string-db.org/api/json/network?identifiers=" +\
        gene1 + "%0D" + gene2
    r = requests.get(server)
    if not r.ok:
        r.raise_for_status()
        sys.exit()
    decoded = r.content.decode()
    dict_decoded = json.loads(decoded)
    if len(dict_decoded):
        ID1 = dict_decoded[0]['stringId_A']
        ID2 = dict_decoded[0]['stringId_B']
        score = dict_decoded[0]['score']
        ns = dict_decoded[0]['nscore']
        fs = dict_decoded[0]['fscore']
        ps = dict_decoded[0]['pscore']
        ass = dict_decoded[0]['ascore']
        es = dict_decoded[0]['escore']
        ds = dict_decoded[0]['dscore']
        ts = dict_decoded[0]['tscore']
        print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}".\
            format(ID1,ID2,score,ns,fs,ps,ass,es,ds,ts),file=Output)
    else:
        print("The String Database: None Results",file=Output)

### Transfer SNP rs id to its position
def SNPID2POS(SNPID):
    temp_file = open(SNPid_URL)
    try:
        for oneline in temp_file:
            if (re.search(SNPID,oneline)):
                    array = re.split('\s+',oneline)
                    if array[3] == SNPID:
                        query_region = re.split('\W+',oneline)
                        region = query_region[0].strip('chr')+":"+ \
                                 query_region[1]+"-"+query_region[2]
                        return region
    finally:
        temp_file.close()

def RegionFormat(Region):
    """
    Convert 19 175678 175698 to 19:178678-175698
    :param Region: Original Region
    :return: Output Format Region
    """
    query_region = re.split('\W+', Region)
    FormatRegion = []
    temp1 = query_region[0].strip('chr')+":"+ \
            query_region[1]+ "-" + query_region[2]
    temp2 = query_region[3].strip('chr')+":"+ \
           query_region[4] + "-" + query_region[5]
    FormatRegion.append(temp1)
    FormatRegion.append(temp2)
    return FormatRegion


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
                        print("{0}\t{1}".format(array[0],array[1]),file = Output)

def pathwayontology(gene1,gene2):
    TraversingFile(gene1,gene2,"reactome_gg.txt")
    TraversingFile(gene1,gene2,"go_gg.txt")
    TraversingFile(gene1,gene2,"kegg_gg.txt")



def main():
    ext = ("gene","regulatory","transcript","cds","motif")
    inputfile = open(FilePath)

    for oneline in inputfile:
        # First Input the gene information
        if (TypeofFile == 1):
            tempid = re.split("\W+",oneline)
            region = SNPID2POS(tempid[0])

        else:
            region = RegionFormat(oneline)

        print(region,file=Mid)


    #gene2generelate("CLN6","CLN8")
    Output.close()


if __name__ == "__main__":
    sys.exit(main())