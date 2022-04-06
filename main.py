import copy
import json
import os
import random
import threading
import tkinter as tk
from tkinter import messagebox
from typing import List

from PIL import Image, ImageTk

import Card
import CheckSet


class SetGameHandler:
    ImagesPath = "Cards\\Images\\"
    JsonsPath = "Cards\\Jsons\\"

    def __init__(self):
        self.window = tk.Tk()
        self.is_active = True

        self.all_cards = []
        self.available_cards = []
        self.load_all_cards()

        self.rest_cards = []

        self.selected_btn = []

    def load_all_cards(self) -> None:
        """
        Load all the cards. each card is a `Card.Card` object.
        """
        files = [SetGameHandler.JsonsPath + f for f in os.listdir(SetGameHandler.JsonsPath) if f.endswith(".json")]
        for file in files:
            with open(file, 'r') as fi:
                f_j = json.loads(fi.read().replace('\n', ''))
                card = Card.Card(f_j["count"], f_j["shape"], f_j["color"], f_j["shading"], f_j["image"])
                self.all_cards.append(card)
        self.available_cards = [copy.deepcopy(c) for c in self.all_cards]

    def get_k_random_cards(self, k: int = 3) -> List[Card.Card]:
        """
        get `k` cards from the deck.

        :param k: amount of cards
        :return: `k` random cards
        """
        selected = random.sample(self.available_cards, k)
        for card in selected:
            self.available_cards.remove(card)
        return selected

    def get_board(self) -> List[Card.Card]:
        """
        load all cards and return the first game board

        :return: the initiate game board
        """
        return self.get_k_random_cards(12)

    def change_bg(self, btn):
        if btn.cget('bg') == "red":
            btn.config(bg="black")
            if btn in self.selected_btn:
                self.selected_btn.remove(btn)
        else:
            self.selected_btn.append(btn)  # .cget('text').split('\\')[-1]
            btn.config(bg="red")

    def add_card(self, path: str, master: tk.Frame) -> tk.Button:
        """
        add the card to the `master` window

        :param path: path to the card picture
        :param master: current frame window
        :return: picture as button
        """
        i1 = ImageTk.PhotoImage(Image.open(path))
        im1 = tk.Button(text=path, master=master, image=i1, background="black")
        im1.config(command=lambda: self.change_bg(im1))
        im1.image = i1
        return im1

    def load_gui_board(self, board: List[Card.Card]):
        """
        load the board to the window

        :param board: the cards
        """
        k = 0
        for i in range(3):
            for j in range(4):
                frame = tk.Frame(master=self.window, relief=tk.RAISED)
                frame.grid(row=i, column=j)
                im = self.add_card(SetGameHandler.ImagesPath + board[k].path_2_image, frame)
                im.pack(pady=5, padx=5)
                k += 1

    @staticmethod
    def sub3_lists(lst: list) -> List[list]:
        """
        get all `lst`'s sub-lists in length of 3

        :param lst: the list
        :return: all the sub-lists in length of 3
        """
        lists = []
        for i in range(len(lst) + 1):
            for j in range(i):
                sl = lst[j: i]
                if len(sl) == 3:
                    lists.append(sl)
        return lists

    def check_it(self):
        while self.is_active:
            if len(self.selected_btn) == 3:
                _cards = []
                for im in self.selected_btn:
                    _cards.append([c for c in self.all_cards if c.path_2_image == im.cget('text').split('\\')[-1]][0])
                if CheckSet.check_set(_cards[0], _cards[1], _cards[2]):
                    messagebox.showinfo("This is a SET!", "This is a SET!")
                    # TODO: replace those cards
                    new_cards = self.get_k_random_cards()
                    for i, btn in enumerate(self.selected_btn):
                        path = SetGameHandler.ImagesPath + new_cards[i].path_2_image
                        new_im = ImageTk.PhotoImage(Image.open(path))
                        btn.config(text=path, image=new_im)
                        btn.image = new_im
                else:
                    messagebox.showerror("Not a SET!", "Not a SET!")

                for btn in self.selected_btn:
                    btn.config(bg="black")

                self.selected_btn = []

    def on_closing(self):
        self.is_active = False
        self.window.destroy()

    def main(self):
        board = self.get_board()

        self.load_gui_board(board)

        # TODO: add a thread which when 3 buttons are selected - check if they are a SET
        th = threading.Thread(target=self.check_it)
        th.start()
        # TODO:     if yes - remove those cards and load new once (maybe show  a fit msg)
        # TODO:     else - clear the selected list (maybe show  a fit msg)

        # TODO: bot to solve the game
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    SetGameHandler().main()
