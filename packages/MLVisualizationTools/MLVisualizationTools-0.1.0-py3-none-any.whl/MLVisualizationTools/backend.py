from typing import List, Dict
import pandas as pd
from os.path import sep as filesep

#Backend functions and classes used by the other scripts

def colinfo(data: pd.DataFrame, exclude:List[str] = None) -> List[Dict]:
    """
    Helper function for generating column info dict for a datframe

    :param data: A pandas Dataframe
    :param exclude: A list of data items to exclude
    """
    if exclude is None:
        exclude = []

    coldata = []
    for item in data.columns:
        if item not in exclude:
            coldata.append({'name': item, 'mean': data[item].mean(),
                            'min': data[item].min(), 'max': data[item].max()})
    return coldata

def fileloader(start: str, target: str):
    """Generates relative file paths"""
    s = start.split(filesep)
    s = s[:-1]
    s = filesep.join(s)
    return s + filesep + target