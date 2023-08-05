#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Created Date : Thursday October 7th 2021                                     #
# Author: Jingxin Fu (jingxin@broadinstitute.org)                              #
# ----------                                                                   #
# Last Modified: Thursday October 7th 2021 4:13:04 pm                          #
# Modified By: Jingxin Fu (jingxin@broadinstitute.org)                         #
# ----------                                                                   #
# Copyright (c) Jingxin Fu 2021                                                #
################################################################################


__doc__=""" 
""" 
import textwrap
def EGA(subparsers):
    """
    Update samples from EGA to the sample table model in the Terra workspace
    """
    p = subparsers.add_parser("EGA", help=EGA.__doc__)
    p_input = p.add_argument_group("Input arguments")
    p_input.add_argument("meta_folder", type=str,
                         help="Path to the EGA delimited_maps folder")


    p_input.add_argument("EGAD", type=str,
                         help="Path to the EGA delimited_maps folder")



def CCG(subparsers):
    """
    Update samples from CCG to the sample table model in the Terra workspace
    """
    p = subparsers.add_parser("CCG", help=CCG.__doc__)
    p_input = p.add_argument_group("Input arguments")
    p_input.add_argument("CCG_ID", type=str,
                         help="Path to the EGA delimited_maps folder")

    p_input.add_argument("--meta", type=str, default='nci-breardon-bi-org,SingleCellStorage_VALab,sample',
                         help="Customize sample meta table Or single cell storage workspace")


