# 地籍資料處理器

本項目用於處理包含地籍資訊的 CSV 檔案，通過網路爬蟲和 API 請求獲取農地經緯度的資料，並將更新後的資料輸出到新的 CSV 檔案中。

## 專案結構

- `main.py`：主要程式
- `CSVProcessor.py`：處理 CSV 檔案的讀取、處理和儲存。
- `EasyMapCrawler.py`：使用 Selenium 抓取地號資料。
- `CadasMapPosition.py`：使用 API 獲取六個坐標點資料。
- `opendata/`：儲存輸入公開資料 CSV 檔案的資料夾。
- `output/`：儲存處理後 CSV 檔案的資料夾。

## 使用說明

1. **環境設置**

   ```sh
   pip install requirements.txt
   ```

2. **準備 CSV 檔案**

   1. 在專案最外層新增 `opendata` 的資料夾。

      - 在 `opendata` 資料夾中新增 `lands` 及 `towncode` 資料夾。

   2. 請至 [不動產成交案件](https://plvr.land.moi.gov.tw/Index) 選取 CSV 格式的全國資料
      並下載。
      - 將「不動產成交案件」CSV 檔案解壓縮至 `opendata/lands` 中。

   3. 請至 [土地段名代碼暨詮釋資料查詢系統](https://lisp.land.moi.gov.tw/MMS/MMSpage.aspx#gobox02)選取全國並下載。
      - 將「土地段名代碼暨詮釋資料查詢系統」CSV 檔案解壓縮至 `opendata/towncode` 中。

3. **申請 API 使用資格**

   這個專案使用到 [國土測繪圖資服務雲](https://maps.nlsc.gov.tw/) 的 CAD-001 之 API。
   -  請參考 [國土測繪圖資服務雲申請文件](https://maps.nlsc.gov.tw/S09SOA/homePage.action?Language=ZH) 並完成申請。

4. **運行程式**

   cd 到本專案資料夾中並執行 `main.py`

    ```shell
    python main.py
    ```

程式將自動處理 `opendata/lands` 目錄中所有符合規則的 CSV 檔案，並將處理結果保存到 output 資料夾中。
