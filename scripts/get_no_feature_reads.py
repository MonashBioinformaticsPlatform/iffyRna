#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import sys
import os
import pysam

# featurecounts files produces with -R CORE flag
f = sys.argv[1]

h = {}

keep = "Unassigned_NoFeatures"

with open(f) as handler:
    for i in handler:
        line = i.strip()

        # Each generated file contains four columns:
        # - read name
        # - status (assigned or the reason if not assigned)
        # - number of targets
        # - target list

        id, t, n, name = line.split("\t")

        if t == keep:
            if id in h:
                #sys.exit("ERROR: can't happend %s" % id)
                print("WARNING: Shouldn't happen for single-end data %s" % id, file=sys.stderr)
            h[id] = n

print("MSG: Created big hash")

# second arg is you original bam file 
b = sys.argv[2]
samfile = pysam.AlignmentFile(b, 'rb')

out_prefix = sys.argv[3]
#tmp = os.path.basename(b)
#tmp2 = tmp.split(".bam")[0]
#tmp2 = b.split(".bam")[0]
outfile = out_prefix + "_NoFeatures.bam"
outfile = pysam.AlignmentFile(outfile, "wb", template=samfile)

cnt1 = 0
cnt2 = 0
threshold = 100000

for i in samfile:
    if i.query_name in h:
        outfile.write(i)
        cnt2 += 1

    cnt1 += 1

    if cnt2 > threshold:
        print("MSG: Processed %s reads" % cnt1)
        print("MSG: NoFeature reads so far %s " % cnt1)
        threshold += cnt2
