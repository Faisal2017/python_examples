import os
import glob

import pandas as pd
import duckdb

from question_1_sql import Q_1_SQL
from question_2_sql import Q_2_SQL
from question_3_sql import Q_3_sql


DF_LIST = {}

# csv to df data type mapping
DATAFRAME_TYPES = {
    'string': 'object',
    'integer': 'int',
    'datetime': 'datetime64[ns]',
    'decimal': 'float64',
}


def read_csv_files_anc_convert_to_df():
    cwd = os.getcwd()
    all_csv_files = glob.glob(os.path.join(cwd, "csv_files/*.csv"))

    transaction_data_types = {}

    for csv_file in all_csv_files:
        csv_name = csv_file.split('.')[0].split('/')[-1]

        df = pd.read_csv(csv_file)

        trimmed_df = df.drop([0, 1]).drop(columns='Column Name')

        data_types = df.iloc[0][1:]

        for i, v in data_types.items():
            v2 = v.replace('(', '').replace(')', '')

            convert_type_to_df_type = DATAFRAME_TYPES[v2]

            transaction_data_types[i] = convert_type_to_df_type

        final_df = trimmed_df.astype(transaction_data_types)

        DF_LIST[csv_name] = final_df

        transaction_data_types = {}


if __name__ == "__main__":
    read_csv_files_anc_convert_to_df()

    # convert DF_LIST to top level variables i.e. variable DF_LIST['account'] becomes account
    # allows duckdb to pick up df's automatically
    for key, val in DF_LIST.items():
        exec(key + '=val')

    q_1 = duckdb.query(Q_1_SQL)
    print('Question 1 : ', q_1)
    # TODO ? Better way to select valid accounts other than specifying all product types ??

    q_2 = duckdb.query(Q_2_SQL)
    print('Question 2 : ', q_2)

    # TODO - use this as per question, as using earlier date to pull thru some rows
    # WHERE date_trunc('day', account_open_date) = '2018-07-01';

    q_3 = duckdb.query(Q_3_sql)
    print('Question 3 : ', q_3)

    # TODO - use this as per question, as using earlier date to pull thru some rows
    # WHERE date_trunc('day', account_open_date) = '2018-07-01';
