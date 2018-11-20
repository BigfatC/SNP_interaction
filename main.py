#!/usr/bin/python3
# encoding: utf-8
"""
@author: Erin Cai
@contact: charlottecaiir@gmail.com
@file: main.py
@time: 18-11-6 下午1:30
"""
import json
import requests, sys, re
import getopt

"""
opts,args = getopt.getopt(sys.argv[1:],'-h-f:',['help','filepath='])
for opt_name,opt_value in opts:
  if opt_name in ('-h','--help'):
    usage()
    exit

def usage():
"""

# Important Annotation file position
SNPid_URL = "/home/erincai/Project/Annotation/snpid2pos.txt"

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
  server = "https://rest.ensembl.org/overlap/region/human/"+region+"?feature="
  for i in range(len(ext)):
    r = requests.get(server+ext[i],headers={"Content-Type" : "application/json"})
    if not r.ok:
      r.raise_for_status()
      sys.exit()
    decoded = r.json()
    print(repr(decoded))

### Transfer SNP rs id to its position
def SNPID2POS(SNPID):
  temp_file = open(SNPid_URL)
  try:
    for oneline in temp_file:
      if (re.search(SNPID,oneline)):
        query_region = re.split('\W+',oneline)
        region = query_region[0].strip('chr')+":"+\
                 query_region[1]+"-"+query_region[2]
        return region
  finally:
    temp_file.close()

### Identify if he is given rs id or


def main(argv=None):

  ext = ("gene","motif")
  idnum = "rs429358"
  region = "19:44908684-44908684"
  #id2feature(idnum,ext)
  #region2feature(region,ext)
  region = SNPID2POS(idnum)

  region2feature(region,ext)


if __name__ == "__main__":
    sys.exit(main())


"""
server = "https://rest.ensembl.org"
ext1 = "/overlap/region/human/7:17459699-17459699?feature=motif"
ext2 = "/overlap/region/human/7:1745977-1745977?feature=motif"

r1 = requests.get(server+ext1, headers={ "Content-Type" : "application/json"})
r2 = requests.get(server+ext2, headers={ "Content-Type" : "application/json"})
if not r1.ok:
  r1.raise_for_status()
  sys.exit()


decoded1 = r1.json()
print(repr(decoded1))
if (decoded1 == None):
  print("Sorry Woops~")

r_decoded1 = r1.content.decode()

decoded2 = r2.json()
print(repr(decoded2))

r_decoded2 = r2.content.decode()

dict_decoded1 = json.loads(r_decoded1)
print(type(dict_decoded1))

dict_decoded2 = json.loads(r_decoded2)

dict_decoded1 = dict_decoded1 + dict_decoded2

for i in range(len(dict_decoded1)):
  if(dict_decoded1[i]['biotype']=="stable_id"):
    print(dict_decoded1[i])


"""
