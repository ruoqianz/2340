import tkinter as tk
import random
from ball import Ball

# Create Window class, always at the top of the page
class Window:

    def __init__(self, root):
        self.root = root
        self.root.geometry("300x300")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # Title frame
        self.title_bar = tk.Frame(self.root, bg="#C0D9D9", relief="raised", bd=2)
        self.title_bar.pack(fill=tk.X)

        # Title label
        self.title_label = tk.Label(self.title_bar, text="Bouncing balls", bg="#00FF00", fg="white")
        self.title_label.pack(side=tk.LEFT, expand=True, fill=tk.X)

        # Content frame
        self.content_frame = tk.Frame(self.root, bg="white", bd=2)
        self.content_frame.pack(expand=True, fill=tk.BOTH)

        # Add Canvas to Content frame
        self.canvas = tk.Canvas(self.content_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # Ensure that the entire window and all its subcomponents are updated
        self.root.update()

        # Create balls
        self.balls = []
        self.create_balls(5)

        # Close Bottom
        self.close_button = tk.Button(self.title_bar, text="X", command=self.root.quit, bg="black", fg="white")
        self.close_button.pack(side=tk.RIGHT, padx=5)
        self.close_button.bind("<Button-1>", self.close_window)

        # Drag events
        self.title_bar.bind("<Button-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.on_drag)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_drag)

        # Adjust size events
        self.content_frame.bind("<Button-1>", self.start_resize)
        self.content_frame.bind("<B1-Motion>", self.on_resize)
        self.content_frame.bind("<ButtonRelease-1>", self.stop_resize)

        # Drag offsets
        self.offset_x = 0
        self.offset_y = 0

    # Handling the event conflict between close and drag that occurs when the mouse clicks close bottom
    def close_window(self, event):
        self.root.destroy()
        return "break"

    # Start dragging the window
    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        self.root.config(cursor="hand2")

    # Stop dragging and resume cursor to default
    def stop_drag(self, event):
        self.root.config(cursor="")

    # Handling drag window events
    def on_drag(self, event):
        x = event.x_root - self.offset_x
        y = event.y_root - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    # Start resizing
    def start_resize(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        self.root.config(cursor="cross")

    # Stop dragging and resume cursor to default
    def stop_resize(self,event):
        self.root.config(cursor="")

    # Handling resize window events
    def on_resize(self, event):
        new_width = max(event.x, 200)
        new_height = max(event.y, 200)
        self.root.geometry(f"{new_width}x{new_height}+{self.root.winfo_x()}+{self.root.winfo_y()}")

    # Create 5 blue balls on canvas
    def create_balls(self, num_balls):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Random generate balls and make sure they all on canvas
        for i in range(num_balls):
            radius = 15
            x = random.randint(radius, canvas_width - radius)
            y = random.randint(radius, canvas_height - radius)
            color = "blue"
            ball = Ball(self.canvas, x, y, radius, color)
            self.balls.append(ball)