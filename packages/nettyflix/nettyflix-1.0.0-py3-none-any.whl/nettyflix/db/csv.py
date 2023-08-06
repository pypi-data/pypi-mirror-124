import pandas as pd
from pathlib import Path


def connect_csv():
    df = pd.read_csv('movies.csv')
    return df