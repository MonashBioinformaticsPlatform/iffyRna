#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import sys
import gzip
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

feats = sys.argv[1]
ref_genome = sys.argv[2]

feats_dict = {}

with open(feats) as feats_handl:
    for i in feats_handl:
        line = i.strip()

        gene_id,chrom,start,end,strand,n_reads,feat_size,frac,mean,std = line.split('\t')

        # header line
        if gene_id.startswith("GeneId"):
            continue

        if chrom not in feats_dict:
            feats_dict[chrom] = {}

        if gene_id in feats_dict[chrom]:
            sys.exit("ERROR: can't happen")
        
        feats_dict[chrom][gene_id] = [start, end, n_reads, feat_size, frac]


for seq in SeqIO.parse(gzip.open(ref_genome, 'rt'), 'fasta'):
    # assuming chrom name is the same
    # which it should be
    feats = feats_dict.get(seq.id)

    if feats is None:
        continue

    for feat, v in feats.items():
        start, end, n_reads, feat_size, frac = v
        frag = seq.seq[int(start):int(end)+1]
        info = "%s|%s|%s|%s|%s" % (start, end, feat_size, n_reads, frac)
        id = "%s_%s" % (seq.id, feat)
        #record = SeqRecord(frag,
        record = SeqRecord(frag.upper(),
                           id=id,
                           name=feat,
                           description=info)
        SeqIO.write(record, sys.stdout, 'fasta')
