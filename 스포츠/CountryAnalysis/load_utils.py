import time
import random
from pprint import pprint
from typing import Union, Tuple, List, Callable
from pathlib import Path
import pickle

from tqdm.auto import tqdm

import numpy as np
import pandas as pd

def get_player_lt(main_path: Path) -> pd.DataFrame:
    player_path_lt = list(main_path.glob('*/'))
    noc_name_lt = [player_path.name for player_path in player_path_lt]
    noc_name_series = pd.Series(noc_name_lt)
    noc_series = noc_name_series.str.split('-').str[0].str.upper()
    name_series = noc_name_series.str.split('-').str[1]
    return pd.DataFrame({
        'noc': noc_series,
        'name': name_series,
        'access_key': noc_name_lt,
        'path': player_path_lt,
    })

def load_player_data(player_data_path: Path) -> dict:
    event_path_lt = list(player_data_path.glob('*.pkl'))
    result_data = dict()
    for event_path in event_path_lt:
        event_name = event_path.name
        event_name = event_name[event_name.find('-') + 1 : event_name.rfind('.')]
        with open(event_path, 'rb') as f:
            data = pickle.load(f)
        short_program_data = data[0]
        freeskating_data = data[1]
        if short_program_data is not None:
            short_program_data = {
                'total': short_program_data[0],
                'TES_score_df': short_program_data[1],
                'TES_tally_df': short_program_data[2],
                'PCS_grade_df': short_program_data[3],
                'PCS_score_df': short_program_data[4],
                'PCS_tally_df': short_program_data[5],
                'PCS_grade': short_program_data[6]['PCS_grade'],
                'PCS_score': short_program_data[6]['PCS_score'],
            }
        if freeskating_data is not None:
            freeskating_data = {
                'total': freeskating_data[0],
                'TES_score_df': freeskating_data[1],
                'TES_tally_df': freeskating_data[2],
                'PCS_grade_df': freeskating_data[3],
                'PCS_score_df': freeskating_data[4],
                'PCS_tally_df': freeskating_data[5],
                'PCS_grade': freeskating_data[6]['PCS_grade'],
                'PCS_score': freeskating_data[6]['PCS_score'],
            }
        result_data[event_name] = {
            'short_program': short_program_data,
            'freeskating': freeskating_data,
        }
    return result_data

def load_select_player_data(player_path_lt: List[pd.DataFrame]) -> dict:
    noc_name_lt = [player_path.name for player_path in player_path_lt]
    result_data = dict()
    for noc_name, player_path in zip(noc_name_lt, player_path_lt):
        result_data[noc_name] = (load_player_data(player_path))
    return result_data

def load_full_data(main_path: Path) -> dict:
    player_path_lt = list(main_path.glob('**'))
    return load_select_player_data(player_path_lt)

def detail_data_map(data: dict, map_func: Callable, select_func: Callable) -> pd.Series:
    result = []
    for player in data:
        for event_result in player:
            result.append(map_func(select_func(event_result)))
    return pd.Series(result)

def short_program_map(data: dict, map_func: callable, data_name: str):
    return detail_data_map(
        data,
        map_func,
        lambda x: x['short_program'][data_name]
    )

def freeskating_map(data: dict, map_func: Callable, data_name: str):
    return detail_data_map(
        data,
        map_func,
        lambda x: x['freeskating'][data_name]
    )

def get_score(scores: np.ndarray) -> float:
    if len(scores.shape) != 1 and scores.shape[0] != 1:
        scores = scores[1, :]
    
    if len(scores) >= 5:
        return np.sum(scores) - np.min(scores) - np.max(scores)
    else:
        return np.sum(scores)
    