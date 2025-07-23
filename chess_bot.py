# chess_bot.py
import chess
import threading
from stockfish import Stockfish
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pyautogui as pag

def algebraic_to_uci(board, move_san):
    try:
        if '+' in move_san:
            move_san=move_san[:-1]
        move = board.parse_san(move_san)
        return move.uci()
    except ValueError as e:
        return None

class ChessBot:
    
    def __init__(self, stockfish_path, chromedriver_path):
        self.STOCKFISH_PATH = stockfish_path
        self.CHROMEDRIVER_PATH = chromedriver_path
        self.stockfish = Stockfish(path=self.STOCKFISH_PATH)
        self.stockfish.set_position([])
        self.driver = None
        self.board=chess.Board()
        self.lst=list()
        self.check=False
        self.str="e2e4"
        self.int=0
        self.x_axis=340
        self.y_axis=875
        self.sq_size=80
        self.x=0
        self.y=0
        self.stockfish.set_skill_level(20)
    

    def reset(self):
        self.board=chess.Board()
        self.lst=[]
        self.check=False


    def open_chess_com(self):
        service = Service(self.CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get("https://www.chess.com/play/computer")
        print("Chess.com opened!")

    def stop_bot(self):
        self.int=0

    

    def print(self):
        print(self.lst)

    def square_to_chesscom_number(self,square):
        files = 'abcdefgh'
        file = files.index(square[0]) + 1  
        rank = int(square[1])
        return (file*10)+rank


    def x_conv(self,x):
        return self.x_axis+(x)*self.sq_size

    def y_conv(self,y):
        return self.y_axis-(y)*self.sq_size

    def make_move(self):
        try:
            if not self.driver:
                print("Browser not open.")
                return

            str=self.str

            from_x=ord(str[0])-ord('a')
            from_y=ord(str[1])-ord('1')
            to_x=ord(str[2])-ord('a')
            to_y=ord(str[3])-ord('1')
            
            from_x,to_x=self.x_conv(from_x),self.x_conv(to_x)
            from_y,to_y=self.y_conv(from_y),self.y_conv(to_y)
            self.x,self.y=from_x,from_y
            pag.moveTo(from_x,from_y,duration=0)
            pag.click()
            time.sleep(0.1)
            pag.moveTo(to_x,to_y,duration=0)
            pag.click()

        except Exception as e:
            print(f"Error performing move {self.str}: {e}")


    def get_best_move(self):
        try:
            self.int=1
        # Set Stockfish's position using UCI moves so far
            self.stockfish.set_position(self.lst)

        # Get the best move in UCI format
            best_move = self.stockfish.get_best_move()

            if best_move:
                print(f"Best move suggested by Stockfish: {best_move}")
                self.str=best_move
                return
            else:
                print("Stockfish couldn't find a best move.")
                return

        except Exception as e:
            print(f"Error getting best move: {e}")
            return

    def rec_move(self):
        move_elements = self.driver.find_elements(By.CLASS_NAME, 'node.main-line-ply')
        new_board=self.board.copy()
        last_move=move_elements[-1].text
        uci_move=algebraic_to_uci(new_board,last_move)
        print("Last Move:", move_elements[-1].text)
        print("Alg to uci:",algebraic_to_uci(new_board,move_elements[-1].text))
        print("\n|||||||||||||||||||||||")

    def recent_move(self):
        self.check=True
        flag=True
        last_move_count=0
        while self.check:
            
            if not self.driver:
                print("Browser not open.")
                return
            move_elements = self.driver.find_elements(By.CLASS_NAME, 'node.main-line-ply')

            if move_elements:
                try:
                    curr_move_count=len(move_elements)
                    last_move = move_elements[-1].text
                    
                    uci_move=algebraic_to_uci(self.board,last_move)
                    if (len(self.lst)==0 or self.lst[-1]!=uci_move) and uci_move!=None and last_move_count<curr_move_count:
                        last_move_count=curr_move_count
                        self.lst.append(uci_move)
                        move = chess.Move.from_uci(uci_move)
                        self.board.push(move)
                        print("Recent Move:", self.lst[-1],"\tMove:",self.lst)
                        self.get_best_move()
                        self.make_move()
                        print("Best Move:",self.str)
                        print(f"x,y= {self.x},{self.y}")

                except Exception as e:
                    print("Error fetching recent move:", e)
            
            elif flag:
                flag=False
                self.get_best_move()
                self.make_move()

                    
            time.sleep(0.2)