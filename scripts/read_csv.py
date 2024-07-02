import os

import pandas as pd  # 建議使用 pandas 來處理 CSV 檔案


def get_matching_files(directory_path: str = 'opendata/lands') -> list[str]:
    all_files = os.listdir(directory_path)
    matching_file = f"{directory_path}/*.csv"
    matching_files = []
    if


def read_opendata_region_files(region_code: str, directory: str = 'opendata/lands') -> pd.DataFrame:
    """
    讀取指定資料夾中符合 {region_code}_lvr_land_a.csv 格式的檔案。

    :param region_code: 地區代碼（小寫），例如 'j' 代表新竹縣
    :param directory: 儲存 CSV 檔案的資料夾
    :return: pandas DataFrame
    """
    all_files = os.listdir(directory)

    matching_file = f"{region_code}_lvr_land_a.csv"

    if matching_file in all_files:
        file_path = os.path.join(directory, matching_file)
        print(f"Reading file: {file_path}")
        df = pd.read_csv(file_path)
        return df
    else:
        print(f"No matching file found for region code '{region_code}' in directory '{directory}'.")
        return None


if __name__ == "__main__":
    df = read_opendata_region_files('j')
    if df is not None:
        print(df.head())
