__version__ = "v1.0"
__copyright__ = "Copyright 2021"
__license__ = "MIT"
__lab__ = "Adam Cribbs lab"

import time
import argparse
import numpy as np
import pandas as pd
from mclumi.align.Read import read as aliread
from mclumi.align.Write import write as aliwrite
from mclumi.fastq.Read import read as rfastq
from mclumi.fastq.Write import write as wfastq
from mclumi.util.Writer import writer as gwriter
from mclumi.util.Hamming import hamming
from mclumi.util.Number import number as rannum
from mclumi.util.Console import console
from mclumi.deduplicate.monomer.Build import build as umibuild
from mclumi.deduplicate.monomer.Cluster import cluster as umimonoclust
from mclumi.deduplicate.monomer.Adjacency import adjacency as umitoolmonoadj
from mclumi.deduplicate.monomer.Directional import directional as umitoolmonodirec
from mclumi.deduplicate.monomer.MarkovClustering import markovClustering as umimonomcl


class dedupPos():

    def __init__(self, bam_fpn, ed_thres, pos, tags=[], mcl_fold_thres=None, inflat_val=2, exp_val=2, iter_num=100, verbose=False):
        """

        Parameters
        ----------
        bam_fpn
        ed_thres

        """
        self.rfastq = rfastq
        self.wfastq = wfastq
        self.pos = pos
        self.tags = tags
        self.rannum = rannum()
        self.umibuild = umibuild
        self.umimonoclust = umimonoclust()
        self.umitoolmonoadj = umitoolmonoadj()
        self.umitoolmonodirec = umitoolmonodirec()
        self.mcl_fold_thres = mcl_fold_thres
        self.umimonomcl = umimonomcl(
            inflat_val=self.inflat_val,
            exp_val=self.exp_val,
            iter_num=self.iter_num,
        )
        self.console = console()
        self.console.verbose = verbose

        self.alireader = aliread(bam_fpn=self.bam_fpn, verbose=self.verbose)
        self.df_bam = self.alireader.todf(tags=['PO'])
        self.df_bam = self.df_bam.loc[self.df_bam['reference_id'] != -1]
        self.console.print('======># of reads with assigned genes in the bam: {}'.format(self.df_bam.shape[0]))

        self.df_bam['umi'] = self.df_bam['query_name'].apply(lambda x: x.split('_')[1])
        self.console.print('======># of redundant umi in the bam: {}'.format(self.df_bam['umi'].shape[0]))
        self.df_bam_gp = self.df_bam.groupby(by=['PO'])
        self.gp_keys = self.df_bam_gp.groups.keys()
        self.console.print('======># of positions in the bam: {}'.format(len(self.gp_keys)))
        self.console.print('======>edit distance thres: {}'.format(ed_thres))

        umi_build_stime = time.time()
        gps = []
        res_sum = []
        for g in self.gp_keys:
            umi_vignette = self.umibuild(
                df=self.df_bam_gp.get_group(g),
                ed_thres=ed_thres,
                verbose=False,
                # verbose=True,
            ).data_summary
            # print(umi_vignette)
            if len(umi_vignette['umi_uniq_mapped_rev']) == 1:
                continue
            else:
                cc = self.umimonoclust.cc(umi_vignette['graph_adj'])
                gps.append(g)
                res_sum.append([
                    umi_vignette,
                    cc,
                    [*umi_vignette['umi_uniq_mapped_rev'].keys()],
                ])
        self.df = pd.DataFrame(
            data=res_sum,
            columns=['vignette', 'cc', 'uniq_repr_nodes'],
            index=gps,
        )
        self.console.print('time for building umi graphs: {:.3f}s'.format(time.time() - umi_build_stime))

        self.df['uniq_mark'] = self.df['uniq_repr_nodes'].apply(lambda x: self.findSingleUMI(x))
        self.df = self.df.loc[self.df['uniq_mark'] == 1]
        self.console.print(self.df.shape[0])

        self.df['cc_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='cc'), axis=1)
        self.df['cc_bam_ids'] = self.df.apply(lambda x: self.bamids(x, method='cc_repr_nodes'), axis=1)

        self.aliwriter = aliwrite(bam_fpn=bam_fpn, df=self.df_bam, tobam_fpn='./s.bam').tobam(
            whitelist=self.decompose(x=self.df['cc_bam_ids'].values)
        )

        self.df['adj'] = self.df.apply(
            lambda x: self.umitoolmonoadj.decompose(
                cc_sub_dict=self.umitoolmonoadj.umi_tools(
                    connected_components=x['cc'],
                    df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                    graph_adj=x['vignette']['graph_adj'],
                )['clusters'],
            ),
            axis=1,
        )
        self.df['adj_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='adj'), axis=1)

        self.df['direc'] = self.df.apply(
            lambda x: self.umitoolmonodirec.decompose(
                cc_sub_dict=self.umitoolmonodirec.umi_tools(
                    connected_components=x['cc'],
                    df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                    graph_adj=x['vignette']['graph_adj'],
                )['clusters'],
            ),
            axis=1,
        )
        self.df['direc_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='direc'), axis=1)

        self.df['mcl'] = self.df.apply(
            lambda x: self.umimonomcl.decompose(
                df=self.umimonomcl.dfclusters(
                    connected_components=x['cc'],
                    graph_adj=x['vignette']['graph_adj'],
                )['clusters'],
            ),
            axis=1,
        )
        self.df['mcl_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='mcl'), axis=1)

        self.df['mcl_val'] = self.df.apply(
            lambda x: self.umimonomcl.decompose(
                df=self.umimonomcl.maxval_val(
                    df_mcl_ccs=self.umimonomcl.dfclusters(
                        connected_components=x['cc'],
                        graph_adj=x['vignette']['graph_adj'],
                    ),
                    df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                    thres_fold=self.mcl_fold_thres,
                )['clusters'],
            ),
            axis=1,
        )
        self.df['mcl_val_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='mcl_val'), axis=1)

        self.df['mcl_ed'] = self.df.apply(
            lambda x: self.umimonomcl.decompose(
                df=self.umimonomcl.maxval_ed(
                    df_mcl_ccs=self.umimonomcl.dfclusters(
                        connected_components=x['cc'],
                        graph_adj=x['vignette']['graph_adj'],
                    ),
                    df_umi_uniq_val_cnt=x['vignette']['df_umi_uniq_val_cnt'],
                    umi_uniq_mapped_rev=x['vignette']['umi_uniq_mapped_rev'],
                    thres_fold=self.mcl_fold_thres,
                )['clusters'],
            ),
            axis=1,
        )
        self.df['mcl_ed_repr_nodes'] = self.df.apply(lambda x: self.umimax(x, method='mcl_ed'), axis=1)

        self.df['uniq_eds'] = self.df.apply(lambda x: self.edave(x, method='uniq_repr_nodes'), axis=1)
        self.df['cc_eds'] = self.df.apply(lambda x: self.edave(x, method='cc_repr_nodes'), axis=1)
        self.df['adj_eds'] = self.df.apply(lambda x: self.edave(x, method='adj_repr_nodes'), axis=1)
        self.df['direc_eds'] = self.df.apply(lambda x: self.edave(x, method='direc_repr_nodes'), axis=1)
        self.df['mcl_eds'] = self.df.apply(lambda x: self.edave(x, method='mcl_repr_nodes'), axis=1)
        self.df['mcl_val_eds'] = self.df.apply(lambda x: self.edave(x, method='mcl_val_repr_nodes'), axis=1)
        self.df['mcl_ed_eds'] = self.df.apply(lambda x: self.edave(x, method='mcl_ed_repr_nodes'), axis=1)

        self.console.print(self.df['uniq_eds'].value_counts())
        self.console.print(self.df['cc_eds'].value_counts())
        self.console.print(self.df['adj_eds'].value_counts())
        self.console.print(self.df['direc_eds'].value_counts())
        self.console.print(self.df['mcl_eds'].value_counts())
        self.console.print(self.df['mcl_val_eds'].value_counts())
        self.console.print(self.df['mcl_ed_eds'].value_counts())

    def findSingleUMI(self, x):
        if len(x) != 1:
            return 1
        else:
            return 0

    def decompose(self, x):
        t = []
        for i in x:
            t = t + i
        print(len(t))
        return t

    def bamids(self, x, method):
        bam_id_maps = x['vignette']['umi_bam_ids']
        return [bam_id_maps[node] for node in x[method]]

    def umimax(self, x, method):
        umi_val_cnts = x['vignette']['df_umi_uniq_val_cnt']
        umi_cc = []
        for k_c, nodes in x[method].items():
            # self.console.print('cc: ', x['cc'])
            # self.console.print('vc: ', umi_val_cnts)
            # self.console.print('nodes: ',nodes)
            # self.console.print('val_cnts: ', umi_val_cnts.loc[umi_val_cnts.index.isin(nodes)].max())
            umi_max = umi_val_cnts.loc[umi_val_cnts.index.isin(nodes)].idxmax()
            umi_cc.append(umi_max)
            # self.console.print('val_cnts1: ',)
        return umi_cc

    def edave(self, x, method):
        repr_nodes = x[method]
        umi_maps = x['vignette']['umi_uniq_mapped_rev']
        node_len = len(repr_nodes)
        if node_len != 1:
            ed_list = []
            for i in range(node_len):
                for j in range(i + 1, node_len):
                    ed_list.append(hamming().general(
                        s1=umi_maps[repr_nodes[i]],
                        s2=umi_maps[repr_nodes[j]],
                    ))
            return np.ceil(sum(ed_list) / (len(ed_list)))
        else:
            return -1

    def eds_(self, x, method):
        """

        Parameters
        ----------
        x
        method

        Returns
        -------

        """
        print(x.index)
        repr_nodes = x[method]
        umi_maps = x['vignette']['umi_uniq_mapped_rev']
        umi_val_cnts = x['vignette']['df_umi_uniq_val_cnt']
        # print(repr_nodes)
        # if len(repr_nodes) == len(np.unique(repr_nodes)):
        #     print(True)
        # else:
        #     print(False)
        node_len = len(repr_nodes)
        if node_len != 1:
            ed_list = []
            for i in range(node_len):
                for j in range(i + 1, node_len):
                    if repr_nodes[i] != repr_nodes[j]:
                        ed_list = ed_list + [hamming().general(
                            umi_maps[repr_nodes[i]],
                            umi_maps[repr_nodes[j]])
                        ] * (umi_val_cnts.loc[repr_nodes[i]] * umi_val_cnts.loc[repr_nodes[j]])
            return round(sum(ed_list) / len(ed_list))
        else:
            return -1

    def evaluate(self, ):
        return


if __name__ == "__main__":
    from mclumi.Path import to

    umikit = dedupPos(
        # bam_fpn=to('example/data/example.bam'),
        bam_fpn=to('example/data/example_buddle.bam'),
        # bam_fpn=to('example/data/RM82CLK1_S3_featurecounts_gene_sorted.bam'),
        mcl_fold_thres=1.5,
        inflat_val=2,
        exp_val=2,
        iter_num=100,
        verbose=True,
        pos='pos',
        ed_thres=1,
    )