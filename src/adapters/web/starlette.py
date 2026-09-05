
class StarletteAdapter:

    def __init__(self, app, templates):
        self.app = app
        self.templates = templates

    def routes(self):
        return [
            ("/", None),
        ]
