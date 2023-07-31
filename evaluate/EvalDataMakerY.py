import os
import openpyxl
from tqdm import tqdm
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import shutil

if __name__ == '__main__':
    # ディレクトリのパスを指定
    dir_path = Path('../data/2023_devday_data')
    result_dir_y_name = 'eval_y'

    # 各拠点を処理
    for location_path in tqdm(list(dir_path.glob('*'))):
        result_dir_y_path = location_path / result_dir_y_name
        result_dir_y_path.mkdir(exist_ok=True)

        for content_type in ['solar', 'surplus30p']:
            target_files = list(location_path.glob(f"*{content_type}*.xlsx"))
            sheets_list = [pd.read_excel(x, sheet_name=None) for x in target_files]
            if len(target_files) > 1:
                sheets = {}
                for sheets_item in sheets_list:
                    sheets.update(sheets_item)

            elif len(target_files) == 1:
                sheets = pd.read_excel(target_files[0], sheet_name=None)

            else:
                continue

            # Excelファイルを開く
            file_path = location_path / target_files[0]
            file_name = file_path.name
            no_ext_file_name, ext = file_path.stem, file_path.suffix
            save_file_path = result_dir_y_path / file_name

            # 毎日分のデータを
            start_date = datetime(2023, 2, 1)
            end_date = datetime(2023, 2, 28)
            delta = timedelta(days=1)

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                this_df = sheets[date_str]

                data_df = this_df[5:]
                data_df.columns = this_df.iloc[4, :].values

                if content_type == 'surplus30p':
                    save_to = result_dir_y_path / f"demand_{date_str}.csv"
                    data_df['30101:電力量（Wh）'].to_csv(save_to, header=None, index=False)
                elif content_type == 'solar':
                    save_to = result_dir_y_path / f"{content_type}_{date_str}.csv"
                    data_df.iloc[:, 1:].sum(axis=1).to_csv(save_to, header=None, index=False)

                current_date += delta