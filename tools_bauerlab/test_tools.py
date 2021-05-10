import tools
import pandas as pd


def test_generate_default_re():
    # different naming conventions are present in Bauer data
    # Adjust regular expression accordingly

    ls_positive_cases = [
        '/home/jovyan/work/epilepsy-data/data/PPS-rats-from-Sebastian/Control-Rats/3266/3266/EPG/EPG-2016-04-08T07-59-34-filter.csv',
        '/home/jovyan/work/epilepsy-data/data/PPS-rats-from-Sebastian/Control-Rats/3263/3263/EPG/EPG-2016-03-28T07-59-42-filter.csv',
        '/home/jovyan/work/epilepsy-data/data/PPS-rats-from-Sebastian/PPS-Rats/32139/32139/EPG/2017-05-29T11-59-07-filter.csv'
        ]

    ls_negative_cases = [
        '/home/jovyan/work/epilepsy-data/data/PPS-rats-from-Sebastian/Control-Rats/3266/3266/modified_3d_files/EPG-2016-04-12T10-59-33-filter.csv',
        '/home/jovyan/work/epilepsy-data/data/PPS-rats-from-Sebastian/Control-Rats/3263/3263/EPG/EPG-2016-04-07T04-59-42-filter-5s-720-new.csv'
        ]

    re = tools.generate_default_re()
    df_pos = pd.DataFrame({'fname': ls_positive_cases})
    df_neg = pd.DataFrame({'fname': ls_negative_cases})

    df_pos = df_pos['fname'].str.extract(re, expand=True)
    df_neg = df_neg['fname'].str.extract(re, expand=True)

    assert df_pos.isnull().values.any() == False
    assert df_neg.isnull().values.any() == True
