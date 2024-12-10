import tkinter as tk
import random
import math
import threading
import time
import psutil
from ball import Ball

class Window:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes('-transparentcolor', 'white')

        # Add Window Drag and Drop
        self.offset_x = 0
        self.offset_y = 0
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_move)

        # ball canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # ball background
        window_diameter = 600
        self.canvas.create_oval(0, 0, window_diameter, window_diameter, fill="lightblue", outline="")

        self.root.update()

        # create balls
        self.balls = []
        self.create_balls(100)

        # close button
        self.close_button = tk.Button(self.root, text="X", command=self.root.quit, bg="black", fg="white")
        self.close_button.place(x=window_diameter - 30, y=10)

        # Initialise network upload traffic reference point
        net_io = psutil.net_io_counters()
        self.old_bytes_sent = net_io.bytes_sent

        # update thread
        self.update_thread = threading.Thread(target=self.update_system_data)
        self.update_thread.daemon = True
        self.update_thread.start()

        self.animate()

    def animate(self):
        for ball in self.balls:
            self.root.after(0, ball.move)
        # Update screen every 50ms
        self.root.after(50, self.animate)

    # Start moving the window
    def start_move(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    # Drag the window
    def on_move(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")


    def create_balls(self, num_balls):
        window_center_x = self.canvas.winfo_width() / 2
        window_center_y = self.canvas.winfo_height() / 2
        window_radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) / 2

        for i in range(num_balls):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, window_radius - 30)
            x = window_center_x + distance * math.cos(angle)
            y = window_center_y + distance * math.sin(angle)
            ball = Ball(self.canvas, x, y)
            self.balls.append(ball)

    # Change color based on time
    def get_color(self):
        t = int(time.time()) % 60
        if t < 20:
            return "blue"
        elif 20 <= t < 40:
            return "purple"
        else:
            return "red"



    # Updating system data in a background thread
    def update_system_data(self):
        while True:
            cpu_usage = psutil.cpu_percent()
            net_io = psutil.net_io_counters()
            new_bytes_sent = net_io.bytes_sent

            # Calculate upload_speed
            interval = 20.0
            bytes_sent_diff = new_bytes_sent - self.old_bytes_sent

            upload_speed = (bytes_sent_diff * 8) / (interval * 1024 * 1024)

            self.old_bytes_sent = new_bytes_sent

            color = self.get_color()
            for ball in self.balls:
                # Pass in upload_speed to update properties

                self.root.after(0, ball.update_properties, cpu_usage, color, upload_speed)

            time.sleep(5)

