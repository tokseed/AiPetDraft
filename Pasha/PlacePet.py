import tkinter as tk


def on_mouse_down(event):
    global dif_x, dif_y

    dif_x, dif_y = event.x, event.y


def update_position(event):
    x = root.winfo_x() + event.x - dif_x
    y = root.winfo_y() + event.y - dif_y

    root.geometry(f"+{x}+{y}")

root = tk.Tk()
root.resizable(False,False)
root.geometry("250x250")
root.config(bg="#000000")
root.overrideredirect(True)
root.wm_attributes("-alpha", 0.1)

root.bind('<ButtonPress-1>', on_mouse_down)
root.bind('<B1-Motion>', update_position)

root.mainloop()
