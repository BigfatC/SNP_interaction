#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: POS2Gene.py
@time: 19-5-31 下午11:43
"""
import json
import requests, sys, re
import argparse
import time
parser = argparse.ArgumentParser(description="Annotation of Variations.")
parser.add_argument("afp", help = "Annotation File Path URL",
                    default = "./Annotation/")
parser.add_argument("-f", "--file", help ="Input File")
parser.add_argument("-o", "--outfile", help ="Output File")
args = parser.parse_args()

AnnotationURL = args.afp
FilePath = args.file

OutputPath = args.outfile
Output = open(OutputPath,'w+')


def region2feature(name ,region , ext):
    """
    Input the position in genome and get its feature like genes/trancripts/promoter etc
    :param region: POS like 17:17459678-17459699
    :param ext: The Fature You wanna to discover
    :return: The Feature that u got, the format of individual annotation is divided by ">"
    """
    if region == "None":
        print("No Annotation",file=Output)
        return
    print(">"+name+","+region,file=Output)
    #Configuration of request for location.
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
    print(len(dict_decoded))
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

            elif dict_decoded[i]['feature_type'] == "regulatory":
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
        print("No Match",file= Output)

def regulatory_detailed(ENSRID,Tissue):
    server = "https://rest.ensembl.org/regulatory/species/homo_sapiens/id/"+ENSRID +"?activity=1"
    r = requests.get(server,headers={"Content-Type" : "application/json"})
    if not r.ok:
        r.raise_for_status()

    decoded = r.content.decode()

    dict_decoded = json.loads(decoded)

    ###Given values
    des = dict_decoded[0]['description']
    start = dict_decoded[0]['start']
    end = dict_decoded[0]['end']
    activity = dict_decoded[0]['activity'][Tissue]
    return activity

def regulatory_detailed(ENSRID,Tissue):
    server = "https://rest.ensembl.org/regulatory/species/homo_sapiens/id/"+ENSRID +"?activity=1"
    r = requests.get(server,headers={"Content-Type" : "application/json"})
    if not r.ok:
        r.raise_for_status()

    decoded = r.content.decode()

    dict_decoded = json.loads(decoded)

    ###Given values
    des = dict_decoded[0]['description']
    start = dict_decoded[0]['start']
    end = dict_decoded[0]['end']
    activity = dict_decoded[0]['activity'][Tissue]
    return activity

def main():
    input = open(FilePath)
    ext = ("gene","regulatory","motif")
    for oneline in input:
        oneline = oneline.strip()
        array = re.split('\s+',oneline)
        region2feature(array[0],array[1],ext)
        time.sleep(0.5)

    Output.close()

if __name__ == "__main__":
    sys.exit(main())
