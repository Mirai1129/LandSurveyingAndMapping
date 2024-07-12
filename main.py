import time

from scripts import CSVProcessor, CadasMapPosition, EasymapCrawler


def main():
    processor = CSVProcessor()
    crawler = EasymapCrawler()
    cadas_position = CadasMapPosition()

    for region_code in processor.list_matching_files():
        df = processor.read_csv_files(region_code)

        if df is not None:
            for index, row in df.iterrows():
                city_name = processor.get_county_name(region_code)
                township_name = row['region_name']
                section = row['section']
                land_number = row['land_serial_number']

                if section and land_number:
                    section_number = processor.find_towncode(city_name, township_name, section, row['sub_section'])
                    if section_number == '':
                        continue

                    if section_number:
                        time.sleep(1.5)
                        land_number_found = crawler.run_process_flow_to_get_land_number(
                            city_name,
                            township_name,
                            section_number,
                            land_number
                        )
                        if land_number_found:
                            cadas_position.set_parameters(region_code.upper(), section_number, land_number_found)
                            position_data = cadas_position.fetch_position()

                            if position_data:
                                df.at[index, 'repX'] = position_data['repX']
                                df.at[index, 'repY'] = position_data['repY']
                                df.at[index, 'ldX'] = position_data['ldX']
                                df.at[index, 'ldY'] = position_data['ldY']
                                df.at[index, 'rtX'] = position_data['rtX']
                                df.at[index, 'rtY'] = position_data['rtY']
                            else:
                                # 若 position_data 是 None，則跳過該項
                                print(f"Skipping index {index} due to missing data.")
                        else:
                            # 若未找到土地號碼，則跳過該項
                            print(f"Skipping index {index} due to missing land number.")

            processor.save_results_to_csv(df, f"{region_code}_lvr_land_a.csv")
    crawler.close_driver()


if __name__ == '__main__':
    main()
