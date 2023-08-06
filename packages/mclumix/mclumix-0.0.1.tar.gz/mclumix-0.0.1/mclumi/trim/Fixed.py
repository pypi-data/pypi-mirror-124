__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import argparse
from mclumi.trim.Template import template as umitrim


class fixed():

    def __init__(self, mode='external', params=None):
        if mode == 'internal':
            print('run codes internally.')
            self.trim_params = params
            print('Your params for trimming UMIs are: {}'.format(self.trim_params))
        else:
            self.parser = argparse.ArgumentParser(description='Sequence Identity calculations')
            self.parser.add_argument(
                "--read_structure", "-rs",
                metavar='read_structure',
                dest='rs',
                required=True,
                type=str,
                help='the read structure with elements in conjunction with +',
            )
            self.parser.add_argument(
                "--lens", "-l",
                metavar='lens',
                dest='l',
                required=True,
                type=str,
                help='lengths of all sub-structures separated by +',
            )
            self.parser.add_argument(
                "--input", "-i",
                metavar='input',
                dest='i',
                required=True,
                type=str,
                help='input a fastq file in gz format for trimming UMIs',
            )
            self.parser.add_argument(
                "--output", "-o",
                metavar='output',
                dest='o',
                required=True,
                type=str,
                help='output a UMI-trimmed fastq file in gz format.',
            )
            args = self.parser.parse_args()
            self.read_structure = args.rs
            self.structure_lengths = []
            for i in args.l.split('+'):
                self.structure_lengths.append(int(i))
            print(args.l)
            print(args.i)
            self.fastq_fpn = args.i
            self.fastq_trimmed_fpn = args.o
            self.params = {s: {'len': l} for s, l in zip(self.read_structure.split('+'), self.structure_lengths)}
            self.params['read_struct'] = self.read_structure
            self.params['fastq'] = {
                'fpn': self.fastq_fpn,
                'trimmed_fpn': self.fastq_trimmed_fpn,
            }

    def call(self, ):
        umitrim_parser = umitrim(self.params)
        df = umitrim_parser.todf()
        umitrim_parser.togz(df)


if __name__ == "__main__":
    p = fixed()
    p.call()