import tkinter as tk
from tkinter import Menu
from pet import Pet
from bite_overlay import BiteOverlay
from gif_animator import GifAnimator


class ToolTip:
    def __init__(self, widget, text, delay_ms=350):
        self.widget = widget
        self.text = text
        self.delay_ms = delay_ms
        self._after_id = None
        self.tw = None

        widget.bind("<Enter>", self._on_enter, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        widget.bind("<ButtonPress>", self._on_leave, add="+")

    def _on_enter(self, event=None):
        self._cancel()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _on_leave(self, event=None):
        self._cancel()
        self._hide()

    def _cancel(self):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        if self.tw:
            return
        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 8

        self.tw = tk.Toplevel(self.widget)
        self.tw.overrideredirect(True)
        self.tw.attributes("-topmost", True)
        self.tw.configure(bg="#0f0f0f")
        self.tw.geometry(f"+{x}+{y}")

        label = tk.Label(
            self.tw,
            text=self.text,
            bg="#0f0f0f",
            fg="white",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9)
        )
        label.pack(ipadx=6, ipady=3)

    def _hide(self):
        if self.tw:
            try:
                self.tw.destroy()
            except Exception:
                pass
            self.tw = None


class ActionsPopup(tk.Toplevel):
    """Всплывающая панель действий (перетаскивается)"""
    def __init__(self, master_window, callbacks):
        super().__init__(master_window)
        self.callbacks = callbacks

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#000000")

        self._drag_dx = 0
        self._drag_dy = 0

        outer = tk.Frame(self, bg="#000000", padx=8, pady=8)
        outer.pack()

        # Полоса для перетаскивания
        drag_bar = tk.Frame(outer, bg="#141414", height=10, cursor="fleur")
        drag_bar.pack(fill="x", pady=(0, 8))
        drag_bar.bind("<Button-1>", self._start_drag, add="+")
        drag_bar.bind("<B1-Motion>", self._do_drag, add="+")

        btn_frame = tk.Frame(outer, bg="#000000")
        btn_frame.pack()

        def mkbtn(txt, cmd, tip):
            b = tk.Button(
                btn_frame,
                text=txt,
                width=2,
                bd=1,
                relief="solid",
                highlightthickness=0,
                bg="#161616",
                fg="white",
                activebackground="#2b2b2b",
                activeforeground="white",
                command=cmd
            )
            b.pack(side="left", padx=3)
            ToolTip(b, tip)
            return b

        mkbtn("🍖", self.callbacks["feed"], "Покормить")
        mkbtn("🎮", self.callbacks["play"], "Поиграть")
        mkbtn("💤", self.callbacks["sleep"], "Уложить спать")
        mkbtn("🖥", self.callbacks["toggle_bite"], "Режим откусывания")
        mkbtn("♻", self.callbacks["reset_bites"], "Сбросить откусы")
        mkbtn("✖", self.callbacks["quit"], "Выход")

    def _start_drag(self, event):
        self._drag_dx = event.x_root - self.winfo_x()
        self._drag_dy = event.y_root - self.winfo_y()

    def _do_drag(self, event):
        x = event.x_root - self._drag_dx
        y = event.y_root - self._drag_dy
        self.geometry(f"+{x}+{y}")


