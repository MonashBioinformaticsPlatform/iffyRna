## iffyRna

> if ya wanna suss out the transcriptome

## Quick start

```
iffyRna -bamFiles bamFiles \
        -gtfFile Mus_musculus.GRCm38.90.genes_only.gtf \
        -fastaRef Mus_musculus.GRCm38.dna_sm.primary_assembly.fa.gz  \
        -paired
```

## Docs

- `-bamFiles` directory that holds bam files, assumes `.bam` file extention. These don't need to be sorted in any particular way
- `-gtfFile` is your normal gtf files (tested with Ensembl), be aware that `iffyRna` needs "gene" feature to be present in the files
the counting will be run with `featureCounts -t gene` options. Check that 3rd column in your gtf contains "gene" field" 
- `-fastaRef` this is normal fasta file, which needs to match gtf files
- `-paired` flag to indicate that your data is paried-end
- `-threads` maximum number of threads to use, note that not all task can be multi-threaded, default value set to [8]

## Instalation

#### Python dependencies

- `numpy`
- `pysam`
- `biopython`

#### iffyRna

It's written in [BigDataScript (bds) language](http://pcingola.github.io/BigDataScript/bigDataScript_manual.html), please intalls as per bds docs, before running `iffyRna`

## Future

- package with conda

