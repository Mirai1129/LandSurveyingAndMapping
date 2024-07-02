import os

import pandas as pd

# region_code 與縣市名稱的對應表
region_mapping = {
    'j': '新竹縣',
    'a': '台北市',
    # 可以根據需要添加更多的對應
}


def get_county_name(region_code):
    """將 region_code 轉換為縣市名稱"""
    return region_mapping.get(region_code, "未知地區")


def read_csv_files(region_code, directory='opendata/lands'):
    """
    讀取並處理符合 {region_code}_lvr_land_a.csv 格式的文件。

    :param region_code: 地區代碼（小寫），例如 'j' 代表新竹縣
    :param directory: 儲存 CSV 檔案的資料夾
    :return: 返回一個包含縣市代碼、鄉鎮市區、土地位置的 DataFrame
    """
    matching_file = f"{region_code}_lvr_land_a.csv"

    # 列出資料夾中的所有文件
    all_files = os.listdir(directory)

    # 檢查文件是否存在於資料夾中
    if matching_file in all_files:
        file_path = os.path.join(directory, matching_file)
        print(f"Reading file: {file_path}")
        # 使用 pandas 來讀取 CSV 檔案
        df = pd.read_csv(file_path, skiprows=1)

        # 選取需要的欄位
        selected_columns = ['The villages and towns urban district',
                            'land sector position building sector house number plate']
        if not all(col in df.columns for col in selected_columns):
            print(f"Some of the required columns are missing in the file: {file_path}")
            return None

        result_df = df[selected_columns].copy()
        result_df['land_code'] = region_code
        result_df['land_name'] = get_county_name(region_code)
        result_df['road_name'] = result_df['land sector position building sector house number plate']
        result_df['region_name'] = result_df['The villages and towns urban district']


        return result_df
    else:
        print(f"No matching file found for region code '{region_code}' in directory '{directory}'.")
        return None


def find_towncode(region_code, town_name, land_position, towncode_file='opendata/towncode/towncode.csv'):
    """
    根據縣市代碼、鄉鎮名稱和土地位置查找對應的代碼。

    :param region_code: 縣市代碼
    :param town_name: 鄉鎮市區名稱
    :param land_position: 土地位置
    :param towncode_file: towncode.csv 的文件路徑
    :return: 對應的代碼，如果找到則返回，否則返回 None
    """
    # 讀取 towncode.csv
    towncode_df = pd.read_csv(towncode_file)

    # 過濾條件
    matching_row = towncode_df[(towncode_df['縣市名稱'] == region_code) &
                               (towncode_df['鄉鎮名稱'] == town_name) &
                               (towncode_df['段'].str.contains(land_position))]

    if not matching_row.empty:
        return matching_row['代碼'].values[0]
    else:
        print(
            f"No matching towncode found for region: {region_code}, town: {town_name}, land position: {land_position}.")
        return None


if __name__ == '__main__':
    # 整合應用的示範
    region_code = 'j'  # 可以根據需要更改地區代碼
    land_data_df = read_csv_files(region_code)

    if land_data_df is not None:
        for index, row in land_data_df.iterrows():
            print(land_data_df.iterrows())
            print(index, row)
            town_name = row['land_code']
            land_position = row['road_name']

            code = find_towncode(region_code, town_name, land_position)
            if code:
                print(f"Found code for {town_name}, {land_position}: {code}")
