import time
import random
from typing import Union, Tuple, List, Literal
from pathlib import Path
import re

from tqdm.auto import tqdm
import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

def wait_random_time(mean: float=2, std: float=1, min: float=1.5, max: float=3) -> None:
    time.sleep(np.clip(np.random.normal(mean, std), min, max))

class PlayerCrawler:
    return_cols = [
        'season', 
                
        'event-title', 
        'event-url', 

        'location', 
        'date', 
                
        'short-program-link', 
        'short-program-score', 
        'short-program-ranking',
                
        'freeskating-link', 
        'freeskating-score', 
        'freeskating-ranking',

        'final-link', 
        'final-score',
        'final-ranking',
    ]

    config = {
        'RAISE_ERROR_NOT_200': True,
    }

    def __init__(
            self, 
            root_url: Union[str, None]=None, 
            header=None, 
            reutrn_cols: Union[List[str], None]=None, 
            config: Union[dict, None]=None
        ):
        if root_url is not None:
            self.root_url = root_url
        else:
            self.root_url = 'https://skatingscores.com'
        
        if header is not None:
            self.header = header
        else:
            self.header = { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98Safari/537.36', 
                'Accept-Language': 'en-US'
            }
        
        if config is not None:
            self.config = config
        
        if reutrn_cols is not None:
            self.return_cols = reutrn_cols
    
    def get_player_url(self, name: str, noc: str, gender: Union[Literal['women', 'men'], str]) -> str:
        return f'{self.root_url}/{noc}/{gender}/{name}'
    
    def get_page(self, url: str) -> Tuple[BeautifulSoup, bool]:
        get = requests.get(url, headers=self.header)
        if get.status_code == 200:
            is_200 = True
        else:
            is_200 = False
        
        if self.config['RAISE_ERROR_NOT_200']:
            get.raise_for_status()
        
        if get.text is not None:
            soup = BeautifulSoup(get.text, 'html.parser')
        else:
            soup = BeautifulSoup('', 'html.parser')
        
        return (soup, is_200)
    
    def __get_sub_result(self, sub_result: BeautifulSoup) -> Tuple[str, float, str]:
        if sub_result.text.strip() == '':
            return '', 0., ''
    
        br_tag = sub_result.find('br')
        if br_tag is not None:
            sub_result_ranking = list(br_tag.previous_siblings)[0].strip()
        else:
            sub_result_ranking = sub_result.text.strip()
    
        sub_result_score_link_tag = sub_result.find('a')
        if sub_result_score_link_tag is None:
            sub_result_link = ''
            sub_result_score = 0.
        elif sub_result_score_link_tag.text == 'WD':
            sub_result_link = sub_result_score_link_tag['href']
            sub_result_score = 0.
            sub_result_ranking = 'WD'
        else:
            sub_result_link = sub_result_score_link_tag['href']
            if ('FNR' in sub_result_score_link_tag.text
                or 'DNQ' in sub_result_score_link_tag.text
                or br_tag is None
                ):
                sub_result_score = 0.
            else:
                sub_result_score = float(sub_result_score_link_tag.text.strip())
        return self.root_url + sub_result_link, sub_result_score, sub_result_ranking
    
    def parse_page(self, soup: BeautifulSoup) -> pd.DataFrame:
        result_data = []
        seasonal_results = soup.find_all('div', attrs='event-grid-wrap')[-1].find_all('table', attrs='event-grid stab')
        for seasonal_result in seasonal_results:
            season = seasonal_result.find('tr', attrs='group-row').text
            events = seasonal_result.find_all('tr')[2:]
            for event in events:
                # Title Name and URL
                title = event.find('td', attrs='event-title').find('a')
                title_name = title.text
                event_url = self.root_url + title['href']

                # Location and Date
                l_tag = event.find('td', attrs='l').find('br')
                location = list(l_tag.previous_siblings)[0].strip()
                date = list(l_tag.next_siblings)[-1].text.strip()
                
                sub_results = event.find_all('td')[-3:]
                # Short Program
                short_program_link, short_program_score, short_program_ranking = self.__get_sub_result(sub_results[0])

                # Freeskating
                freeskating_link, freeskating_score, freeskating_ranking = self.__get_sub_result(sub_results[1])

                # Final Result
                final_result_link, final_result_score, final_result_ranking = self.__get_sub_result(sub_results[2])

                result_data.append({
                    'season': season,

                    'event-title': title_name,
                    'event-url': event_url,

                    'location': location,
                    'date': date,

                    'short-program-link': short_program_link, 
                    'short-program-score': short_program_score, 
                    'short-program-ranking': short_program_ranking,
                
                    'freeskating-link': freeskating_link, 
                    'freeskating-score': freeskating_score, 
                    'freeskating-ranking': freeskating_ranking,

                    'final-link': final_result_link, 
                    'final-score': final_result_score,
                    'final-ranking': final_result_ranking,
                })
        
        result_df = pd.DataFrame(result_data)
        result_df['date'] = result_df['date'].str.replace('Sept', 'Sep')
        result_df['date'] = result_df['date'].str.replace('sept', 'Sep')
        datetime1 = pd.to_datetime(result_df['date'], format='%b %d, %Y', errors='coerce') # February 11, 2014
        datetime2 = pd.to_datetime(result_df['date'], format='%b. %d, %Y', errors='coerce') # February. 11, 2014
        datetime3 = pd.to_datetime(result_df['date'], format='%B %d, %Y', errors='coerce') # Feb 11, 2014
        datetime4 = pd.to_datetime(result_df['date'], format='%B. %d, %Y', errors='coerce') # Feb. 11, 2014
        new_datetime = datetime1.fillna(datetime2).fillna(datetime3).fillna(datetime4)
        if new_datetime.isna().sum() != 0:
            print(result_df[new_datetime.isna()]['date'])
            raise ValueError
        result_df['date'] = new_datetime
        
        result_df.loc[result_df['short-program-link'].str.fullmatch(self.root_url), 'short-program-link'] = ''
        result_df.loc[result_df['freeskating-link'].str.fullmatch(self.root_url, ), 'freeskating-link'] = ''
        result_df.loc[result_df['final-link'].str.fullmatch(self.root_url), 'final-link'] = ''
        result_df.loc[result_df['final-score'] == 0., 'final-score'] = result_df[result_df['final-score'] == 0.]['short-program-score']

        result_df = result_df.loc[::-1, :].reset_index(drop=True)
        result_df = result_df[self.return_cols]
        return result_df

    def get_player_page(self, name: str, noc: str, gender: str) -> pd.DataFrame:
        url = self.get_player_url(name, noc, gender)
        soup, is_200 = self.get_page(url)
        if not is_200:
            return pd.DataFrame({col: [] for col in self.return_cols})
        else:
            return self.parse_page(soup)

