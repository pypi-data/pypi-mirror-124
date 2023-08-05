#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Friday October 8th 2021                                       #
# Author: Jingxin Fu (jingxin@broadinstitute.org)                              #
# ----------                                                                   #
# Last Modified: Friday October 8th 2021 4:47:07 pm                            #
# Modified By: Jingxin Fu (jingxin@broadinstitute.org)                         #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2021                                                #
################################################################################


__doc__ = """
Scripts to process CCG data
"""
from .db import TerraTable, get_terra_table_to_df
import pandas as pd
import os


class CCG:
    def __init__(self, meta, CCG_ID,BCL=None):
        """Customize the scripts to preprocess data from EGA
        Parameters
        ----------
        meta : String
            Path to the meta file, delimeter: '\t'
        CCG_ID : String
            CCG Project ID
        """
        self.meta = meta
        self.BCL = BCL
        self.formatDt = getattr(CCG, CCG_ID)(self)

    def update(self, billing_project, workspace,no_check):
        """ Update the Sample Table in Terra workspace"""
        tb = TerraTable(billing_project, workspace)
        tb.update(self.formatDt, no_check)
    
    def bclStorage(self):
        df = pd.read_csv(self.meta,sep='\t')
        return df
        
    def makefastqUpdate(self):
        df = pd.read_csv(self.meta, sep='\t')
        df.rename(columns={
            'Sample': 'entity:sample_id'
        },inplace=True)
        return df

    def bclUpdate(self):
        project,workspace,table_name = self.meta.split(',')
        tb_from = get_terra_table_to_df(project, workspace, table_name)
        tb_from.rename(columns={
            'entity:sample_id': 'entity:bcl_id'
        },inplace=True)
        return tb_from

    def KevinBi2020CancerCell(self):
        df = pd.read_csv(self.meta)
        df['Cohort_Sample_ID'] = df['Sample']
        df['Dataset'] = 'phs002065'
        df['Sample'] = df['Dataset']+'_'+df['Sample']
        df['Access'] = 'dbGaP'
        df['Pubmed'] = '33711272'
        df['Cohort'] = 'Kevin, Bi, et al. 2021'
        df['Cancer'] = 'RCC'
        df['Library_Strategy'] = 'RNA-Seq'
        df['Library_Source'] = 'single cell'
        df['Chemistry'] = 'SC3Pv2'
        df['CellRanger_Version'] = '6.0.1'

        df.rename(columns={
            'Sample':'entity:sample_id',
            'Flowcell': 'Fastq_Folder'
        },inplace=True)
        return df
