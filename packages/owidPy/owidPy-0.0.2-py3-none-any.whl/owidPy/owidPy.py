#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 16:59:37 2021

@author: piers
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
from plotnine import ggplot, geom_line, aes, theme_538


pd.set_option('display.max_rows', 100)

def get_datasets():
    response = requests.get('https://ourworldindata.org/charts')
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all(['section', 'a'])
    
    titles = []
    urls = []
    for link in links:
        titles.append(link.text)
        urls.append(link.get('href'))
        
    dic = {'title': titles,
           'chart_id': urls}
    
    datasets = pd.DataFrame(dic)
    datasets = datasets[datasets.chart_id.str.contains('grapher') > 0].drop_duplicates()
    datasets.chart_id = datasets.chart_id.str.split(pat = '/').str[2]
    return datasets
    
def owid_search(term):
    datasets = get_datasets()
    
    return datasets[datasets.title.str.contains(term, case = False, regex = False) > 0]
    
    
    
    
def get_data_url(chart_id):
    url = f"https://ourworldindata.org/grapher/{chart_id}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    preload_link = soup.find_all('link', attrs = {'rel':'preload'})[0].get('href')

    full_url = f"https://ourworldindata.org{preload_link}"
    
    return full_url
    
def owid(chart_id):
    data_url = get_data_url(chart_id)

    json_raw = requests.get(data_url).json()

    vars = json_raw['variables']

    datasets = []
    for i in vars:
        val_name = vars[i]['name']
        data_dict = {'entity_id': vars[i]['entities'],
                     'year': vars[i]['years'],
                     val_name: vars[i]['values']}
        #data = pd.DataFrame(data_dict).rename('')
        datasets.append(pd.DataFrame(data_dict))
    
    all_data = reduce(lambda x, y: pd.merge(x, y, on = ['entity_id', 'year']), datasets)

    entity_ids = list(json_raw['entityKey'].keys())
    codes = []
    entities = []
    
    for id in entity_ids:
        codes.append(json_raw['entityKey'][id]['code'])
        entities.append(json_raw['entityKey'][id]['name'])
    
    entity_key_dict = {'entity_id': entity_ids,
                       'entity': entities,
                       'code': codes}
    
    entity_key = pd.DataFrame(entity_key_dict)

    all_data['entity_id'] = all_data['entity_id'].astype(str)
    
    data = all_data.merge(right = entity_key, how = 'left', on = 'entity_id')
    
    data = data[['entity', 'code'] + [c for c in data if c not in ['entity', 'code']]]
    
    data.pop('entity_id')
    
    return data

owid_search('beef')
    
df = owid("beef-and-buffalo-meat-consumption-per-person")
df
df.columns.values[3] = 'value'

df
(ggplot(df[df.entity == 'United Kingdom'], aes('year', 'value'))
 + geom_line()
 + theme_538())



chart_id = "gross-vs-net-enrollment-rate-in-primary-education"







    
    
    
    
    
    
    
    