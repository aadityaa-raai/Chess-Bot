♟️ Chess Bot with GUI
An automated chess bot that plays on Chess.com using Stockfish, Selenium, and PyAutoGUI. This bot detects opponent moves from the Chess.com board and plays the best move using Stockfish.

📦 Features
GUI control panel using Tkinter
Automatically opens Chess.com vs Computer
Reads the opponent's move via DOM scraping
Uses Stockfish to compute the best move
Moves pieces using PyAutoGUI
Threaded execution for responsive GUI

🛠 Requirements
Install all required libraries using:

bash
pip install -r req.txt
Dependencies in req.txt:

stockfish
selenium
pyautogui
opencv-python
python-chess

🚀 How to Run
Download:
Stockfish engine
ChromeDriver
Update the following paths in bot_gui.py:

stockfish_path=r"YOUR_STOCKFISH_PATH"
chromedriver_path=r"YOUR_CHROMEDRIVER_PATH"
Run the GUI:

bash
python bot_gui.py
🧠 How It Works
GUI (bot_gui.py):

Provides buttons to open Chess.com, start the bot, and stop/reset it.

Displays the current best move being calculated.

Bot Logic (chess_bot.py):

Opens browser via Selenium

Parses board state using python-chess

Converts algebraic moves to UCI

Uses Stockfish to calculate best move

Simulates mouse movements to make moves on Chess.com

🖼 UI Preview
pgsql
Copy
Edit
+--------------------------+
| [Open Chess.com]        |
| [Start Bot]             |
| [Stop]                  |
| Best Move: e2e4         |
+--------------------------+
⚠️ Notes
Works only with the default theme and layout of Chess.com.
Calibrate x_axis, y_axis, and sq_size in chess_bot.py if your screen resolution or zoom is different.
Do not interact with the board manually while the bot is running.

📁 Project Structure
bash
Copy
Edit
├── bot_gui.py       # GUI logic
├── chess_bot.py     # Core bot implementation
├── req.txt          # Required Python packages
🙏 Credits
Stockfish

python-chess

Selenium

PyAutoGUI

