import os
import openpyxl
from tqdm import tqdm
from pathlib import Path
import pandas as pd
import shutil
from datetime import datetime, timedelta

if __name__ == '__main__':
    # ディレクトリのパスを指定
    dir_path = Path('../data/2023_devday_data')
    result_dir_name = 'eval_input'
    result_dir_ex_name = 'eval_input_ex'

    # 各拠点を処理
    for location_path in tqdm(dir_path.glob('*')):
        result_dir_path = location_path / result_dir_name
        result_dir_path.mkdir(exist_ok=True)

        result_dir_ex_path = location_path / result_dir_ex_name
        result_dir_ex_path.mkdir(exist_ok=True)

        for csv_file_path in location_path.glob('*.csv'):
            # CSVファイルを読み込む
            df = pd.read_csv(csv_file_path)

            # target_dateを日時型に変換する
            df['target_date_tmp'] = pd.to_datetime(df['target_date']).dt.date

            # 学習用: 2021年2月1日から2022年1月31日までの行を抽出する
            start_date = pd.to_datetime('2022-02-01').date()
            end_date = pd.to_datetime('2023-01-31').date()
            output_df = df[(df['target_date_tmp'] >= start_date) & (df['target_date_tmp'] <= end_date)]

            # 抽出結果をCSVファイルとして保存する
            save_path = result_dir_path / csv_file_path.name
            print(save_path)
            output_df.drop(columns=['target_date_tmp']).to_csv(save_path)

            # 3日目以降の評価用データ
            start_date = datetime(2023, 2, 1).date()
            end_date = datetime(2023, 2, 26).date()
            delta = timedelta(days=1)

            current_date = start_date
            while current_date <= end_date:
                # 対象の日付だけにする
                output_df = df[(df['target_date_tmp'] >= start_date) & (df['target_date_tmp'] <= current_date)]

                two_days_later = current_date + timedelta(days=2)
                save_path = result_dir_ex_path.joinpath(csv_file_path.stem + f"_{two_days_later.strftime('%Y-%m-%d')}.csv")
                print(save_path)
                output_df.drop(columns=['target_date_tmp']).to_csv(save_path)
                current_date += delta