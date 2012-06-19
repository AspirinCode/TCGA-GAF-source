#!/usr/bin/env python

import argparse
import Gaf
import re
import sys

            

parser = argparse.ArgumentParser()
parser.add_argument('miRnaGaf', type=str, help="miRNA GAF file")
parser.add_argument('preMiRnaGaf', type=str, help="pre-miRNA GAF file")
parser.add_argument("-n", dest="entryNumber", help="Initial entry number",
                    default=0)
args = parser.parse_args()

entryNumber = args.entryNumber

#
# First, read the pre-miRna GAF data into a dictionary.  
preMiRnas = dict()
preMiRnaGafFp = open(args.preMiRnaGaf)
for line in preMiRnaGafFp:
    preMiRnaGaf = Gaf.Gaf(line)
    preMiRnas[preMiRnaGaf.featureId] = preMiRnaGaf
preMiRnaGafFp.close()


#
# Next, read the uncombined miRNA GAF data.  For each miRNA,
# look up its parent pre-miRNA from the dictionary and generate
# a mapping.
miRnaFp = open(args.miRnaGaf)
for line in miRnaFp:
    miRnaGaf = Gaf.Gaf(line)
    preMiRnaId = miRnaGaf.featureInfo.split("pre-miRNA=")[1]
    assert preMiRnas.has_key(preMiRnaId)
    preMiRnaGaf = preMiRnas[preMiRnaId]
    miRnaToPreMiRna = Gaf.FeatureToCompositeGaf()
    miRnaToPreMiRna.assign(miRnaGaf, preMiRnaGaf)
    miRnaToPreMiRna.featureInfo = ""
    entryNumber = entryNumber + 1
    miRnaToPreMiRna.entryNumber = entryNumber
    miRnaToPreMiRna.write(sys.stdout)
exit(0)
