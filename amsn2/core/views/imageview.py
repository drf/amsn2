class ImageView(object):
    class ResourceType:
        UNKNOWN = "unknown" #Should not be used
        FILE = "File"
        SKIN = "Skin"

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
