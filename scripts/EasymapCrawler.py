import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class EasymapCrawler:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 無頭模式（背景運行）
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = "https://easymap.land.moi.gov.tw/Z10Web/Normal"
        self.open_driver()

    def open_driver(self) -> None:
        self.driver.get(self.url)
        self.driver.maximize_window()
        self._click_tutorial_button()

    def _click_tutorial_button(self) -> None:
        begin_button = self.driver.find_element(By.XPATH, '//*[@id="guideModal"]/div/div/div[3]/button/span')
        time.sleep(3)
        try:
            begin_button.click()
        except ElementNotInteractableException:
            print("Begin button is not found or clicked")

    def select_city(self, city_name: str) -> None:
        """
        Select page's land city option
        :param city_name:
        :return:
        """
        self.driver.implicitly_wait(10)  # 最多等待10秒

        city_dropdown = self.driver.find_element(By.XPATH, '//*[@id="land_city_id"]')
        select = Select(city_dropdown)
        select.select_by_visible_text(city_name)  # 選擇指定的城市名

        selected_option = select.first_selected_option
        print(f"Selected city: {selected_option.text}")

        # 顯式等待鄉鎮下拉選單被更新，這裡我們等待 id 為 'land_town_id' 的元素出現
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="land_town_id"]/option[2]'))
            )
        except TimeoutException:
            print("Timed out waiting for township options to load")

    def select_township(self, township_name: str) -> None:
        self.driver.implicitly_wait(10)  # 最多等待10秒

        township_dropdown = self.driver.find_element(By.XPATH, '//*[@id="land_town_id"]')
        select = Select(township_dropdown)

        try:
            select.select_by_visible_text(township_name)  # 選擇指定的鄉鎮名
        except NoSuchElementException:
            print(f"Could not locate element with visible text: {township_name}")

        selected_option = select.first_selected_option
        print(f"Selected township: {selected_option.text}")

    def fill_section_number(self, section_number: str) -> None:
        """

        :param section_number: It must be like `0452` not `452`
        :return:
        """
        try:
            section_input_box = self.driver.find_element(By.XPATH, '//*[@id="land_section_text"]')
            section_input_box.clear()
            section_input_box.send_keys(section_number)

        except TimeoutException:
            print(f"Timed out waiting for the section input box to be clickable.")
        except ElementNotInteractableException:
            print(f"Element not interactable for section number: {section_number}")
        except NoSuchElementException:
            print(f"Could not locate section input box for number: {section_number}")

    def fill_land_number(self, land_number: str) -> None:
        try:
            land_input_box = self.driver.find_element(By.XPATH, '//*[@id="land_landno"]')
            land_input_box.clear()
            land_input_box.send_keys(land_number)

        except TimeoutException:
            print(f"Timed out waiting for the section input box to be clickable.")
        except ElementNotInteractableException:
            print(f"Element not interactable for section number: {land_number}")
        except NoSuchElementException:
            print(f"Could not locate section input box for number: {land_number}")

    def click_search_button(self) -> None:
        """
        Click search button to get result.
        :return:
        """
        try:
            search_button = self.driver.find_element(By.XPATH, '//*[@id="btn_land_search_id"]')
            search_button.click()
        except Exception as e:
            print(e)

    def get_land_number(self) -> str:
        """
        Get land number
        :return: land_number
        """
        land_number = self.driver.find_element(By.XPATH, '//*[@id="LANDtab"]/table/tbody/tr[4]/td')
        return land_number.text

    def run_process_flow_to_get_land_number(self, city_name: str, township_name: str, section_number: str,
                                            land_number: str) -> str:
        try:
            self.open_driver()
            self.select_city(city_name)
            self.select_township(township_name)
            self.fill_section_number(section_number)
            self.fill_land_number(land_number)
            self.click_search_button()
            return self.get_land_number()
        finally:
            self.close_driver()

    def close_driver(self) -> None:
        self.driver.quit()


def main() -> None:
    crawler = EasymapCrawler()

    try:
        city_name = "新竹縣"
        township_name = "竹北市"
        section_number = "0452"
        land_number = "905"

        land_number_found = crawler.run_process_flow_to_get_land_number(city_name, township_name, section_number,
                                                                        land_number)
        if land_number_found:
            print(f"Found land number: {land_number_found}")
        else:
            print("Could not find land number.")
    finally:
        crawler.close_driver()


if __name__ == '__main__':
    main()
