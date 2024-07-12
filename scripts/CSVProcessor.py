import os
import re

import pandas as pd

from modules import CODE_TO_REGION


class CSVProcessor:
    def __init__(self, directory='opendata/lands'):
        self.directory = directory

    def get_county_name(self, region_code):
        """將 region_code 轉換為縣市名稱"""
        return CODE_TO_REGION.get(region_code, "未知地區")

    def list_matching_files(self):
        """
        列出符合 {region_code}_lvr_land_a.csv 格式的文件，並返回匹配的 region_code 列表。
        """
        all_files = os.listdir(self.directory)
        pattern = re.compile(r'([a-z])_lvr_land_a\.csv')
        return [match.group(1) for file_name in all_files if (match := pattern.match(file_name))]

    def split_segment_and_land_number(self, text):
        """分割段名、小段和地號"""
        pattern_full = re.compile(r'([\u4e00-\u9fa5]+)段([\u4e00-\u9fa5]+)?小段[^0-9]*([0-9]+)地號')
        pattern_simple = re.compile(r'([\u4e00-\u9fa5]+)段[^0-9]*([0-9]+)地號')

        if match_full := pattern_full.match(text):
            return {'section': match_full.group(1), 'sub_section': match_full.group(2),
                    'land_serial_number': match_full.group(3)}
        elif match_simple := pattern_simple.match(text):
            return {'section': match_simple.group(1), 'sub_section': None, 'land_serial_number': match_simple.group(2)}
        else:
            return None

    def read_csv_files(self, region_code):
        """
        讀取並處理符合 {region_code}_lvr_land_a.csv 格式的文件。
        """
        matching_file = f"{region_code}_lvr_land_a.csv"
        file_path = os.path.join(self.directory, matching_file)

        if not os.path.exists(file_path):
            print(f"No matching file found for region code '{region_code}' in directory '{self.directory}'.")
            return None

        df = pd.read_csv(file_path, skiprows=1)
        required_columns = ['The villages and towns urban district',
                            'land sector position building sector house number plate']

        if not all(col in df.columns for col in required_columns):
            print(f"Some of the required columns are missing in the file: {file_path}")
            return None

        df['land_code'] = region_code
        df['land_name'] = self.get_county_name(region_code)
        df['road_name'] = df['land sector position building sector house number plate']
        df['region_name'] = df['The villages and towns urban district']

        split_results = df['road_name'].apply(self.split_segment_and_land_number)
        df['section'] = split_results.apply(lambda x: x['section'] if x else None)
        df['sub_section'] = split_results.apply(lambda x: x['sub_section'] if x else None)
        df['land_serial_number'] = split_results.apply(lambda x: x['land_serial_number'] if x else None)

        return df

    def find_towncode(self, land_name, region_name, section, sub_section,
                      towncode_file='opendata/towncode/towncode.csv'):
        """
        根據縣市名稱、鄉鎮名稱、段和小段查找對應的代碼。
        """
        towncode_df = pd.read_csv(towncode_file)
        matching_rows = towncode_df[(towncode_df['縣市名稱'] == land_name) &
                                    (towncode_df['鄉鎮名稱'] == region_name) &
                                    (towncode_df['段'] == section)]
        if sub_section:
            matching_rows = matching_rows[matching_rows['小段'] == sub_section]

        if not matching_rows.empty:
            towncode = matching_rows['代碼'].values[0]
            towncode_item = towncode.item()
            formatted_num = '{:04d}'.format(towncode_item)
            return formatted_num
        else:
            print(
                f"No matching towncode found for land: {land_name}, region: {region_name}, section: {section}, sub-section: {sub_section}.")
            return None

    def save_results_to_csv(self, result_df, original_filename, output_directory='output'):
        """
        將結果保存到指定目錄下的 CSV 文件中，文件名為 {原檔名}_result.csv
        """
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        output_filename = f"{os.path.splitext(original_filename)[0]}_result.csv"
        output_filepath = os.path.join(output_directory, output_filename)
        result_df.to_csv(output_filepath, index=False, encoding='utf-8-sig')
        print(f"Results saved to {output_filepath}")
