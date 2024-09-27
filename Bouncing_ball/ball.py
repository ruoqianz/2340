# Create Ball class
class Ball:
    def __init__(self, canvas, x, y, radius, color):
        self.canvas = canvas
        self.id = canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill=color
        )
        self.radius = radius
