import xml.etree.ElementTree as ET

import requests


class CadasMapPosition:
    """與地籍地圖位置 API 交互的類。"""

    def __init__(self):
        """初始化方法，不需要參數。"""
        self.country_code = None  # 縣市代碼
        self.section_number = None  # 地段代碼
        self.land_number = None  # 地號
        self.url = None  # API請求的URL
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def set_parameters(self, country_code, section_number, land_number):
        """
        設定查詢參數。

        參數：
        - country_code: 縣市代碼
        - section_number: 地段代碼
        - land_number: 地號 (8位)
        """
        self.country_code = country_code
        self.section_number = section_number
        self.land_number = land_number
        self.url = f"https://api.nlsc.gov.tw/dmaps/CadasMapPosition/{self.country_code}/{self.section_number}/{self.land_number}"

    def fetch_position(self):
        """從 API 獲取地籍位置信息並解析 XML 響應。"""
        if not self.url:
            raise Exception("URL 未定義，請先設定查詢參數。")

        response = requests.get(self.url, headers=self.header)

        if response.status_code == 200:
            return self.parse_xml(response.text)
        else:
            raise Exception(f"獲取數據出錯：{response.status_code}")

    def parse_xml(self, xml_data):
        """解析 XML 數據並提取位置信息。"""
        try:
            root = ET.fromstring(xml_data)
            position = {
                '代表點X': root.find('.//repX').text,
                '代表點Y': root.find('.//repY').text,
                '左下X': root.find('.//ldX').text,
                '左下Y': root.find('.//ldY').text,
                '右上X': root.find('.//rtX').text,
                '右上Y': root.find('.//rtY').text
            }
            return position
        except ET.ParseError as e:
            raise Exception(f"解析 XML 出錯：{e}")


def main():
    # 使用示例：

    # 創建一個 CadasMapPosition 類的實例
    cad_map_position = CadasMapPosition()

    # 設定查詢參數
    cad_map_position.set_parameters('B', '0012', '00010000')

    # 獲取地籍位置數據
    position_data = cad_map_position.fetch_position()

    # 打印獲取到的位置數據
    print(position_data)


if __name__ == '__main__':
    main()
