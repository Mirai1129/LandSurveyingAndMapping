import os

import pandas as pd

from modules import get_region_name
from scripts import read_opendata_region_files

# read csv data
land_information_data = pd.read_csv(f'opendata/x_lvr_land_a.csv', skiprows=1)
town_code_data = pd.read_csv(f'opendata/towncode/towncode.csv')

# land information initialize
LAND_ADDRESS = "land sector position building sector house number plate"
LAND_USING_TARGET = "non-metropolis land use"


def walk_opendata_folder(region_code):
    directory = 'opendata/lands'  # 檔案所在的目錄
    all_files = os.listdir(directory)
    region = get_region_name(region_code)

    matching_files = [
        file for file in all_files
        if file.lower() == f"{region_code}_lvr_land_a.csv"
    ]

    for file in matching_files:
        file_path = os.path.join(directory, file)
        print(f"Reading file: {file_path}")
        data = pd.read_csv(file_path, skiprows=1)
        print(data.head())

    print(region)
    # TODO 讀取縣市土地檔案裡的鄉鎮市區以及地號

    # TODO 利用縣市以及鄉鎮市區讀取 land_code.csv 的地段代碼

    # TODO 抓取地號代碼（爬蟲）


def read_csv_file(file_path: str) -> pd.DataFrame:
    """讀取指定的 CSV 檔案"""
    print(f"Reading file: {file_path}")
    data = pd.read_csv(file_path, skiprows=1)
    return data


def main() -> None:
    # walk_opendata_folder("j")
    read_opendata_region_files("x")


if __name__ == '__main__':
    main()
