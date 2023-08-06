# mcl-umi

pip installed test version for mclumi

https://test.pypi.org/project/tfg666/0.0.0.0.17/

the package readthedocs manual 
https://tfg666.readthedocs.io/en/latest/index.html

##installation

```shell
pip install -i https://test.pypi.org/simple/ tfg666==0.0.0.0.24
```

##Usage
overall
```shell
mclumi -h
```

get the data files in `mclumi/example/data/`


two tools: 1. trim 2. dedup_basic

trim (extracting and attaching umis to names of reads in fastq format)
```angular2html
mclumi trim -i ./pcr_1.fastq.gz -o ./pcr_1222.fastq.gz -rs primer_1+umi_1+seq_1+seq_2+umi_2+primer_2 -l 20+12+6+8+10+20
```

dedup_basic
```angular2html
mclumi dedup_basic -m mcl -ed 1 -ibam ./example.bam -otsv ./dedup_stat.tsv
```