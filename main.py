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


def main() -> None:
    # print(get_region_code("新竹縣"))
    # print(town_code_data['段'])
    read_csv_files("j")


if __name__ == '__main__':
    main()
