#!/usr/bin/env python3

# Scan along bam (coordinate sorted) if found a read start 1Mb window
# capture all reads in that window.
# Calculate per base coverage and report
# mean and std, min and max coverage location at base level, which genomic locatio has 
# the highest base coverage.
# 
# From that I should be able to understand whether there is an even coverage or not
# and perhaps multiple putative features are in that region

# NOTE Mitochondria is a special case, I'm seeing a lot of reads mapped at the junction
# but they are regarded as unmapped casue circular genome represented as linear
# Will need to think about that, skip for now

import sys
#from Bio import SeqIO
import pysam
import numpy as np

def log_feat(chrom, name, start, end, n_reads):

    feat_len = end-start

    if name in feats[chrom]:
        sys.exit("ERROR: can't happen")

    feats[chrom][name] = [start, end, n_reads, feat_len]

f = sys.argv[1]

samfile = pysam.AlignmentFile(f, 'rb')

k = 2000
threshold = 50

first = None
# this is per feature
n_reads = 0
tot_reads = 0
prev_pos = 0
prev_chrom = None
last_l = None
cnt = 1

# Need to keep track of all reads per chromosome
# Want to rank newly called features
# e.g if a particular feature aggregates most of the reads at the chromsome
# this needs rather high ranking. 
# Penalties for feature length. since longer feature will aggregate more reads
# just due to size

feats = {}
totals = {}

## NOTE WARNING!
#     This code assumes coordinate sorted bam
#     It will run on reads sorted bam
#     but this isn't right !
##
## TODO check that bam is sorted, error out if not

for line in samfile:

    # skip unmapped reads
    if line.is_unmapped:
        continue

    cigar = line.cigartuples
    chrom = line.reference_name

    if chrom not in feats:
        feats[chrom] = {}

    # TODO
    # for now lets grab reads that are not split
    # just cause I don't want to mark about with cigar at this stage
    # will need to handle this later
    if len(cigar) == 1:
        # this is with respect to the read
        # will need this later, once start handling cigar
        align_start = line.query_alignment_start

        pos = line.reference_start
        read_id = line.query_name
        l = line.query_length
        last_l = l

        # init variables
        if first is None:
            first = pos
        if prev_chrom is None:
            prev_chrom = chrom

        diff = pos - prev_pos

        if diff > l+k:
            # this is confusing stop
            # but I'm pretty sure I don't want read in the last section
            # of the chromosome if then don't pass the threshold
            if n_reads > threshold:

                name = "feature_%s" % cnt
                log_feat(chrom, name, first, pos+l, n_reads)            
                cnt += 1

            first = pos
            n_reads = 0
        elif chrom != prev_chrom:
            totals[prev_chrom] = tot_reads
            tot_reads = 0

            if n_reads > threshold:

                name = "feature_%s" % cnt
                log_feat(prev_chrom, name, first, prev_pos+l, n_reads)            
                cnt += 1

            first = pos
            n_reads = 0

        tot_reads += 1

        prev_pos = pos
        n_reads += 1

        prev_chrom = chrom

totals[prev_chrom] = tot_reads
log_feat(prev_chrom, "last_guys", first, prev_pos+last_l, n_reads)

empty_keys = []

for chr in feats:
    if feats[chr]:
        for k,v in feats[chr].items():
            feats[chr][k].append(round(v[2]/totals[chr], 2))
    else:
        empty_keys.append(chr)

print("\t".join(("GeneId", "Chrom", "Start", "End", "Strand", "Nreads", "FeatSize", "Frac", "Mean", "Std")))

for chr in feats:
    if chr in empty_keys:
        continue

    #fracs = [v[4] for v in feats[chr].values()]
    try:
        #print("Trying: %s" % chr)
        fracs = [v[4] for v in feats[chr].values()]
    except IndexError:
        #print(feats[chr].values())
        sys.exit("Huh? %s" % chr)

    if len(fracs) == 1:
        #print(">%s\t-1\t-1" % chr)

        key = list(feats[chr].keys())[0]
        v = feats[chr][key]
        v.insert(0, key)
        v.insert(1, chr)
        v.insert(4, '.')
        v += [-1, -1]
        vals = '\t'.join(map(str, v))
        print(vals)
        continue

    m = round(np.mean(fracs), 2)
    s = round(np.std(fracs), 2)
    #print(">%s\t%s\t%s" % (chr, m, s))

    for feat, v in sorted(feats[chr].items(), key=lambda x: x[1][2], reverse=True):
        if v[4] > s*2:
            v.insert(0, feat)
            v.insert(1, chr)
            v.insert(4, '.')
            v += [m, s]
            vals = '\t'.join(map(str, v))
            print(vals)
