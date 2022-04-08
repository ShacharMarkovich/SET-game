import base64
import json
import os


def make():
    ImagesPath = "Cards\\Images\\"

    base64_all = {ImagesPath: {}, "icon.ico": None, "back.jpg": None}

    for img in os.listdir(ImagesPath):
        with open(ImagesPath + img, "rb") as f:
            data = f.read()
        base64_all[ImagesPath][img] = base64.b64encode(data).decode()

    with open("icon.ico", "rb") as f:
        data = f.read()
    base64_all["icon.ico"] = base64.b64encode(data).decode()

    with open("back.jpg", "rb") as f:
        data = f.read()
    base64_all["back.jpg"] = base64.b64encode(data).decode()

    with open("AllInBase64.json", 'w')as all_in_base64:
        all_in_base64.write(json.dumps(base64_all))


if __name__ == "__main__":
    make()
