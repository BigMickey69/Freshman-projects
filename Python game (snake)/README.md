# Python game
這是一個使用 Python 和 Pygame 實現蟒蛇吃貧果的遊戲。目標是通過控制蛇的移動來吃掉蘋果，並讓蛇的長度逐漸增加並求生存。

aka就是貪食蛇，
因Python這個英文單字其實是「蟒蛇」
所以將這遊戲命名為Python (自己覺得很幽默)

## Extra Features:
    Python has very cute eyes
    more and more apples spawn as the game goes on!
    added a grace period when touching walls, preventing instant death


## 專案結構

- **main.py**：主要程式區，負責遊戲邏輯和界面顯示。
- **assets**：包含遊戲所需的圖片資源

## 遊戲功能

- **控制蛇的移動**：使用 W、A、S、D 鍵來控制蛇的方向。
- **吃蘋果**：當蛇吃到蘋果時，得分增加，蛇的長度增加。
- **顯示得分**：實時顯示當前得分。
- **遊戲結束判斷**：當蛇碰到自己或邊界時，遊戲結束並顯示輸的畫面。

### 依賴項
- pygame
