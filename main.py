import os

import pandas as pd

# read csv data
land_information_data = pd.read_csv(f'opendatas/x_lvr_land_a.csv', skiprows=1)
town_code_data = pd.read_csv(f'opendatas/towncode.csv')

# land information initialize
LAND_ADDRESS = "land sector position building sector house number plate"
LAND_USING_TARGET = "non-metropolis land use"


def read_csv_files(region_code):
    directory = 'opendatas/test'  # 檔案所在的目錄
    all_files = os.listdir(directory)

    matching_files = [
        file for file in all_files
        if file.lower() == f"{region_code}_lvr_land_a.csv"
    ]

    for file in matching_files:
        file_path = os.path.join(directory, file)
        print(f"Reading file: {file_path}")
        data = pd.read_csv(file_path, skiprows=1)
        print(data.head())

    # TODO 讀取縣市土地檔案裡的鄉鎮市區以及地號

    # TODO 利用縣市以及鄉鎮市區讀取 land_code.csv 的地段代碼

    # TODO 抓取地號代碼（爬蟲）


def main() -> None:
    read_csv_files("j")


if __name__ == '__main__':
    main()
