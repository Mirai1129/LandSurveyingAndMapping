import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()
driver.get("https://easymap.land.moi.gov.tw/Z10Web/Normal")

driver.implicitly_wait(10)  # 最多等待10秒
driver.maximize_window()

begin_button = driver.find_element(By.XPATH, '//*[@id="guideModal"]/div/div/div[3]/button/span')
time.sleep(5)
begin_button.click()

city_dropdown = driver.find_element(By.XPATH, '//*[@id="land_city_id"]')
select = Select(city_dropdown)
select.select_by_visible_text("新竹縣")  # 選擇指定的城市名

township_dropdown = driver.find_element(By.XPATH, '//*[@id="land_town_id"]')
select = Select(township_dropdown)
select.select_by_visible_text("竹北市")  # 選擇指定的城市名

land_input_box = driver.find_element(By.XPATH, '//*[@id="land_section_text"]')
# land_input_box.click()
land_input_box.send_keys("0452")

time.sleep(20)
