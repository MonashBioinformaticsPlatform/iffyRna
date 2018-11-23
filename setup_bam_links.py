#!/usr/bin/env python3

import os
import sys

f = sys.argv[1]
prefix = "data"

with open(f) as handler:
    for i in handler:
        item = i.strip()

        if item.startswith("#"):
            continue

        line = item.split("/")

        bam_files = os.listdir(item)
        fqc = os.path.dirname(item) + "/fastqcReport"

        fqc_files = os.listdir(fqc)

        lib_type = "single"

        for fq in fqc_files:
            if "_R2" in fq:
                lib_type = "paired"
                break

        tmp = line[4:6]
        tmp.insert(0, prefix)
        tmp.insert(1, lib_type)
        fn = '/'.join(tmp)

        os.makedirs(fn, exist_ok=True)

        #print(item, lib_type, fn)

        for bam in bam_files:
            if bam.endswith("dups.bam"):
                src = '/'.join((item, bam))
                dest = '/'.join((fn, bam))
                os.symlink(src, dest)
               #print(src, dest)
        #os.removedirs(fn)
