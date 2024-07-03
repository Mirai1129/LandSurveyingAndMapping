import os
import re

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


def list_matching_files(directory='opendata/lands'):
    """
    列出符合 {region_code}_lvr_land_a.csv 格式的文件，並返回匹配的 region_code 列表。

    :param directory: 儲存 CSV 檔案的資料夾
    :return: 返回所有符合的 region_code 列表
    """
    all_files = os.listdir(directory)
    pattern = re.compile(r'([a-z])_lvr_land_a\.csv')
    matching_region_codes = []

    for file_name in all_files:
        match = pattern.match(file_name)
        if match:
            matching_region_codes.append(match.group(1))

    return matching_region_codes


def split_segment_and_land_number(text):
    """分割段名、小段和地號"""
    # 匹配 段, 小段 和 地號
    pattern_full = re.compile(r'([\u4e00-\u9fa5]+)段([\u4e00-\u9fa5]+)?小段[^0-9]*([0-9]+)地號')
    # 匹配 段 和 地號
    pattern_simple = re.compile(r'([\u4e00-\u9fa5]+)段[^0-9]*([0-9]+)地號')

    match_full = pattern_full.match(text)
    match_simple = pattern_simple.match(text)

    if match_full:
        section = match_full.group(1)
        sub_section = match_full.group(2) if match_full.group(2) else None
        land_serial_number = match_full.group(3)
        return {'section': section, 'sub_section': sub_section, 'land_serial_number': land_serial_number}

    elif match_simple:
        section = match_simple.group(1)
        sub_section = None
        land_serial_number = match_simple.group(2)
        return {'section': section, 'sub_section': sub_section, 'land_serial_number': land_serial_number}

    else:
        return None


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

        # 使用 pandas 來讀取 CSV 檔案，這樣可以確保第一行正確作為標頭
        df = pd.read_csv(file_path)

        # 確認第一行是否符合預期，並作為列名
        first_row = df.iloc[0]
        df.columns = first_row

        # 再次讀取檔案，跳過第一行，以獲得正確的資料
        df = pd.read_csv(file_path, header=1)

        # 選取需要的欄位
        selected_columns = ['The villages and towns urban district',
                            'land sector position building sector house number plate']
        if not all(col in df.columns for col in selected_columns):
            print(f"Some of the required columns are missing in the file: {file_path}")
            return None

        origin_df = pd.read_csv(file_path)
        print(origin_df.iloc[:0])

        result_df = df.copy()
        result_df['land_code'] = region_code
        result_df['land_name'] = get_county_name(region_code)
        result_df['road_name'] = result_df['land sector position building sector house number plate']
        result_df['region_name'] = result_df['The villages and towns urban district']

        # 將分割段名、小段和地號的結果存入 section, sub_section 和 land_serial_number 列中
        split_results = result_df['road_name'].apply(split_segment_and_land_number)
        result_df['section'] = split_results.apply(lambda x: x['section'] if x else None)
        result_df['sub_section'] = split_results.apply(lambda x: x['sub_section'] if x else None)
        result_df['land_serial_number'] = split_results.apply(lambda x: x['land_serial_number'] if x else None)

        return result_df
    else:
        print(f"No matching file found for region code '{region_code}' in directory '{directory}'.")
        return None


def find_towncode(land_name, region_name, section, sub_section, towncode_file='opendata/towncode/towncode.csv'):
    """
    根據縣市名稱、鄉鎮名稱、段和小段查找對應的代碼。

    :param land_name: 縣市名稱
    :param region_name: 鄉鎮市區名稱
    :param section: 段名
    :param sub_section: 小段名
    :param towncode_file: towncode.csv 的文件路徑
    :return: 對應的代碼，如果找到則返回，否則返回 None
    """
    # 讀取 towncode.csv
    towncode_df = pd.read_csv(towncode_file)

    # 過濾條件：匹配 縣市名稱、鄉鎮名稱 和 段
    matching_rows = towncode_df[(towncode_df['縣市名稱'] == land_name) &
                                (towncode_df['鄉鎮名稱'] == region_name) &
                                (towncode_df['段'] == section)]

    # 如果有小段，需要進一步匹配小段
    if sub_section:
        matching_rows = matching_rows[matching_rows['小段'] == sub_section]

    # 檢查是否有匹配的行
    if not matching_rows.empty:
        return matching_rows['代碼'].values[0]
    else:
        print(
            f"No matching towncode found for land: {land_name}, region: {region_name}, section: {section}, sub-section: {sub_section}.")
        return None


def save_results_to_csv(result_df, original_filename, output_directory='output'):
    """
    將結果保存到指定目錄下的 CSV 文件中，文件名為 {原檔名}_result.csv

    :param result_df: 包含結果的 DataFrame
    :param original_filename: 原始檔名，用於生成新的結果檔名
    :param output_directory: 儲存結果的資料夾
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 修改成繁體中文編碼
    output_filename = f"{os.path.splitext(original_filename)[0]}_result.csv"
    output_filepath = os.path.join(output_directory, output_filename)

    result_df.to_csv(output_filepath, index=False, encoding='utf-8-sig')  # 使用繁體中文編碼
    print(f"Results saved to {output_filepath}")


def main():
    # 列出符合的 region_code
    matching_region_codes = list_matching_files()

    print(f"Found matching region codes: {matching_region_codes}")

    original_filename = f"j_lvr_land_a.csv"
    land_data_df = read_csv_files("j")

    if land_data_df is not None:
        all_results = []

        for index, row in land_data_df.iterrows():
            land_name = row['land_name']
            region_name = row['region_name']
            section = row['section']
            sub_section = row['sub_section']

            code = find_towncode(land_name, region_name, section, sub_section)
            if code:
                print(
                    f"Found code for {land_name}, {region_name}, section: {section}, sub-section: {sub_section}: {code}")

            all_results.append({
                'land_code': "j",
                'land_name': land_name,
                'region_name': region_name,
                'section': section,
                'sub_section': sub_section,
                'land_serial_number': row['land_serial_number'],
                'towncode': code
            })

        # 如果有結果，合併原本的資料和新增的內容，然後保存到 CSV
        if all_results:
            result_df = pd.DataFrame(all_results)

            # 合併原本的資料和新增的內容
            combined_df = pd.concat([land_data_df, result_df], axis=1)

            save_results_to_csv(combined_df, original_filename)
        else:
            print(f"No results to save for j")


if __name__ == "__main__":
    main()
