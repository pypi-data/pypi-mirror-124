#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 14:43:26 2021

@author: piers
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
#from plotnine import ggplot, geom_line, aes, theme_538
import webbrowser
from plotnine import ggplot, aes, geom_line, theme, theme_538, labs, element_line, element_rect
from random import sample


class Owid:
    def __init__(self, chart_id):
        self.chart_id = chart_id
        self.url = self.get_data_url()
        self.data = self.get_data()
        self.data_info = ""
        
    def get_data(self):
        data_url = self.url
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
        
        
    def get_data_url(self):
        chart_id = self.chart_id
        url = f"https://ourworldindata.org/grapher/{chart_id}"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        preload_link = soup.find_all('link', attrs = {'rel':'preload'})[0].get('href')
    
        full_url = f"https://ourworldindata.org{preload_link}"
    
        return full_url
    
    def view_chart(self):
        webbrowser.open(f'https://ourworldindata.org/grapher/{self.chart_id}')
        
    def plot(self):
        data = self.data 
        title = data.columns.values[3]
        data.columns.values[3] = 'value'
        entities = data.entity.unique()
        n_years = len(data.year.unique())
        if n_years > 1:
            print('Starting Plot')
            (ggplot(data[data.entity.isin(sample(list(entities), 5))],
                    aes(x = 'year', y = 'value', colour = 'entity'))
             + geom_line()
             + theme_538() 
             + labs(title = title, x = '', y = '', colour = '')
             + theme(axis_line_x = (element_line(size = 0.5)), axis_ticks_major_x = (element_line()),
                     legend_position = "bottom", legend_box_background = element_rect(fill = 'black'),
                     aspect_ratio=(0.45))).draw()
    
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
    
    
    
    