# chess_bot_gui.py

import tkinter as tk
import threading
from chess_bot import ChessBot
import time
# Create App window
app = tk.Tk()
app.title("ChessBot GUI")
app.attributes("-topmost", True)

# Initialize ChessBot instance
bot = ChessBot(
    stockfish_path=r"C:\Users\KIIT\Downloads\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe",
    chromedriver_path=r"C:\Users\KIIT\Downloads\chromedriver-win64\chromedriver.exe"
)

move=""

def open_browser():
    threading.Thread(target=bot.open_chess_com).start()

def start_bot():
    thrd.start_recent_move_thread()

def clear():
    thrd.stop_thread()
    print("Chck Before:",bot.check)
    print("Thread Before:",thrd.recent_move_thread.is_alive())
    bot.reset()
    print("lst:",bot.lst)
    print("Chck:",bot.check)
    thrd.recent_move_thread.join()
    print("Thread:",thrd.recent_move_thread.is_alive())
    print()

def best_move_txt():
    while True:
        move_label.config(text=f"Best Move: {bot.str}")
        move_label.pack(pady=10)
        time.sleep(0.8)

class threads():
    
    def __init__(self):
        self.stop_event=threading.Event()
        self.recent_move_thread = threading.Thread(target=bot.recent_move)
        self.recent_move_thread.daemon = True
        self.check=self.recent_move_thread.is_alive()

    def start_recent_move_thread(self):
        if self.check==True:
            print("Thread can only be started once!!")
        else:
            # self.stop_event.clear()
            # self.recent_move_thread=threading.Thread(target=bot.recent_move,args=(self.stop_event,))
            self.recent_move_thread.start()
            txt_thread=threading.Thread(target=best_move_txt)
            txt_thread.daemon=True
            txt_thread.start()
            print("Recent move detection thread started.")
    
    def start_thread(self):
        if self.recent_move_thread and self.recent_move_thread.is_alive():
            print("Thread is already running.")
            return

        # Clear any previous stop signal
        self.stop_event.clear()

        # Create a new thread
        self.recent_move_thread = threading.Thread(target=bot.recent_move, args=(self.stop_event,))
        self.recent_move_thread.daemon = True
        self.recent_move_thread.start()
        print("Thread started.")

    def stop_thread(self):
        if self.recent_move_thread and self.recent_move_thread.is_alive():
            self.stop_event.set()
            self.recent_move_thread.join()
            print("Thread stopped.")
        else:
            print("No thread running.")

    def is_running(self):
        return self.recent_move_thread and self.recent_move_thread.is_alive()

thrd=threads()
            
# Buttons in the GUI
open_button = tk.Button(app, text="Open Chess.com", command=open_browser, height=2, width=20)
open_button.pack(pady=10)

recent_move_button = tk.Button(app, text="Start Bot", command=thrd.start_recent_move_thread, height=2, width=20)
recent_move_button.pack(pady=10)

stop_button = tk.Button(app, text="Stop ", command=clear, height=2, width=20)
stop_button.pack(pady=10)

move_label = tk.Label(app, text="Best Move: ", font=("Arial", 16))
move_label.pack(pady=10)


app.geometry("300x400")
app.mainloop()
