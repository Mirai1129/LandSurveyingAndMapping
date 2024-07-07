# main.py
from modules.region_processor import process_region_code
from scripts import CSVProcessor, CadasMapPosition, EasymapCrawler


def main():
    csv_processor = CSVProcessor()
    cadas_processor = CadasMapPosition()
    easymap_crawler = EasymapCrawler()
    matching_region_codes = csv_processor.list_matching_files()
    print(f"Found matching region codes: {matching_region_codes}")

    for region_code in matching_region_codes:
        process_region_code(region_code, csv_processor)


if __name__ == "__main__":
    main()
