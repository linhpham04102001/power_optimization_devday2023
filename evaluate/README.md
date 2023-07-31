
# How to Run Evaluator
- Download files from here  
https://drive.google.com/drive/folders/1jMahJ4oFGfI-41k5WHhe1NE7dQKAp0qw?usp=sharing
- Place `2023_devday_data` in `data` directory
- implement predict funtion in `Evaluator.py`
- run script
```
python Evaluator.py
```

## for real evaluation
we will run same script for `2023-03-01 ~ 2023-03-31`

# File Description

|FileName|Description|
|-----|-----|
|EvalDataMakerCSV.py|divide csv files into input and extra input|
|EvalDataMakerEXCEL.py|divide xlsx files into input and extra input|
|EvalDataMakerY.py|create truth data|

# Data Directory Structure 
```
.
├── v1
│   ├── eval_input
│   │      input data fixed part (2022-03-01 ~ 2023-01-31
│   ├── eval_input_ex
│   │      extra input data (to predict 2023-02-03, use `{hoge}_v00001_2023-02-03.csv`
│   │      `{hoge}_v00001_2023-02-03.csv` includes 2days before the date.
│   │      ex) `{hoge}_v00001_2023-02-05.csv` has 2023-02-01 ~ 2023-02-03
│   └── eval_y 
│   │      truth data to evaluate
├── v2
.....
```