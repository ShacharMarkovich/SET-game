import requests

url = "https://www.setgame.com/sites/all/modules/setgame_set/assets/images/new/"


def download_all(path: str):
    """
    download the images and save them in the given `path`

    :param path: images directory
    """
    for i in range(1, 82):
        card = str(i) + ".png"
        res = requests.get(url + card)
        with open(path + '/' + card, 'wb') as f:
            for chunk in res.iter_content(1024):
                f.write(chunk)
