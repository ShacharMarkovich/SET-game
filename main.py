import json
import copy
import os
import random
import threading
import tkinter as tk
from itertools import combinations
from time import sleep
from tkinter import messagebox, DISABLED, NORMAL
from tkinter.messagebox import askyesno
from typing import List, Union

from PIL import Image, ImageTk

import Card
import CheckSet
from getCards.createJson import create
from getCards.extractAllImages import extract_all_images


class SetGameHandler:
    ImagesPath = "Cards\\Images\\"
    JsonsPath = "Cards\\Jsons\\"
    PlaceHolder = "back.jpg"
    Icon = "icon.ico"
    Amount = 81

    def __init__(self):
        self.get_data()

        self.window = tk.Tk()
        self.window.resizable(width=False, height=False)
        self.window.iconbitmap(SetGameHandler.Icon)
        self.window.title("The SET Game - by Shachar Markovich")

        self.add_cards_state = None

        if not hasattr(self, 'th'):
            self.th = threading.Thread(target=self.check_it)
        self.is_active = True

        self.all_cards = []
        self.available_cards = []
        self.board = []
        self.start_over = False
        self.selected_btn = []
        self.cards_amount = 12

    @staticmethod
    def get_data():
        """
        check if all description jsons and images are exists in the directory,
        if not - create them.
        """

        # check if Cards dir exists:
        if not os.path.exists(SetGameHandler.JsonsPath.split("\\")[0]):
            os.mkdir(SetGameHandler.JsonsPath.split("\\")[0])

        # check if Cards/Jsons dir exists:
        if not os.path.exists(SetGameHandler.JsonsPath):
            os.mkdir(SetGameHandler.JsonsPath)
        if len(os.listdir(SetGameHandler.JsonsPath)) != SetGameHandler.Amount:
            create(SetGameHandler.JsonsPath)

        # check if Cards/Images dir exists:
        if not os.path.exists(SetGameHandler.ImagesPath):
            os.mkdir(SetGameHandler.ImagesPath)
        if len(os.listdir(SetGameHandler.ImagesPath)) != SetGameHandler.Amount:
            extract_all_images()

    def load_all_cards(self) -> None:
        """
        Load all the cards. each card is a `Card.Card` object.
        """
        files = [SetGameHandler.JsonsPath +
                 f for f in os.listdir(SetGameHandler.JsonsPath) if f.endswith(".json")]
        for file in files:
            with open(file, 'r') as fi:
                f_j = json.loads(fi.read().replace('\n', ''))
                card = Card.Card(f_j["count"], f_j["shape"],
                                 f_j["color"], f_j["shading"], f_j["image"])
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
                btn.config(bg="white", highlightthickness=3)

                if btn in self.selected_btn:
                    self.selected_btn.remove(btn)
            else:
                self.selected_btn.append(btn)
                btn.config(bg="green", highlightthickness=3)

    def add_card(self, name: str, path: str, master: tk.Frame) -> tk.Button:
        """
        add the card to the `master` window

        :param name: the card's name
        :param path: path to the card picture
        :param master: current frame window
        :return: picture as button
        """
        i1 = ImageTk.PhotoImage(Image.open(path))
        im1 = tk.Button(name=name, text=path, master=master,
                        image=i1, background="white")
        im1.config(command=lambda: self.change_bg(im1), highlightthickness=3)
        im1.image = i1
        return im1

    def help_me(self):
        """Show a possible SET on the board, if any"""
        ans = self.find_set()
        if ans:

            ans[0].config(bg="blue", highlightthickness=3)
            ans[1].config(bg="blue", highlightthickness=3)
            ans[2].config(bg="blue", highlightthickness=3)
        else:
            messagebox.showerror(
                "Oops", "Sorry!\nThere is no set!\nPlease add 3 more cards!")

    def find_set(self):
        """
        try to find a set.

        :returns: if there is a SET - return the buttons of the SET,    else - return False show fit message.
        """
        # get all cards and their button on the screen:
        board_cards = {}
        for i in range(3):
            for j in range(4):
                card_button = self.window.children[f"{
                    i},{j}"].children[f"btn{i},{j}"]
                img = card_button.cget('text').split('\\')[-1]
                if img != SetGameHandler.PlaceHolder:
                    board_cards[img] = (
                        card_button, [card for card in self.all_cards if card.path_2_image == img][0])

        # get all the subset of possible SETs from them:
        possible_sets = combinations(board_cards.keys(), 3)
        for possible_set in possible_sets:
            if CheckSet.check_set(board_cards[possible_set[0]][1],
                                  board_cards[possible_set[1]][1],
                                  board_cards[possible_set[2]][1]):
                return (board_cards[possible_set[0]][0],
                        board_cards[possible_set[1]][0],
                        board_cards[possible_set[2]][0])
        return False

    def add_3_cards(self):
        """Showes 3 more cards on the board
        """
        if self.cards_amount == 15:
            messagebox.showerror("Oops", "Sorry!\nI cannot add more cards")
        else:
            new_cards = self.get_k_random_cards()
            if not new_cards:
                messagebox.showerror("Oops", "No more cards to add!")
            else:
                # ask the user if he wants a hint instead of adding 3 cards, only when there is a SET
                a_set = self.find_set()
                if a_set:
                    if askyesno("Add 3 cards?", "there is at least one SET in the board!\nDo you want a hint?"):
                        a_set[0]['background'] = "dark green"
                        return

                # find the PlaceHolder cards and replace them with the new cards:
                k = 0
                for frame_key in (k for k in self.window.children.keys() if ',' in k):
                    child_id = list(self.window.children[frame_key].children)[0]
                    if self.window.children[frame_key].children[child_id].cget('text') == self.PlaceHolder:
                        self.window.children[frame_key].children[child_id].destroy()
                        self.window.children[frame_key].grid(row=int(frame_key.split(',')[0]),
                                                             column=int(frame_key.split(',')[1]))
                        im = self.add_card(f"btn{frame_key}", SetGameHandler.ImagesPath + new_cards[k].path_2_image, self.window.children[frame_key])
                        im.pack(pady=5, padx=5)
                        self.board.append(new_cards[k])
                        k += 1
                self.cards_amount = 15
            self.add_cards_state()

    def remove_3_cards(self):
        """remove the selected 3 cards from the board, show the PlaceHolder background instead"""
        if self.cards_amount != 15:
            raise Exception("It should not have happened...")
        else:
            selected_cards = []
            for btn in self.selected_btn:
                selected_cards.append(
                    [c for c in self.all_cards if c.path_2_image == btn.cget('text').split('\\')[-1]][0])
            for i, btn in enumerate(self.selected_btn):
                new_im = ImageTk.PhotoImage(
                    Image.open(SetGameHandler.PlaceHolder))
                btn.config(text=SetGameHandler.PlaceHolder, image=new_im)
                btn.image = new_im
                self.board.remove(selected_cards[i])

            self.add_cards_state()

    def load_gui_board(self):
        """
        load the board to the GUI window
        """
        # load the playing cards:
        k = 0
        for i in range(3):
            for j in range(4):
                frame = tk.Frame(
                    name=f"{i},{j}", master=self.window, relief=tk.RAISED)
                frame.grid(row=i, column=j)
                im = self.add_card(
                    f"btn{i},{j}", SetGameHandler.ImagesPath + self.board[k].path_2_image, frame)
                im.pack(pady=5, padx=5)
                k += 1
        self.cards_amount = 12

        for i in range(3):
            frame = tk.Frame(
                name=f"{i},4", master=self.window, relief=tk.RAISED)
            frame.grid(row=i, column=4)
            im = self.add_card(f"pH{i},4", SetGameHandler.PlaceHolder, frame)
            im.pack(pady=5, padx=5)

        # load the help-me button:
        frame = tk.Frame(name="help_frame",
                         master=self.window, relief=tk.RAISED)
        # column is five in order to  save place for more optional 3 cards
        frame.grid(row=0, column=5)
        help_btn = tk.Button(text="Find me a SET",
                             master=frame, command=self.help_me)
        help_btn.pack(pady=5, padx=5)

        # load the add cards button:
        frame = tk.Frame(name="add_cards_frame",
                         master=self.window, relief=tk.RAISED)
        # column is five in order to  save place for more optional 3 cards
        frame.grid(row=1, column=5)
        add_cards_btn = tk.Button(
            text="add 3 cards", master=frame, command=self.add_3_cards)
        self.add_cards_state = lambda: self.__change_state(add_cards_btn)
        add_cards_btn.pack(pady=5, padx=5)

    @staticmethod
    def __change_state(btn):
        btn['state'] = NORMAL if btn['state'] == DISABLED else DISABLED

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
                    self.flash_color(self.selected_btn, "#00ff00")
                    sleep(1.5)
                    if self.cards_amount <= 12:
                        new_cards = self.get_k_random_cards()

                        if not new_cards:  # if the deck is empty - fill with the `PlaceHolder`
                            for i, btn in enumerate(self.selected_btn):
                                new_im = ImageTk.PhotoImage(
                                    Image.open(SetGameHandler.PlaceHolder))
                                btn.config(
                                    text=SetGameHandler.PlaceHolder, image=new_im)
                                btn.image = new_im
                                # update self.board
                                self.board.remove(_cards[i])

                            if not self.find_set():
                                messagebox.showinfo("Game Over",
                                                    "The game is finished, no more cards and no more SETs!")
                                self.on_closing()

                        else:  # - add the new cards
                            for i, btn in enumerate(self.selected_btn):
                                path = SetGameHandler.ImagesPath + \
                                    new_cards[i].path_2_image
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
                    self.flash_color(self.selected_btn, "#ff4040")
                    sleep(1.5)

                for btn in self.selected_btn:
                    btn.config(bg="white", highlightthickness=3)

                self.selected_btn = []

    def flash_color(self, btns, color):
        for btn in btns:
            btn.config(background=color)

        def __flash_color(btns, count):
            if count < 6:
                for btn in btns:
                    current_color = btn.cget("background")
                    next_color = color if current_color == "white" else "white"
                    btn.config(background=next_color)
                count += 1
                self.window.after(100 if count < 6 else 1500,
                                  __flash_color, btns, count)

        times = 0
        __flash_color(btns, times)

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
        self.load_all_cards()
        self.board = self.get_board()
        self.load_gui_board()
        self.th.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()


if __name__ == "__main__":
    SetGameHandler().play()
