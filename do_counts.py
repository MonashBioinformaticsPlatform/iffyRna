#!/usr/bin/env python3.5

import sys
import os
import subprocess

f = sys.argv[1]
ref = sys.argv[2]
extn = "NoFeatures.bam"
counts_exe = "/home/kirill/downloads/subread-1.6.3-source/bin/featureCounts"

for root, dirs, files in os.walk(f):
    #print(root, dirs, files)
    if files:
        lib_type = root.split("/")[1]

        extr = ""
        if lib_type == "paired":
            extr = "-p"
            
        #output = os.path.join(root, "NonStrandedCounts.txt")
        output = os.path.join(root, "NonStrandedCountsNoFeatures.txt")

        #stdout = os.path.join(root, "log.stdout")
        #stderr = os.path.join(root, "log.stderr")
        #handler_out = open(stdout, "w")
        #handler_err = open(stderr, "w")

        bams = ' '.join([os.path.join(root, f) for f in files if f.endswith(extn)])

        #cmd = [root, "=", counts_exe, "-T", "13", "-a", ref, "-s", "0", "-R", "CORE", "-o", output, extr, bams]
        cmd = [root, "=", counts_exe, "-T", "13", "-t", "gene", "-a", ref, "-s", "0", "-R", "CORE", "-o", output, extr, bams]
        #print("MSG: Started %s .." % root)
        #print("MSG: Runnin %s .." % ' '.join([str(c) for c in cmd]))
        print(' '.join([str(c) for c in cmd]))

        #subprocess.run(cmd, stdout=handler_out, stderr=handler_err)
        #subprocess.call(cmd, stdout=handler_out, stderr=handler_err)

        #with open(log, "w") as handler:
        #    handler.write(res.stderr)
