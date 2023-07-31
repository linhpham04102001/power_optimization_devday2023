import pandas as pd
import numpy as np
import datetime
from pathlib import Path
from tqdm import tqdm
from sklearn.metrics import mean_absolute_percentage_error

# for real evaluation
# start_date = datetime.date(2023, 3, 1)
# end_date = datetime.date(2023, 3, 31)

# for test evaluation
start_date = datetime.date(2023, 2, 1)
end_date = datetime.date(2023, 2, 28)

dir_path = Path('../data/2023_devday_data')
input_dir_name = 'eval_input'
input_dir_ex_name = 'eval_input_ex'
eval_dir_y_name = 'eval_y'


def get_excel_input(input_dir_path, input_dir_ex_path, category, date_str):
    # input
    input_files = list(input_dir_path.glob(f"*{category}*.xlsx"))
    if category == 'battery':
        assert 1 >= len(input_files) >= 0
    else:
        assert 2 >= len(input_files) >= 1
    # extra input
    ex_input_files = list(input_dir_ex_path.glob(f"*{category}*_{date_str}.xlsx"))
    assert 1 >= len(ex_input_files) >= 0
    return input_files, ex_input_files

def get_csv_input(input_dir_path, input_dir_ex_path, category, date_str):
    # input
    input_files = list(input_dir_path.glob(f"*{category}*.csv"))
    assert len(input_files) == 1
    # extra input
    ex_input_files = list(input_dir_ex_path.glob(f"*{category}*_{date_str}.csv"))
    assert 1 >= len(ex_input_files) >= 0
    return input_files, ex_input_files

def predict(
    location_path, target_date,
    solar_input_files, solar_ex_input_files, surplus_input_files, surplus_ex_input_files,
    battery_input_files, battery_ex_input_files, solar_csv_input_files, solar_csv_ex_input_files,
    cloud_csv_input_files, cloud_csv_ex_input_files, weather_csv_input_files, weather_csv_ex_input_files
):
    """
    plaese implement your prediction method here
    :return: 48 * power_generation and power_demand
    """
    power_generation = [1] * 48
    power_demand = [1] * 48
    return power_generation, power_demand



def evaluate():
    # evaluate for each location
    power_generation_pred = []
    power_generation_truth = []
    power_demand_pred = []
    power_demand_truth = []

    for location_path in tqdm(list(dir_path.glob('*'))):
        input_dir_path = location_path / input_dir_name
        input_dir_ex_path = location_path / input_dir_ex_name
        eval_dir_y_path = location_path / eval_dir_y_name

        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            print(f"predicting for location: {location_path.name}, date: {date_str}")

            # prepare the input data (EXCEL)
            # solar input
            solar_input_files, solar_ex_input_files = get_excel_input(
                input_dir_path, input_dir_ex_path, 'solar', date_str
            )
            # surplus input
            surplus_input_files, surplus_ex_input_files = get_excel_input(
                input_dir_path, input_dir_ex_path, 'surplus', date_str
            )
            # battery input
            battery_input_files, battery_ex_input_files = get_excel_input(
                input_dir_path, input_dir_ex_path, 'battery', date_str
            )
            # prepare input data (CSV)
            # solar
            solar_csv_input_files, solar_csv_ex_input_files = get_csv_input(
                input_dir_path, input_dir_ex_path, 'solar', date_str
            )
            # cloud
            cloud_csv_input_files, cloud_csv_ex_input_files = get_csv_input(
                input_dir_path, input_dir_ex_path, 'cloud', date_str
            )
            # weather
            weather_csv_input_files, weather_csv_ex_input_files = get_csv_input(
                input_dir_path, input_dir_ex_path, 'weather', date_str
            )

            # your prediction method
            power_generation, power_demand = predict(
                location_path, date_str,
                solar_input_files, solar_ex_input_files, surplus_input_files, surplus_ex_input_files,
                battery_input_files, battery_ex_input_files, solar_csv_input_files, solar_csv_ex_input_files,
                cloud_csv_input_files, cloud_csv_ex_input_files, weather_csv_input_files, weather_csv_ex_input_files
            )

            power_generation_pred.extend(power_generation)
            power_demand_pred.extend(power_demand)

            # get truth data
            power_generation_truth_path = eval_dir_y_path / f"solar_{date_str}.csv"
            power_generation_truth_df = pd.read_csv(power_generation_truth_path, header=None).fillna(0)
            assert not power_generation_truth_df.iloc[:, 0].hasnans
            power_generation_truth_list = power_generation_truth_df.iloc[:, 0].values.tolist()
            power_generation_truth.extend(power_generation_truth_list)

            power_demand_truth_path = eval_dir_y_path / f"demand_{date_str}.csv"
            power_demand_truth_df = pd.read_csv(power_demand_truth_path, header=None).fillna(0)
            assert not power_demand_truth_df.iloc[:, 0].hasnans
            power_demand_truth_list = power_demand_truth_df.iloc[:, 0].values.tolist()
            power_demand_truth.extend(power_demand_truth_list)

            # increment current_date
            current_date += datetime.timedelta(days=1)

    power_generation_metric = mean_absolute_percentage_error(power_generation_pred, power_generation_truth)
    power_demand_truth_metric = mean_absolute_percentage_error(power_demand_pred, power_demand_truth)
    return (power_generation_metric + power_demand_truth_metric) / 2


if __name__ == '__main__':
    metric = evaluate()
    print(f"your metrics is {metric}!")
