import copy
import os
import random
import threading
from tkinter import messagebox

import Card
from PIL import Image, ImageTk
import json
import CheckSet
import tkinter as tk

selected_btn = []
all_cards = []


def load_all_cards() -> list[Card.Card]:
    """
    Load all the cards. each card is a `Card.Card` object.

    :return: list of all cards
    """
    files = ["Cards\\Jsons\\" + f for f in os.listdir("Cards\\Jsons") if f.endswith(".json")]
    for file in files:
        with open(file, 'r') as fi:
            f_j = json.loads(fi.read().replace('\n', ''))
            card = Card.Card(f_j["count"], f_j["shape"], f_j["color"], f_j["shading"], f_j["image"])
            all_cards.append(card)
    return [copy.deepcopy(c) for c in all_cards]


def get_board() -> tuple[list[Card], list[Card]]:
    """
    load all cards and return the first game board
    """
    cards = load_all_cards()
    selected_cards = random.sample(cards, k=12)
    for card in selected_cards:
        cards.remove(card)

    return cards, selected_cards


def change_bg(btn):
    if btn.cget('bg') == "red":
        btn.config(bg="black")
        if btn.cget('text') in selected_btn:
            selected_btn.remove(btn.cget('text'))
    else:
        selected_btn.append(btn.cget('text').split('\\')[-1])
        btn.config(bg="red")


def add_card(path: str, master: tk.Frame) -> tk.Button:
    """
    add the card to the `master` window

    :param path: path to the card picture
    :param master: current frame window
    :return: picture as button
    """
    i1 = ImageTk.PhotoImage(Image.open(path))
    print(path)
    print(path.split('\\')[-1].split('.')[0])
    im1 = tk.Button(text=path, master=master, image=i1, background="black")
    im1.config(command=lambda: change_bg(im1))
    im1.image = i1
    return im1


def load_board(window, board: list[Card.Card]):
    """
    load the board to the window

    :param window: the main window
    :param board: the cards
    """
    k = 0
    for i in range(3):
        for j in range(4):
            frame = tk.Frame(master=window, relief=tk.RAISED)
            frame.grid(row=i, column=j)
            im = add_card("Cards\\Images\\" + board[k].path_2_image, frame)
            im.pack(pady=5, padx=5)
            k += 1


def sub3_lists(lst: list) -> list[list]:
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


def check_it():
    global selected_btn
    while True:
        if len(selected_btn) == 3:
            _cards = []
            for im in selected_btn:
                _cards.append([c for c in all_cards if c.path_2_image == im][0])
            if CheckSet.check_set(_cards[0], _cards[1], _cards[2]):
                messagebox.showinfo("This is a SET!", "This is a SET!")
            else:
                messagebox.showerror("Not a SET!", "Not a SET!")
            selected_btn = []


def main():
    rest_cards, board = get_board()
    window = tk.Tk()

    load_board(window, board)

    # TODO: add a thread which when 3 buttons are selected - check if they are a SET
    th = threading.Thread(target=check_it)
    th.start()
    # TODO:     if yes - remove those cards and load new once (maybe show  a fit msg)
    # TODO:     else - clear the selected list (maybe show  a fit msg)

    # TODO: bot to solve the game

    window.mainloop()


if __name__ == "__main__":
    main()
