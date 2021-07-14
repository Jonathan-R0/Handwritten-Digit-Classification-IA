class Pencil:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.r = 8

    def update(self, event):
        self.x = event.x
        self.y = event.y

    def draw(self, drawer):
        drawer(self.x - self.r, self.y - self.r, self.x +
               self.r, self.y + self.r, fill='black')