class PetWindow:
    def __init__(self):
        self.pet = Pet()
        self.root = tk.Tk()
        self.root.title("Desktop Pet")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)

        # прозрачный фон
        self.root.attributes("-transparentcolor", "white")
        self.root.configure(bg="white")

        self.root.geometry("260x260+200+200")

        self.bite_overlay = None
        self.original_position = (200, 200)
        self.is_moving = False
        self.popup = None  # ActionsPopup

        self.offset_x = 0
        self.offset_y = 0

        self.pet_frame = tk.Frame(self.root, bg="white")
        self.pet_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # контейнер гифки
        self.pet_container = tk.Frame(self.pet_frame, bg="white", width=170, height=170)
        self.pet_container.pack(expand=True)
        self.pet_container.pack_propagate(False)

        self.pet_label = tk.Label(self.pet_container, bg="white")
        self.pet_label.place(relx=0.5, rely=0.5, anchor="center")

        # кнопка "≡" на углу гифки
        self.menu_button = tk.Button(
            self.pet_container,
            text="≡",
            font=("Segoe UI", 12, "bold"),
            bg="#0f0f0f",
            fg="white",
            bd=1,
            relief="solid",
            highlightthickness=0,
            activebackground="#2b2b2b",
            activeforeground="white",
            command=self.toggle_popup,
            padx=5,
            pady=0
        )
        self.menu_button.place(relx=1.0, rely=0.0, anchor="ne", x=-2, y=2)
        ToolTip(self.menu_button, "Действия")

        self.animator = GifAnimator(self.pet_label)
        self.load_animation("idle")

        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<ButtonRelease-1>", self.stop_drag)
        self.root.bind("<Button-3>", self.show_context_menu)

        # контекстное меню (запасной способ)
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🍖 Покормить", command=self.feed)
        self.context_menu.add_command(label="🎾 Поиграть", command=self.play_action)
        self.context_menu.add_command(label="😴 Уложить спать", command=self.sleep_pet)
        self.context_menu.add_separator()
        self.context_menu.add_checkbutton(label="🖥️ Режим откусывания", command=self.toggle_bite_mode)
        self.context_menu.add_command(label="🔄 Сбросить откусы", command=self.reset_bites)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="❌ Выход", command=self.quit)

        if self.pet.bite_mode:
            self.init_bite_overlay()

        self.update_pet()
        self.animate_loop()


    # ---------- popup ----------

    def toggle_popup(self):
        # закрывать/открывать только по "≡"
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
            self.popup = None
            return

        callbacks = {
            "feed": self.feed,
            "play": self.play_action,
            "sleep": self.sleep_pet,
            "toggle_bite": self.toggle_bite_mode,
            "reset_bites": self.reset_bites,
            "quit": self.quit
        }
        self.popup = ActionsPopup(self.root, callbacks)

        # показать над питомцем
        self.root.update_idletasks()
        self.popup.update_idletasks()

        root_x = self.root.winfo_rootx()
        root_y = self.root.winfo_rooty()
        root_w = self.root.winfo_width()

        pop_w = self.popup.winfo_width()
        pop_h = self.popup.winfo_height()

        x = root_x + (root_w - pop_w) // 2
        y = root_y - pop_h - 8
        if y < 0:
            y = root_y + 8

        self.popup.geometry(f"+{x}+{y}")

    # ---------- gif ----------

    def load_animation(self, state):
        ok = self.animator.load_gif(state)
        if not ok:
            self.animator.show_emoji(self.pet.get_emotion())

    def animate_loop(self):
        interval = self.animator.animate()
        self.root.after(interval, self.animate_loop)

    # ---------- drag main window ----------

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y
        self.is_moving = True

    def drag(self, event):
        if self.is_moving:
            x = self.root.winfo_x() + event.x - self.offset_x
            y = self.root.winfo_y() + event.y - self.offset_y
            self.root.geometry(f"+{x}+{y}")
            self.original_position = (x, y)

    def stop_drag(self, event):
        self.is_moving = False

    # ---------- context menu ----------

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    # ---------- bite overlay ----------

    def toggle_bite_mode(self):
        self.pet.bite_mode = not self.pet.bite_mode
        self.pet.save_state()

        if self.pet.bite_mode:
            self.init_bite_overlay()
        else:
            if self.bite_overlay:
                self.bite_overlay.destroy()
                self.bite_overlay = None

    def init_bite_overlay(self):
        if self.bite_overlay is None:
            self.bite_overlay = BiteOverlay()
            for i in range(self.pet.bite_count):
                self.bite_overlay.add_bite(i + 1)

    def reset_bites(self):
        self.pet.reset_bites()
        if self.bite_overlay:
            self.bite_overlay.clear_bites()

    # ---------- actions ----------

    def feed(self):
        self.pet.feed()
        if not self.is_moving:
            self.load_animation("eating")

        if self.pet.bite_mode:
            if self.bite_overlay is None:
                self.init_bite_overlay()

            self.original_position = (self.root.winfo_x(), self.root.winfo_y())
            self.animate_to_corner()
            self.root.after(2000, lambda: self.bite_overlay.add_bite(self.pet.bite_count))
            self.root.after(3000, self.return_position)
            self.root.after(4000, lambda: self.load_animation("idle"))
        else:
            self.root.after(2000, lambda: self.load_animation("idle"))

    def play_action(self):
        if self.is_moving:
            return
        self.pet.play()
        self.load_animation("playing")
        self.root.after(2000, lambda: self.load_animation("idle"))

    def sleep_pet(self):
        if self.is_moving:
            return
        self.pet.sleep()
        self.load_animation("sleeping")
        self.root.after(3000, lambda: self.load_animation("idle"))

    # ---------- move to corner ----------

    def animate_to_corner(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        target_x = screen_width - 350
        target_y = screen_height - 400

        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()

        steps = 30
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps

        def move_step(step=0):
            if step < steps and not self.is_moving:
                new_x = int(current_x + dx * step)
                new_y = int(current_y + dy * step)
                self.root.geometry(f"+{new_x}+{new_y}")
                self.root.after(30, lambda: move_step(step + 1))

        move_step()

    def return_position(self):
        target_x, target_y = self.original_position
        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()

        steps = 20
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps

        def move_step(step=0):
            if step < steps and not self.is_moving:
                new_x = int(current_x + dx * step)
                new_y = int(current_y + dy * step)
                self.root.geometry(f"+{new_x}+{new_y}")
                self.root.after(30, lambda: move_step(step + 1))

        move_step()

    # ---------- tick ----------

    def update_pet(self):
        self.pet.tick()
        self.root.after(10000, self.update_pet)

    # ---------- quit ----------

    def quit(self):
        self.pet.save_state()
        if self.bite_overlay:
            self.bite_overlay.destroy()
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
        self.root.destroy()


if __name__ == "__main__":
    w = PetWindow()
    w.root.mainloop()

