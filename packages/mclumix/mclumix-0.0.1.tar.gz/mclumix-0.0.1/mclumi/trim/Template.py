__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import pandas as pd
from mclumi.fastq.Read import read as rfastq
from mclumi.fastq.Write import write as wfastq
from mclumi.trim.Filter import filter
from mclumi.trim.UMIRuleOut import umiRuleOut as umiro
from mclumi.trim.SeqRuleOut import seqRuleOut as seqro
from mclumi.Path import to


class template(object):

    def __init__(self, params):
        self.params = params
        self.filter = filter()
        self.umiro = umiro(read_summary=self.params)
        self.seqro = seqro(read_summary=self.params)
        self.rfastq = rfastq
        self.wfastq = wfastq

    def todf(self, ):
        """
        Notes
        -----
        Trimmed UMIs and genomic sequences.

        Examples
        --------
        >>> params = {
        ...  'read_struct': 'primer_1+umi_1+seq_1+seq_2+umi_2+primer_2',
        ...  'umi_1': {'len': 12},
        ...  'umi_2': {'len': 10},
        ...  'primer_1': {'len': 20},
        ...  'primer_2': {'len': 20},
        ...  'seq_1': {'len': 6},
        ...  'seq_2': {'len': 8},
        ...  'fastq': {
        ...      'path': to('example/data/'),
        ...      'name': 'pcr_1',
        ...      'trimmed_path': to('example/data/'),
        ...      'trimmed_name': 'pcr_1_trim',
        ...   },
        ... }
        >>> p = template(params)
        >>> p.todf()

        Returns
        -------
            pandas dataframe with column names: seq_raw, name, umi_1, umi_2, ..., umi_n, seq_2, seq_3, ..., seq_n

        """
        print('===>reading from fastq...')
        names, seqs, _, _ = self.rfastq().fromgz(
            fastq_fpn=self.params['fastq']['fpn'],
        )
        df = pd.DataFrame(seqs, columns=['seq_raw'])
        df['name'] = names
        print('===>umi structure: {}'.format(self.params['read_struct']))
        compo_struct = self.params['read_struct'].split('+')
        umi_pos_in_struct = [i for i, cstruct in enumerate(compo_struct) if 'umi' in cstruct.split('_')]
        seq_pos_in_struct = [i for i, cstruct in enumerate(compo_struct) if 'seq' in cstruct.split('_')]
        print('===>umi positions in the read structure: {}'.format(', '.join(map(str, umi_pos_in_struct))))
        print('===>seq positions in the read structure: {}'.format(', '.join(map(str, seq_pos_in_struct))))
        umi_rule_out_len_dict = self.umiro.sequential(
            compo_struct=compo_struct,
            umi_pos_in_struct=umi_pos_in_struct,
        )
        seq_rule_out_len_dict = self.seqro.sequential(
            compo_struct=compo_struct,
            seq_pos_in_struct=seq_pos_in_struct,
        )
        for key, val in umi_rule_out_len_dict.items():
            start = val
            end = val + self.params[key]['len']
            df[key] = df.apply(lambda x: self.filter.singleStart(x['seq_raw'], start, end), axis=1)
            print('===>{} has been taken out'.format(key))
        for key, val in seq_rule_out_len_dict.items():
            start = val
            end = val + self.params[key]['len']
            df[key] = df.apply(lambda x: self.filter.singleStart(x['seq_raw'], start, end), axis=1)
            print('===>{} has been taken out'.format(key))
        return df

    def togz(self, df):
        """

        Note
        ----
            write to a Fastq file in gz format.

        Example
        -------
        >>>params = {
        ... 'read_struct': 'primer_1+umi_1+seq_1+seq_2+umi_2+primer_2',
        ... 'umi_1': {'len': 12},
        ... 'umi_2': {'len': 10},
        ... 'primer_1': {'len': 20},
        ... 'primer_2': {'len': 20},
        ... 'seq_1': {'len': 6},
        ... 'seq_2': {'len': 8},
        ... 'fastq': {
        ...     'path': to('example/data/'),
        ...     'name': 'pcr_1',
        ...     'trimmed_path': to('example/data/'),
        ...     'trimmed_name': 'pcr_1_trim',
        ... },
        ...}
        >>>p = template(params)
        >>>df = p.todf()
        >>>p.togz(df)

        Parameters
        ----------
        df
            pandas Dataframe returned from todf().

        Returns
        -------
            pandas dataframe in the column orders: seq_1, name, umi_1, umi_2, ..., umi_n, seq_2, seq_3, ..., seq_n

        """
        print('===>start saving in gz format...')
        # # /* block. in case of only UMIs present in the reads. */
        if 'seq_1' not in df.columns.tolist():
            df['seq_1'] = 'B'
        df_col_names = df.columns.tolist()
        df_col_names.remove('seq_raw')
        df_col_names.remove('seq_1')
        df_trimmed = df[['seq_1'] + df_col_names]
        self.wfastq().togz(
            list_2d=df_trimmed.values.tolist(),
            sv_fpn=self.params['fastq']['trimmed_fpn'],
        )
        print('===>trimmed UMIs have been saved in gz format.')
        return df_trimmed


if __name__ == "__main__":
    import importlib

    f31 = importlib.import_module('mclumi.trim.Fixed')  # 绝对导入
    # params_ = importlib.import_module('.c.c', package='b')  # 相对导入
     # 取出变量
     # 取出class C
    import os
    print(__file__)
    print(os.path.dirname(__file__))
    params = {
        'umi_1': {
            'len': 12,
        },
        'umi_2': {
            'len': 10,
        },
        'umi_3': {
            'len': 12,
        },
        # 'read_struct': 'umi_1+seq_1',
        'read_struct': 'primer_1+umi_1+seq_1+seq_2+umi_2+primer_2',
        # 'read_struct': 'primer+umi_start+seq+umi_1+primer',
        # 'read_struct': 'primer+umi_1+seq_1+primer+umi_2+seq_2+umi_3+primer',
        'primer_1': {
            'len': 20,
        },
        'primer_2': {
            'len': 20,
        },
        'seq_1': {
            'len': 6,
        },
        'seq_2': {
            'len': 8,
        },
        'fastq': {
            'path': to('example/data/'),
            'name': 'pcr_1',
            'trimmed_path': to('example/data/'),
            'trimmed_name': 'pcr_1_trim',
        },
    }
    p = template(params)

    df = p.todf()

    print(df)
    print(p.togz(df))