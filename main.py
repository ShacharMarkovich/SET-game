import copy
import json
import os
import random
import threading
import tkinter as tk
from itertools import combinations
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
        self.board = []
        self.load_all_cards()

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
        """
        change the given button background color.

        :param btn: btn to change it background color
        """
        if btn.cget('bg') == "red":
            btn.config(bg="black")

            if btn in self.selected_btn:
                self.selected_btn.remove(btn)
        else:
            self.selected_btn.append(btn)
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

    @staticmethod
    def sub3_lists(my_list):
        return combinations(my_list, 3)

    def help_me(self):
        # get all cards and their button on the screen:
        board_cards = {}
        for i in range(3):
            for j in range(4):
                card_button = self.window.children['main_frame'].children[f"{i},{j}"].children['!button']
                img = card_button.cget('text').split('\\')[-1]
                board_cards[img] = (card_button, [card for card in self.all_cards if card.path_2_image == img][0])

        # get all the subset of possible SETs from them:
        possible_sets = combinations(board_cards.keys(), 3)
        for possible_set in possible_sets:
            if CheckSet.check_set(board_cards[possible_set[0]][1],
                                  board_cards[possible_set[1]][1],
                                  board_cards[possible_set[2]][1]):
                board_cards[possible_set[0]][0].config(bg="blue")
                board_cards[possible_set[1]][0].config(bg="blue")
                board_cards[possible_set[2]][0].config(bg="blue")
                return
        messagebox.showerror("Oops", "Sorry!\nThere is no set!\nPlease add 3 more cards!")

    def load_gui_board(self):
        """
        load the board to the GUI window
        """
        # load the playing cards:
        k = 0
        main_frame = tk.Frame(name="main_frame", master=self.window, relief=tk.RAISED)
        main_frame.grid(column=0)
        for i in range(3):
            for j in range(4):
                frame = tk.Frame(name=f"{i},{j}", master=main_frame, relief=tk.RAISED)
                frame.grid(row=i, column=j)
                im = self.add_card(SetGameHandler.ImagesPath + self.board[k].path_2_image, frame)
                im.pack(pady=5, padx=5)
                k += 1

        # load the help-me button:
        frame = tk.Frame(name="help_frame", master=main_frame, relief=tk.RAISED)
        frame.grid(row=0, column=4)
        help_btn = tk.Button(text="Find me a SET", master=frame, command=self.help_me)
        help_btn.pack(pady=5, padx=5)

        # load the add cards button:
        frame = tk.Frame(name="add_cards_frame", master=main_frame, relief=tk.RAISED)
        frame.grid(row=1, column=4)
        help_btn = tk.Button(text="add 3 cards", master=frame,
                             command=lambda: messagebox.showerror("Oops",
                                                                  "Sorry!\nThere is still no implement for this!"))
        help_btn.pack(pady=5, padx=5)

    def check_it(self):
        """
        get the player selected cards and check if they are a SET and play accordingly
        """
        while self.is_active:
            if len(self.selected_btn) == 3:  # must be 3 cards in order to ba a SET
                # get the selected cards objects and check if they are a SET:
                _cards = []
                for im in self.selected_btn:
                    _cards.append([c for c in self.all_cards if c.path_2_image == im.cget('text').split('\\')[-1]][0])
                if CheckSet.check_set(_cards[0], _cards[1], _cards[2]):
                    # if yes - update the selected button to new cards
                    messagebox.showinfo("This is a SET!", "This is a SET!")
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
        """
        change the main window status to inactive and close it.
        """
        self.is_active = False
        self.window.destroy()

    def play(self):
        """
        Play the SET game
        """
        self.board = self.get_board()

        self.load_gui_board()

        th = threading.Thread(target=self.check_it)
        th.start()

        # TODO: add 3 cards when there is no set
        # TODO: handle when the deck is finished
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    SetGameHandler().play()
