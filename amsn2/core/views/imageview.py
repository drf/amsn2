class ImageView(object):
    """
        Known resource_type are:
            - Filename
            - Theme
            - None
    """

    FILENAME = "Filename"
    THEME = "Theme"

    def __init__(self, resource_type=None, value=None):
        self.imgs = []
        if resource_type is not None and value is not None:
            self.load(resource_type, value)

    def load(self, resource_type, value):
        self.imgs = [(resource_type, value)]

    def append(self, resource_type, value):
        self.imgs.append((resource_type, value))

    def prepend(self, resource_type, value):
        self.imgs.insert(0, (resource_type, value))

    def clone(self):
        img = ImageView()
        img.imgs = self.imgs[:]
        return img

    def appendImageView(self, iv):
        self.imgs.extend(iv.imgs)

    def prependImageView(self, iv):
        self.imgs = iv.imgs[:].extend(self.imgs)

    def reset(self):
        self.imgs = []

