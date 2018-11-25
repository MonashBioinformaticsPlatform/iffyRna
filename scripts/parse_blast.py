#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import sys
import json

#blast json file
f = sys.argv[1]

# ok, so I think the structure is such
# each "report" holds info for a specific query
# that holds several numbers of hits.
# I need to get first (top?) hit from each report tag
# number of report should equal to number of queries
# each "report", will have "results" section

#search": {
#          "query_id": "Query_1",
#          "query_title": "chk1_product_1 Contig_65_159.103:filter(unmasked)|start|1230|length|457",
#          "query_len": 457,
#          "hits": [
#            {
#              "num": 1,
#              "description": [
#                {
#                  "id": "gi|744815412|gb|CP007774.1|",
#                  "accession": "CP007774",
#                  "title": "Campylobacter volucris LMG 24379, complete genome",
#                  "taxid": 580033,
#                  "sciname": "Campylobacter volucris LMG 24379"
#                }
#              ],

print('\t'.join(("Query", "Hit", "Taxid", "Accession", "E.value", "Score")))
with open(f) as handler:
    parsed_json = json.loads(handler.read())
    blast = parsed_json["BlastOutput2"]
    for report in blast:
        here = report['report']['results']['search']
        query = here["query_title"]

        first_hit = here["hits"][0]
        n = first_hit['num']

        base = first_hit['description'][0]
        name = base["title"]
        taxid = str(base["taxid"])
        id = base["accession"]

        base2 = first_hit['hsps'][0]
        eval = str(base2['evalue'])
        score = str(base2['score'])

        print("\t".join((query, name, taxid, id, eval, score)))
        
        #print(report['report'].keys())
