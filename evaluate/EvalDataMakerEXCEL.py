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
    result_dir_name = 'eval_input'
    result_dir_ex_name = 'eval_input_ex'

    # 各拠点を処理
    for location_path in tqdm(list(dir_path.glob('*'))):
        result_dir_path = location_path / result_dir_name
        result_dir_path.mkdir(exist_ok=True)

        result_dir_ex_path = location_path / result_dir_ex_name
        result_dir_ex_path.mkdir(exist_ok=True)
        for content_type in ['solar', 'surplus30p', 'battery30']:
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
            save_file_path = result_dir_path / file_name

            # 入力ファイル名と日付の範囲
            start_date = datetime(2022, 3, 1)
            end_date = datetime(2023, 1, 31)

            # 日付がstart_date以降のシートだけを選択して、新しいExcelファイルに保存する
            filtered_sheets = {sheet_name: sheet for sheet_name, sheet in sheets.items() if
                               start_date <= datetime.strptime(sheet_name, '%Y-%m-%d') <= end_date}
            output_file = save_file_path
            with pd.ExcelWriter(output_file) as writer:
                for sheet_name, sheet in filtered_sheets.items():
                    sheet.to_excel(writer, sheet_name=sheet_name, index=False)

            # 3日目以降の追加教師データ
            start_date = datetime(2023, 2, 1)
            end_date = datetime(2023, 2, 26)
            delta = timedelta(days=1)

            current_date = start_date
            while current_date <= end_date:
                # 対象の日付だけにする
                filtered_sheets = {sheet_name: sheet for sheet_name, sheet in sheets.items() if
                                   start_date <= datetime.strptime(sheet_name, '%Y-%m-%d') <= current_date}

                two_days_later = current_date + timedelta(days=2)
                output_file = result_dir_ex_path.joinpath(
                    f"{no_ext_file_name}_{two_days_later.strftime('%Y-%m-%d')}.xlsx"
                )
                print(output_file)

                with pd.ExcelWriter(output_file) as writer:
                    for sheet_name, sheet in filtered_sheets.items():
                        sheet.to_excel(writer, sheet_name=sheet_name, index=False)

                current_date += delta