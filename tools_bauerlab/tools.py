import pandas as pd
from pathlib import Path


def generate_default_re():
    treatments = ['Control-Rats', 'PPS-Rats']
    stages = ['BL', 'EPG']

    sub_treat = '|'.join(treatments)
    sub_id = '\d{4,5}'
    sub_stage = '|'.join(stages)
    sub_date = '\d{4}-\d{2}-\d{2}'
    sub_time = '\d{2}-\d{2}-\d{2}'
    sub_suffix = 'filter.csv'

    re = (r'('+sub_treat+
          ')/('+sub_id+
          ')/(?:'+sub_id+
          ')/('+sub_stage+
          ')/(?:(?:'+sub_stage+')-)?('+sub_date+')'+
          'T('+sub_time+')'+
          '-' + sub_suffix)

    return re


def generate_fileinfo_table(path, re=None):
    """
    Generate file info table by recursively scanning for all files in path
    that match regular expression
    """

    if not re:
        re = generate_default_re()

    ls_fname = [str(i.absolute()) for i in Path(path).rglob('*')]
    df = pd.DataFrame({'fname': ls_fname})
    df_extract = df['fname'].str.extract(re, expand=True)

    df_extract = df_extract.rename(
        columns={
            0: 'treatment',
            1:'id',
            2:'stage',
            3:'date',
            4:'time'})

    df = df.join(df_extract)

    df = df.dropna()
    df = df.reset_index(drop=True)

    # merge date and time to datetime
    df = _assign_datetime(df, drop_columns=True)
    
    # convert id to int
    df['id'] = pd.to_numeric(df['id'])
    
    return df
        

def _assign_datetime(df, drop_columns=False):
    df['datetime'] = pd.to_datetime(df['date']+'-'+df['time'], format="%Y-%m-%d-%H-%M-%S")
    if drop_columns:
        df = df.drop(['date', 'time'], axis=1, inplace=False)
    return df


def get_stageonset(df):
    """
    For each animal, get the minimal time for each stage
    """
#    df_i = pd.DataFrame.copy(df)
    onst = df.groupby(['id', 'stage'])['datetime'].min()
    df_on = pd.DataFrame(onst).reset_index()
    
    # convert id to int
#    df_on[id] = pd.to_numeric(df_on['id'])
    
    return df_on


def get_deltat_stageonset(
        df, df_on=None, return_total_seconds=False, return_deltat=False):
    """
    Get time since stageonset
    """

    if not df_on:
        df_on = get_stageonset(df)
    
    ls_delta_t = []
    for i, row_i in df.iterrows():
        # define time vector
        id_i = row_i['id']
        stage_i = row_i['stage']
        t_i = row_i['datetime']
        t_onset = df_on[
            (df_on['stage'] == stage_i) &
            (df_on['id'] == id_i)]['datetime'].values[0]
        delta_t = t_i-t_onset
        if return_total_seconds:
            delta_t = delta_t.total_seconds()
        ls_delta_t.append(delta_t)

    if return_deltat:
        return ls_delta_t
    else:
        df['deltat_stageonset'] = ls_delta_t
        return df
