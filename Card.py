class Card:
    def __init__(self, count: int, shape: str, shading: str, color: str, path: str):
        """class c'tor

        Args:
            count (int): shapes on the card
            shape (str): the shape
            shading (str): the shading
            color (str): shape's color
            path (str): path to card's image
        """

        self.count = count
        self.shape = shape
        self.shading = shading
        self.color = color
        self.path_2_image = path

    def __eq__(self, other):
        return self.count == other.count and self.shape == other.shape and \
               self.shading == other.shading and self.color == other.color and \
               self.path_2_image == other.path_2_image
