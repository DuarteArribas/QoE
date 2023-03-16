import pandas as pd
import os
import shutil

def remove_user(user):
    shutil.rmtree('subjective_results/' + user)

def check_user(user, mos_df):
    user_df = [pd.read_csv(f'{user}/{codec}', index_col=0) for codec in os.listdir(user)]
    # TODO: Encontrar função do pandas ou outra coisa qualquer para verificar se o user é outlier (user_df e mos_df são listas de dataframes, cada uma com um dataframe de cada codec)

if __name__ == '__main__':
    codec_list = [codec.split('Results')[0].upper() for codec in os.listdir('mos_results')]
    mos_df = [pd.read_csv(f'mos_results/{codec}', index_col=0) for codec in os.listdir('mos_results')]
    print(codec_list)

    # Go through the users
    for user in os.listdir('subjective_results'):
        check_user('subjective_results/' + user, mos_df)