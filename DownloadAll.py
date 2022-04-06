import requests

url = "https://www.setgame.com/sites/all/modules/setgame_set/assets/images/new/"


def download_all():
    for i in range(1, 82):
        card = str(i) + ".png"
        res = requests.get(url + card)
        print(f"[!] got {card}!")
        with open(card, 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)
        print(f"[!] save {card}!")


if __name__ == "__main__":
    # download_all()
    pass