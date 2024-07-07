def process_region_code(region_code, csv_processor):
    """處理單一 region_code 的資料"""
    original_filename = f"{region_code}_lvr_land_a.csv"
    land_data_df = csv_processor.read_csv_files(region_code)

    if land_data_df is None:
        return

    all_results = []

    for _, row in land_data_df.iterrows():
        land_name = row['land_name']
        region_name = row['region_name']
        section = row['section']
        sub_section = row['sub_section']

        code = csv_processor.find_towncode(land_name, region_name, section, sub_section)
        if code:
            print(f"Found code for {land_name}, {region_name}, section: {section}, sub-section: {sub_section}: {code}")

        all_results.append(code)

    if all_results:
        land_data_df['towncode'] = all_results
        csv_processor.save_results_to_csv(land_data_df, original_filename)
