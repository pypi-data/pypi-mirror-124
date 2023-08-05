#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Thursday October 7th 2021                                     #
# Author: Jingxin Fu (jingxin@broadinstitute.org)                              #
# ----------                                                                   #
# Last Modified: Thursday October 7th 2021 3:20:46 pm                          #
# Modified By: Jingxin Fu (jingxin@broadinstitute.org)                         #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2021                                                #
################################################################################


__doc__=""" 
Scripts to process EGA data
""" 
import os
import pandas as pd
from .db import TerraTable

class EGA:
    def __init__(self,meta_folder,EGAD):
        """Customize the scripts to preprocess data from EGA
        Parameters
        ----------
        meta_folder : String
            Path to the EGA delimited_maps folder
        EGAD : String
            EGA Dataset ID
        """
        self.meta_folder = meta_folder
        self.formatDt= getattr(EGA,EGAD)(self)
    
    def update(self, billing_project, workspace, no_check):
        """ Update the Sample Table in Terra workspace"""
        tb = TerraTable(billing_project, workspace)
        tb.update(self.formatDt, no_check)

    def EGAD00001005054(self):
        """ Update the Sample Table in Terra workspace
        Parameters
        ----------
        meta_folder : String
            Path to the EGA delimited_maps folder
        """
        df_sample = pd.read_csv(os.path.join(self.meta_folder,'Sample_File.map'), sep='\t',header=None)
        df_sample.columns = 'SAMPLE_ALIAS,SAMPLE_ACCESSION,FILE_NAME,FILE_ACCESSION'.split(
            ',')
        df_meta = pd.read_csv(os.path.join(
            self.meta_folder, 'Study_Experiment_Run_sample.map'), sep='\t',header=None)
        df_meta.columns = """STUDY EGA_ID
    STUDY_TITLE
    STUDY_TYPE
    INSTRUMENT_PLATFORM
    INSTRUMENT_MODEL
    LIBRARY_LAYOUT
    LIBRARY_NAME
    LIBRARY_STRATEGY
    LIBRARY_SOURCE
    LIBRARY_SELECTION
    EXPERIMENT EGA_ID
    RUN EGA_ID
    SUBMISSION CENTER_NAME
    RUN_CENTER_NAME
    EA SAMPLE_ID
    SAMPLE_ALIAS
    BIOSAMPLE_ID
    EGA_SAMPLE_ID""".split('\n    ')[:15]
        df = df_sample.merge(
            df_meta, left_on='SAMPLE_ACCESSION', right_on='EA SAMPLE_ID')
        format_dt = pd.DataFrame(columns=['entity:sample_id','EGAF','Cancer'])
        for sid, dt in df.groupby('SAMPLE_ALIAS'):
            format_dt = format_dt.append({
                'entity:sample_id':sid,
                'EGAF': ','.join(dt['FILE_ACCESSION'].values),
                'Library_Strategy': dt['LIBRARY_STRATEGY'].unique()[0],
                'Library_Source': dt['LIBRARY_SOURCE'].unique()[0],
                'Cancer':'Lung',
                'Sequence_Platform': dt['INSTRUMENT_PLATFORM'].unique()[0]
            },ignore_index=True)

        format_dt['Sample_Source'] = format_dt.Library_Source.map({
            'TRANSCRIPTOMIC SINGLE CELL': 'Fresh Frozen',
            'GENOMIC': 'FFPE'
        })

        format_dt.Library_Source = format_dt.Library_Source.map({
            'TRANSCRIPTOMIC SINGLE CELL': 'single cell',
            'GENOMIC': 'bulk'
        })

        format_dt['Dataset'] = 'EGAD00001005054'
        format_dt['Access'] = 'EGA'
        format_dt['Pubmed'] = '32385277'
        format_dt['Cohort'] = 'Kim, Nayoung, et al. 2020'
        format_dt['Cancer'] = 'Lung'
        format_dt['Patient'] = format_dt['entity:sample_id'].map(lambda x:'_'.join(x.split('_')[:2]))
        format_dt['Cohort_Sample_ID'] = format_dt['entity:sample_id']
        format_dt['entity:sample_id'] = format_dt['Dataset']+'_'+format_dt['entity:sample_id']

        ## Add Reference information
        format_dt['Reference'] = None
        format_dt.loc[format_dt.Library_Source ==
                      'single cell', 'Reference'] = 'GRCh38-2020-A'
        ## Add Chemistry information
        format_dt['Chemistry'] = None
        format_dt.loc[format_dt.Library_Source ==
                      'single cell', 'Chemistry'] = 'SC3Pv2'

        ## Add CellRanger_Version information
        format_dt['CellRanger_Version'] = None
        format_dt.loc[format_dt.Library_Source ==
                      'single cell', 'CellRanger_Version'] = '6.0.1'
        ## Add Parameter for Alignment
        wxs_loc = (format_dt.Library_Strategy == 'WXS')
        pbl_loc = (format_dt.Cohort_Sample_ID.str.contains('PBL'))
        format_dt['Biopsy'] = None
        format_dt.loc[wxs_loc, 'Biopsy'] = 'Tumor'
        format_dt.loc[wxs_loc & pbl_loc , 'Biopsy'] = 'PBL'

        format_dt['Fastq1'] = None
        format_dt.loc[wxs_loc, 'Fastq1'] = 'gs://fc-9c765c88-1fd1-4975-9f71-7525601e6258/WXS_Level1/'+ \
            format_dt.loc[wxs_loc, 'entity:sample_id'] + '/' +\
            format_dt.loc[wxs_loc, 'Patient'] + '_1.fastq.gz'

        format_dt.loc[wxs_loc & pbl_loc, 'Fastq1'] = 'gs://fc-9c765c88-1fd1-4975-9f71-7525601e6258/WXS_Level1/' + \
            format_dt.loc[wxs_loc & pbl_loc, 'entity:sample_id'] + '/' +\
            format_dt.loc[wxs_loc & pbl_loc, 'Patient'] + '_PBL_1.fastq.gz'


        format_dt['Fastq2'] = None
        format_dt.loc[wxs_loc, 'Fastq2'] = 'gs://fc-9c765c88-1fd1-4975-9f71-7525601e6258/WXS_Level1/' + \
            format_dt.loc[wxs_loc, 'entity:sample_id'] + '/' +\
            format_dt.loc[wxs_loc, 'Patient'] + '_2.fastq.gz'

        format_dt.loc[wxs_loc & pbl_loc, 'Fastq2'] = 'gs://fc-9c765c88-1fd1-4975-9f71-7525601e6258/WXS_Level1/' + \
            format_dt.loc[wxs_loc & pbl_loc, 'entity:sample_id'] + '/' +\
            format_dt.loc[wxs_loc & pbl_loc, 'Patient'] + '_PBL_2.fastq.gz'


        if format_dt.shape[0] != format_dt['entity:sample_id'].nunique():
            raise ValueError('Sample ID should be unique!')
        return format_dt
    
    
    
