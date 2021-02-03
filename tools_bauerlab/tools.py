import pandas as pd
from pathlib import Path

def generate_default_re():
    
    treatments = ['Control-Rats', 'PPS-Rats']
    stages = ['BL', 'EPG']

    sub_treat = '|'.join(treatments)
    sub_id = '\d{4}'
    sub_stage = '|'.join(stages)
    sub_date = '\d{4}-\d{2}-\d{2}'
    sub_time = '\d{2}-\d{2}-\d{2}'
    sub_suffix = 'filter.csv'

    re = (r'('+sub_treat+
          ')/('+sub_id+
          ')/(?:'+sub_id+
          ')/('+sub_stage+
          ')/'+'(?:'+sub_stage+
          ')-('+sub_date+')'+
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
    
    return df
        
