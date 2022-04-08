import copy
import json
import os
import random
import threading
import tkinter as tk
from itertools import combinations
from tkinter import messagebox
from typing import List, Union

from PIL import Image, ImageTk

import Card
import CheckSet
from getCards.DownloadAll import download_all
from getCards.createJson import create


class SetGameHandler:
    ImagesPath = "Cards\\Images\\"
    JsonsPath = "Cards\\Jsons\\"
    PlaceHolder = "back.jpg"
    Amount = 81

    def __init__(self):
        self.check_data()

        self.window = tk.Tk()
        self.is_active = True

        self.all_cards = []
        self.available_cards = []
        self.board = []

        self.load_all_cards()

        self.selected_btn = []
        self.cards_amount = 12

    @staticmethod
    def check_data():
        """
        check if all description jsons and images are exists in the directory,
        if not - create them.
        TODO: if a specific card(s) is missing
        """
        if not os.path.exists(SetGameHandler.JsonsPath.split("\\")[0]):
            os.mkdir(SetGameHandler.JsonsPath.split("\\")[0])

        if not os.path.exists(SetGameHandler.JsonsPath):
            os.mkdir(SetGameHandler.JsonsPath)
            create(SetGameHandler.JsonsPath)

        if not os.path.exists(SetGameHandler.ImagesPath):
            os.mkdir(SetGameHandler.ImagesPath)
            download_all(SetGameHandler.ImagesPath)

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

    def get_k_random_cards(self, k: int = 3) -> Union[List[Card.Card], bool]:
        """
        get `k` cards from the deck.
        if deck is empty - return false.

        :param k: amount of cards
        :return: `k` random cards
        """
        if not len(self.available_cards):
            return False
        print("amount of available cards:", len(self.available_cards))
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
        if btn.cget('text') != SetGameHandler.PlaceHolder:
            if btn.cget('bg') == "green":
                btn.config(bg="black", highlightthickness=1)

                if btn in self.selected_btn:
                    self.selected_btn.remove(btn)
            else:
                self.selected_btn.append(btn)
                btn.config(bg="green", highlightthickness=2)

    def add_card(self, name: str, path: str, master: tk.Frame) -> tk.Button:
        """
        add the card to the `master` window

        :param name: the card's name
        :param path: path to the card picture
        :param master: current frame window
        :return: picture as button
        """
        i1 = ImageTk.PhotoImage(Image.open(path))
        im1 = tk.Button(name=name, text=path, master=master, image=i1, background="black")
        im1.config(command=lambda: self.change_bg(im1), highlightthickness=1)
        im1.image = i1
        return im1

    def help_me(self):
        """
        try to find a set.
        if there is a SET - show it to the player,
        else - show fit message.
        """
        # TODO: make it return the cards and how show them
        # get all cards and their button on the screen:
        board_cards = {}
        for i in range(3):
            for j in range(4):
                card_button = self.window.children[f"{i},{j}"].children[f"btn{i},{j}"]
                img = card_button.cget('text').split('\\')[-1]
                if img != SetGameHandler.PlaceHolder:
                    board_cards[img] = (card_button, [card for card in self.all_cards if card.path_2_image == img][0])

        # get all the subset of possible SETs from them:
        possible_sets = combinations(board_cards.keys(), 3)
        for possible_set in possible_sets:
            if CheckSet.check_set(board_cards[possible_set[0]][1],
                                  board_cards[possible_set[1]][1],
                                  board_cards[possible_set[2]][1]):
                board_cards[possible_set[0]][0].config(bg="blue", highlightthickness=2)
                board_cards[possible_set[1]][0].config(bg="blue", highlightthickness=2)
                board_cards[possible_set[2]][0].config(bg="blue", highlightthickness=2)
                return
        messagebox.showerror("Oops", "Sorry!\nThere is no set!\nPlease add 3 more cards!")

    def add_3_cards(self):
        if self.cards_amount == 15:
            messagebox.showerror("Oops", "Sorry!\nI cannot add more cards")
        else:
            k = 0
            new_cards = self.get_k_random_cards()
            if not new_cards:
                messagebox.showerror("Oops", "No more cards to add!")
            else:
                for frame_key in (k for k in self.window.children.keys() if ',' in k):
                    child_id = list(self.window.children[frame_key].children)[0]
                    if self.window.children[frame_key].children[child_id].cget('text') == self.PlaceHolder:
                        self.window.children[frame_key].children[child_id].destroy()

                        self.window.children[frame_key].grid(row=int(frame_key.split(',')[0]),
                                                             column=int(frame_key.split(',')[1]))
                        im = self.add_card(f"btn{frame_key}", SetGameHandler.ImagesPath + new_cards[k].path_2_image,
                                           self.window.children[frame_key])
                        im.pack(pady=5, padx=5)
                        self.board.append(new_cards[k])
                        k += 1
                self.cards_amount = 15

    def remove_3_cards(self):
        if self.cards_amount != 15:
            raise Exception("It should not have happened...")
        else:
            selected_cards = []
            for btn in self.selected_btn:
                selected_cards.append(
                    [c for c in self.all_cards if c.path_2_image == btn.cget('text').split('\\')[-1]][0])
            for i, btn in enumerate(self.selected_btn):
                new_im = ImageTk.PhotoImage(Image.open(SetGameHandler.PlaceHolder))
                btn.config(text=SetGameHandler.PlaceHolder, image=new_im)
                btn.image = new_im
                # update self.board
                self.board.remove(selected_cards[i])

    def load_gui_board(self):
        """
        load the board to the GUI window
        """
        # load the playing cards:
        k = 0
        for i in range(3):
            for j in range(4):
                frame = tk.Frame(name=f"{i},{j}", master=self.window, relief=tk.RAISED)
                frame.grid(row=i, column=j)
                im = self.add_card(f"btn{i},{j}", SetGameHandler.ImagesPath + self.board[k].path_2_image, frame)
                im.pack(pady=5, padx=5)
                k += 1
        self.cards_amount = 12

        for i in range(3):
            frame = tk.Frame(name=f"{i},4", master=self.window, relief=tk.RAISED)
            frame.grid(row=i, column=4)
            im = self.add_card(f"pH{i},4", SetGameHandler.PlaceHolder, frame)
            im.pack(pady=5, padx=5)

        # load the help-me button:
        frame = tk.Frame(name="help_frame", master=self.window, relief=tk.RAISED)
        frame.grid(row=0, column=5)  # column is five in order to  save place for more optional 3 cards
        help_btn = tk.Button(text="Find me a SET", master=frame, command=self.help_me)
        help_btn.pack(pady=5, padx=5)

        # load the add cards button:
        frame = tk.Frame(name="add_cards_frame", master=self.window, relief=tk.RAISED)
        frame.grid(row=1, column=5)  # column is five in order to  save place for more optional 3 cards
        help_btn = tk.Button(text="add 3 cards", master=frame, command=self.add_3_cards)
        help_btn.pack(pady=5, padx=5)

    def check_it(self):
        """
        get the player selected cards and check if they are a SET and play accordingly
        """
        while self.is_active:
            if len(self.selected_btn) == 3:  # must be 3 cards in order to ba a SET

                # get the selected cards objects:
                _cards = []
                for im in self.selected_btn:
                    _cards.append([c for c in self.all_cards if c.path_2_image == im.cget('text').split('\\')[-1]][0])
                # check if they are a SET:
                if CheckSet.check_set(_cards[0], _cards[1], _cards[2]):
                    # if yes - update the selected button to new cards
                    messagebox.showinfo("This is a SET!", "This is a SET!")
                    if self.cards_amount <= 12:
                        new_cards = self.get_k_random_cards()

                        if not new_cards:  # if the deck is empty - fill with the `PlaceHolder`
                            for i, btn in enumerate(self.selected_btn):
                                new_im = ImageTk.PhotoImage(Image.open(SetGameHandler.PlaceHolder))
                                btn.config(text=SetGameHandler.PlaceHolder, image=new_im)
                                btn.image = new_im
                                # update self.board
                                self.board.remove(_cards[i])
                        else:  # - add the new cards
                            for i, btn in enumerate(self.selected_btn):
                                path = SetGameHandler.ImagesPath + new_cards[i].path_2_image
                                new_im = ImageTk.PhotoImage(Image.open(path))
                                btn.config(text=path, image=new_im)
                                btn.image = new_im
                                # update self.board
                                self.board.remove(_cards[i])
                                self.board.append(new_cards[i])

                    else:
                        self.remove_3_cards()
                        self.cards_amount = 12

                else:
                    messagebox.showerror("Not a SET!", "Not a SET!")

                for btn in self.selected_btn:
                    btn.config(bg="black", highlightthickness=1)

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

        # TODO: add 3 cards only if checked that there is no more SETs
        # TODO: make an option to have more than 15 cards on the board
        # TODO: add an help option:
        #  when add 3 more cards tell the player that there is a set and give him an hint if he want
        #  a button that gives a hint
        #  - the hint is one card in another color
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    SetGameHandler().play()
