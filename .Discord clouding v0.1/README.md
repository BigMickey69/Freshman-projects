# 利用 Discord 訊息中附檔不會過期這個特點來造就無限雲端空間

本專案利用 Discord 訊息中附檔不會過期的特點，實現了一個無限雲端空間的解決方案。通過將文件分割為多個塊上傳至 Discord 頻道，並在需要時重新組裝下載，可以有效地存儲和管理大量文件。

預計伺服器從今天算起 2024/7/15 開到暑假結束，
有請幾位朋友測試，說明使用方法後都有使用有成功使用

## 專案結構

- **Bot/main.py**：Discord Bot主程序，負責文件的上傳、下載、與 Discord 伺服器的交互，也有使用Flask來與網站端溝通。
- **Bot/convert_to_chunks.py**：將檔案分割為~25MB大小之chunks
- **Bot/chunks_to_file.py**：將檔案分割的chunks轉回原文件
- **Bot/responses.py**：處理Discord頻道上與Jose講話時的回應

- **Website/main.py**：網站主程序，提供用戶界面進行文件上傳和管理。
- **Website/website/\_\_init\_\_.py**：Flask 應用的初始化，包括數據庫設置和清理機制。
- **Website/website/auth.py**：處理用戶認證和授權。
- **Website/website/models.py**：數據庫模型定義，包括用戶、文件等。
- **Website/website/cleanup.py**：定期清理下載文件的機制。
- **Website/website/views.py**：定義各種視圖函數，處理用戶請求和界面顯示。


## 網站測試

網站架在：http://discordclouding.asuscomm.com:1212/

使用說明：http://discordclouding.asuscomm.com:1212/how-to-use

若想測試但不想註冊，歡迎使用測試帳號 → 
    email = Test@gmail.com
    password = 0000

若想看背後的Discord 頻道 → 加入連結：https://discord.gg/fTpNeF4UAd


細說原理：http://discordclouding.asuscomm.com:1212/logic

關於我：http://discordclouding.asuscomm.com:1212/about-me



## 安裝與運行

### 依賴項
- Flask
- SQLAlchemy
- Flask-Login
- Discord.py
- requests
- aiofiles
- python-dotenv

若想自己執行看看：
    到Discord Developer Portal申請一個Discord bot
    設定機器人權限與各種設定
    將機器人的Token丟到.env檔之中
    創建一個Discord伺服器
    將機器人邀請到伺服器中

    開兩個VScode或pycharm等IDE
    一個開啟母資料夾，打開Bot中的main.py
    另一個開啟子資料夾Website，打開裡面main.py

    創建幾個頻道
    複製要用的頻道ID
    到對應的.py檔中將頻道ID改為自己的ID
    執行兩VScode中的　main.py　即可使用！
    （不含port-fowarding）






