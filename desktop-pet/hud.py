import tkinter as tk


class HUD(tk.Toplevel):
    """Пассивный HUD со статами (перетаскивается мышью)"""
    def __init__(self, master, pet, x=40, y=40):
        super().__init__(master)
        self.pet = pet

        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # прозрачность (белый будет невидимым)
        self.configure(bg="white")
        self.attributes("-transparentcolor", "white")

        self.bar_width = 160
        self.bar_height = 12

        self._drag_x = 0
        self._drag_y = 0

        self.frame = tk.Frame(self, bg="white")
        self.frame.pack()

        self.hunger = tk.Canvas(self.frame, width=self.bar_width, height=self.bar_height,
                                bg="white", highlightthickness=0)
        self.hunger.pack(pady=2)

        self.energy = tk.Canvas(self.frame, width=self.bar_width, height=self.bar_height,
                                bg="white", highlightthickness=0)
        self.energy.pack(pady=2)

        self.mood = tk.Canvas(self.frame, width=self.bar_width, height=self.bar_height,
                              bg="white", highlightthickness=0)
        self.mood.pack(pady=2)

        # перетаскивание — можно тащить за любой бар
        for w in (self.hunger, self.energy, self.mood):
            w.bind("<Button-1>", self._start_drag, add="+")
            w.bind("<B1-Motion>", self._do_drag, add="+")

        self.geometry(f"+{x}+{y}")
        self.update_bars()

    def _start_drag(self, event):
        self._drag_x = event.x_root - self.winfo_x()
        self._drag_y = event.y_root - self.winfo_y()

    def _do_drag(self, event):
        x = event.x_root - self._drag_x
        y = event.y_root - self._drag_y
        self.geometry(f"+{x}+{y}")

    def _draw_bar(self, canvas, value, color, bg_color, icon):
        canvas.delete("all")
        w = self.bar_width
        h = self.bar_height
        r = h // 2

        # капсула фон
        canvas.create_rectangle(r, 0, w - r, h, fill=bg_color, outline=bg_color)
        canvas.create_oval(0, 0, h, h, fill=bg_color, outline=bg_color)
        canvas.create_oval(w - h, 0, w, h, fill=bg_color, outline=bg_color)

        fill_w = int((value / 100) * w)
        fill_w = max(0, min(w, fill_w))
        if fill_w > 0:
            if fill_w < h:
                canvas.create_oval(0, 0, h, h, fill=color, outline=color)
            else:
                canvas.create_rectangle(r, 0, fill_w - r, h, fill=color, outline=color)
                canvas.create_oval(0, 0, h, h, fill=color, outline=color)
                canvas.create_oval(fill_w - h, 0, fill_w, h, fill=color, outline=color)

        # иконка белая + число белое
        canvas.create_text(10, h // 2, text=icon, fill="white", font=("Segoe UI", 8, "bold"))
        canvas.create_text(w - 10, h // 2, text=str(value), fill="white", font=("Segoe UI", 8, "bold"))

    def update_bars(self):
        self._draw_bar(self.hunger, self.pet.hunger, "#e74c3c", "#3d1a1a", "🍖")
        self._draw_bar(self.energy, self.pet.energy, "#3498db", "#1a2a3d", "⚡")
        self._draw_bar(self.mood, self.pet.mood, "#2ecc71", "#1a3d1a", "😊")
