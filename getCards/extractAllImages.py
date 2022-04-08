import base64

from bata_base64 import base64_all


def extract_all_images():
    """
    download the images and save them in the given `path`
    """
    ImagesPath = "Cards\\Images\\"
    PlaceHolder = "back.jpg"
    Icon = "icon.ico"
    
    for img_name, img_b64 in base64_all[ImagesPath].items():
        with open(ImagesPath + img_name, 'wb') as img_f:
            img_f.write(base64.b64decode(img_b64.encode()))

    with open(Icon, 'wb') as img_f:
        img_f.write(base64.b64decode(base64_all[Icon].encode()))

    with open(PlaceHolder, 'wb') as img_f:
        img_f.write(base64.b64decode(base64_all[PlaceHolder].encode()))
