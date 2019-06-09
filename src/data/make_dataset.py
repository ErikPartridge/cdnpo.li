# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import pandas as pd
import locale
import re
import numpy as np

# "1,000 (1/4)" = 250
def apply_fraction(s):
    if isinstance(s, int):
        return s
    if isinstance(s, float):
        if np.isnan(s):
            return 100
        return int(s)
    split = s.split()
    sample = int(split[0].replace(',', ''))
    regex = r"\/\d"
    if len(split) > 1:
        sample /= int(re.findall(regex, split[1])[0].replace("/", ""))
    return int(sample)

def parse_margin(s):
    if isinstance(s, float):
        return s
    trimmed = s.replace('±', '')
    split = trimmed.split()
    try:
        return float(split[0])
    except ValueError:
        return np.nan

def sort_margin_fraction(df):
    df = df.replace('-', np.nan)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    if "Margin" in list(df):
        df['Margin'] = df['Margin'].apply(lambda x: parse_margin(x))
    if "Sample" in list(df):
        df['Sample'] = df['Sample'].apply(lambda s: apply_fraction(s))
    df.sort_values('Date', inplace=True)
    df.index = df['Date']
    return df

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')
    df2019 = sort_margin_fraction(pd.read_csv("./data/raw/2019 Federal Polling.csv"))
    df2015 = sort_margin_fraction(pd.read_csv("./data/raw/2015 Federal Polling.csv"))
    df2011 = sort_margin_fraction(pd.read_csv("./data/raw/2011 Federal Polling.csv"))
    df2008 = sort_margin_fraction(pd.read_csv("./data/raw/2008 Federal Polling.csv"))
    df2019['Date'] = df2019["Date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    df2019.to_csv("./data/processed/2019_Federal.csv")
    df2015.to_csv("./data/processed/2015_Federal.csv")
    df2011.to_csv("./data/processed/2011_Federal.csv")
    df2008.to_csv("./data/processed/2008_Federal.csv")




if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    main()
