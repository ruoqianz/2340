import random
import math


class Ball:
    def __init__(self, canvas, center_x, center_y):
        self.canvas = canvas
        self.center_x = center_x
        self.center_y = center_y

        self.radius = 5
        self.color = "blue"

        self.speed_x = 2
        self.speed_y = 2

        # Drawing the ball on the canvas
        self.id = self.canvas.create_oval(
            center_x - self.radius, center_y - self.radius,
            center_x + self.radius, center_y + self.radius,
            fill=self.color
        )

    def move(self):
        # Moving the ball
        self.canvas.move(self.id, self.speed_x, self.speed_y)
        pos = self.canvas.coords(self.id)
        x = (pos[0] + pos[2]) / 2
        y = (pos[1] + pos[3]) / 2

        # Window centre and radius
        window_center_x = self.canvas.winfo_width() / 2
        window_center_y = self.canvas.winfo_height() / 2
        window_radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 2
        distance_to_center = math.sqrt((x - window_center_x) ** 2 + (y - window_center_y) ** 2)

        # Detecting if the boundary is exceeded
        if distance_to_center + self.radius >= window_radius:
            # Calculate the distance beyond the boundary
            overlap = distance_to_center + self.radius - window_radius

            # Reverse velocity direction
            self.speed_x = -self.speed_x
            self.speed_y = -self.speed_y

            # Adjust the position so that the ball re-enters the boundary
            adjust_x = overlap * (x - window_center_x) / distance_to_center
            adjust_y = overlap * (y - window_center_y) / distance_to_center
            self.canvas.move(self.id, -adjust_x, -adjust_y)

    def update_properties(self, cpu_usage, color, upload_speed):

        # Use cpu_usage to determine the size
        self.radius = int(max(5, cpu_usage * 5))

        # Use upload_speed to determine the speed of the ball.

        self.speed_x = upload_speed * 20
        self.speed_y = upload_speed * 10

        # Updating colours
        self.color = color
        print(f"cpu_usage：{cpu_usage:.2f}%")
        print(f"upload_speed：{upload_speed} Mbps")

        # Update the display properties of the ball on the canvas
        pos = self.canvas.coords(self.id)
        x_center = (pos[0] + pos[2]) / 2
        y_center = (pos[1] + pos[3]) / 2
        self.canvas.coords(self.id,
                           x_center - self.radius, y_center - self.radius,
                           x_center + self.radius, y_center + self.radius)
        self.canvas.itemconfig(self.id, fill=self.color)