def parse_detailed_result(soup: BeautifulSoup) -> Tuple[pd.DataFrame, dict, None]:
    top_tag = soup.find('div', attrs='perf-wrap')
    if top_tag is None:
        return (
            None, 
            None, 
            None, 
            None, 
            None, 
            None, 
            {
                'PCS_grade': None, 
                'PCS_score': None, 
            }
        )
    
    # `total_df`
    if (top_tag.find('div', attrs='ptab1-wrap') is not None 
        and top_tag.find('div', attrs='ptab1-wrap').find('table', attrs='ptab ptab2 paneltab hov-tab') is not None
        and top_tag.find('div', attrs='ptab1-wrap').find('table', attrs='ptab ptab2 paneltab hov-tab').find('tr') is not None
    ):
        total_tag = top_tag.find('div', attrs='ptab1-wrap').find('table', attrs='ptab ptab2 paneltab hov-tab')
        total_data = dict()
        total_each_score = total_tag.find('tr', attrs='s tally').find_all('td')[3:-1]
        total_grade_exists = True
        for i, single_score in enumerate(total_each_score):
            if single_score.text.strip() == '-':
                continue
            total_grade_exists = single_score.find('span') is not None
            if total_grade_exists:
                grade = int(single_score.find('span').text.strip())
                score_text = list(single_score.find('br').next_siblings)[0].text.strip()
                if score_text == '-':
                    score = 0.
                else:
                    score = float(score_text)
                total_data[f'J{i}'] = [grade, score]
            else:
                score_text = single_score.text.strip()
                if score_text == '-':
                    score = 0.
                else:
                    score = float(score_text)
                total_data[f'J{i}'] = [score]
        if total_grade_exists:
            total_df = pd.DataFrame(total_data, index=['grade', 'score'])
        else:
            total_df = pd.DataFrame(total_data, index=['score'])
    else:
        total_df = None

    # `TES_score_df`
    TES_data_tag = None
    if top_tag.find('div', attrs='ptab2-wrap') is not None and top_tag.find('div', attrs='ptab2-wrap').find('table', attrs='tes-tab ptab ptab2 hov-tab') is not None:
        TES_scores_tag = top_tag.find('div', attrs='ptab2-wrap').find('table', attrs='tes-tab ptab ptab2 hov-tab')
        TES_data_tag = TES_scores_tag.find_all('tr')
        TES_head = TES_data_tag[0]
        TES_data_tag = TES_data_tag[1:]

        TES_cols = TES_head.find_all('td')
        TES_cols.pop(0)
        TES_cols.pop(1)
        TES_cols.pop(2)
        if TES_cols[2].find('span', attrs='goe-m') is not None:
            TES_cols[2].find('span', attrs='goe-m').extract()
        TES_cols = [tag.text.strip() for tag in TES_cols]

        TES_score_data = []
        for row in TES_data_tag[:-1]:
            data_lt = row.find_all('td')[1:]
            data_lt.pop(1)
            data_lt.pop(2)
            data_lt[0].find('sup').extract()
            if data_lt[2].find('span', attrs='goe-m') is not None:
                data_lt[2].find('span', attrs='goe-m').extract()
            TES_score_data.append({col: data.text.strip() for col, data in zip(TES_cols, data_lt)})

        TES_score_df = pd.DataFrame(TES_score_data)
    else:
        TES_score_df = None

    # `TES_tally_df`
    if TES_data_tag is not None and TES_data_tag[-1].find('tr') is not None:
        TES_total_data = dict()
        TES_total_each_score = TES_data_tag[-1].find_all('td')[1:-1]
        TES_grade_exists = True
        for i, single_score in enumerate(TES_total_each_score):
            TES_grade_exists = TES_grade_exists and (single_score.find('span') is not None)
            if TES_grade_exists:
                grade = int(single_score.find('span').text.strip())
                score_text = list(single_score.find('br').next_siblings)[0].text.strip()
                if score_text == '-':
                    score = -1.
                else:
                    score = float(score_text)
                TES_total_data[f'J{i}'] = [grade, score]
            else:
                score_text = single_score.text.strip()
                if score_text == '-':
                    score = 0.
                else:
                    score = float(score_text)
                TES_total_data[f'J{i}'] = [score]
        if TES_grade_exists:
            TES_tally_df = pd.DataFrame(TES_total_data, index=['grade', 'score'])
        else:
            TES_tally_df = pd.DataFrame(TES_total_data, index=['score'])
    else:
        TES_tally_df = None

    # `PCS_grade_df`, `PCS_score_df`
    PCS_data_tag = None
    if top_tag.find('div', attrs='ptab2-wrap') is not None and top_tag.find_all('div', attrs='ptab2-wrap')[-1].find('table', attrs='ptab ptab2 hov-tab') is not None:
        PCS_scores_tag = top_tag.find_all('div', attrs='ptab2-wrap')[-1].find('table', attrs='ptab ptab2 hov-tab')
        PCS_data_tag = PCS_scores_tag.find_all('tr')
        PCS_head = PCS_data_tag[0]
        PCS_data_tag = PCS_data_tag[1:]

        PCS_cols = [tag for tag in PCS_head.find_all('td') if tag.text.strip() != '']
        PCS_cols = [tag.text.strip() for tag in PCS_cols]

        PCS_data = []
        for row in PCS_data_tag[:-1]:
            data_lt = row.find_all('td')
            data_lt = [data for data in data_lt if data.text.strip() != '']
            PCS_data.append({col: data.text.strip() for col, data in zip(PCS_cols, data_lt)})

        PCS_total_df = pd.DataFrame(PCS_data)
        for col in PCS_total_df.columns:
            PCS_total_df[col] = PCS_total_df[col].str.split('  ', expand=False)
        for col in PCS_total_df.columns:
            if (PCS_total_df[col].apply(len) == 1).any():
                PCS_total_df.loc[
                    PCS_total_df[col].apply(len) == 1, 
                    col
                ] = PCS_total_df[col][PCS_total_df[col].apply(len) == 1].apply(lambda x: [None] + x)

        PCS_total_df = PCS_total_df.explode([col for col in PCS_total_df.columns])

        PCS_grade_df = PCS_total_df[0::2]
        PCS_score_df = PCS_total_df[1::2]
    else:
        PCS_grade_df = None
        PCS_score_df = None

    # `PCS_tally_df`
    if PCS_data_tag is not None and PCS_data_tag[-1].find('td') is not None:
        PCS_total_data = dict()
        PCS_total_each_score = PCS_data_tag[-1].find_all('td')[1:-1]
        PCS_grade_exists = True
        for i, single_score in enumerate(PCS_total_each_score):
            if single_score.text.strip() == '-':
                continue
            PCS_grade_exists = single_score.find('span') is not None
            if PCS_grade_exists:
                grade = int(single_score.find('span').text.strip())
                score_text = list(single_score.find('br').next_siblings)[0].text.strip()
                if score_text == '-':
                    score = 0.
                else:
                    score = float(score_text)
                PCS_total_data[f'J{i}'] = [grade, score]
            else:
                score_text = single_score.text.strip()
                if score_text == '-':
                    score = 0.
                else:
                    score = float(score_text)
                PCS_total_data[f'J{i}'] = [score]
        if PCS_grade_exists:
            PCS_tally_df = pd.DataFrame(PCS_total_data, index=['grade', 'score'])
        else:
            PCS_tally_df = pd.DataFrame(PCS_total_data, index=['score'])
    else:
        PCS_tally_df = None

    if top_tag.find('div', attrs='ptab5-wrap') is not None and top_tag.find_all('div', attrs='ptab5-wrap')[-1].find('td', attrs='r pcs') is not None:
        PCS_total_tag = top_tag.find_all('div', attrs='ptab5-wrap')[-1].find('td', attrs='r pcs')

        PCS_br_tag = PCS_total_tag.find('br')
        PCS_grade = list(PCS_br_tag.previous_siblings)[0].strip()
        PCS_score = list(PCS_br_tag.next_siblings)[0].strip()
    else:
        PCS_grade = None
        PCS_score = None

    return (
        total_df, 
        TES_score_df, 
        TES_tally_df, 
        PCS_grade_df, 
        PCS_score_df, 
        PCS_tally_df, 
        {
            'PCS_grade': PCS_grade,
            'PCS_score': PCS_score,
        }
    )

# Controller Component for Figure Skating Score
class MainCrawler:
    config = {
        'PlayerCrawler-config': None,
    }
    
    def __init__(
            self,
            root_url: Union[str, None]=None, 
            header=None, 
            config: Union[dict, None]=None
        ):
        if root_url is not None:
            self.root_url = root_url
        else:
            self.root_url = 'https://skatingscores.com'
        
        if header is not None:
            self.header = header
        else:
            self.header = { 
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98Safari/537.36', 
                'Accept-Language': 'en-US'
            }
        
        if config is not None:
            self.config = config

        self._player_crawler = PlayerCrawler(
            root_url=self.root_url,
            header=self.header,
            config=self.config['PlayerCrawler-config'],
        )

    @property
    def player_crawler(self):
        return self._player_crawler
    
    def change_player_crawler_attr(self, attr_name: str, new_value):
        if hasattr(self._player_crawler, attr_name):
            setattr(self._player_crawler, attr_name, new_value)
        else:
            AttributeError(f"player_crawler has no attribute '{attr_name}'")
