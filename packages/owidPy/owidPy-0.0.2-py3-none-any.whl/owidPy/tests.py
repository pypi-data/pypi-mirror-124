#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 12:48:17 2021

@author: piers
"""
import os
os.chdir('/Users/piers/Documents/OWID/owidPy')

from owidPy import owid, owid_search
import seaborn as sns


import owidPy

owidPy.owid_search('rights')

owid_search("rights")

df = owid("legally-recognized-rights-to-land")

df

sns.lineplot(x = 'year', y = 'Fund for Peace (Fragile States Index (Human Rights Dimension))',
             hue = 'entity',
             data = df[df.entity.isin(['United Kingdom', 'United States'])])


