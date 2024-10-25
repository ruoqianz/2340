import random
import math

class Ball:
    def __init__(self, canvas, center_x, center_y):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y
        self.radius = 13
        self.color = "yellow"
        self.speed_x = 1
        self.speed_y = 1

        self.id = self.canvas.create_oval(center_x - self.radius, center_x - self.radius,
                                          center_x + self.radius, center_x + self.radius, fill=self.color)

    def move(self):
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        pos = self.canvas.coords(self.id)
        x = (pos[0] + pos[2]) / 2
        y = (pos[1] + pos[3]) / 2

        # Change of direction of motion when hitting the boundary
        window_center_x = self.canvas.winfo_width() / 2
        window_center_y = self.canvas.winfo_height() / 2
        window_radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 2
        distance_to_center = math.sqrt((x - window_center_x) ** 2 + (y - window_center_y) ** 2)

        if distance_to_center + self.radius >= window_radius:
            if (x - window_center_x) ** 2 + (y - window_center_y) ** 2 >= window_radius ** 2:
                # reversing the x and y direction
                self.speed_x = -self.speed_x
                self.speed_y = -self.speed_y

    def update_properties(self, cpu_usage, mem_usage, color):
        # Updated size, speed and colours
        self.radius =int(math.log(mem_usage + 1) * 1.5)
        self.speed_x = cpu_usage * random.uniform(0, 1)
        self.speed_y = cpu_usage * random.uniform(0, 1)
        self.color = color

        # Updating the ball on the canvas

        self.canvas.itemconfig(self.id, fill=self.color)



