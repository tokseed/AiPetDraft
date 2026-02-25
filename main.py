import os

python_path = r'C:\Users\Иван\AppData\Local\Python\pythoncore-3.14-64'
os.environ['TCL_LIBRARY'] = os.path.join(python_path, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(python_path, 'tcl', 'tk8.6')

from pet_window import PetWindow
from hud import HUD

if __name__ == '__main__':
    w = PetWindow()

    # HUD всегда поверх, отдельное окно
    hud = HUD(w.root, w.pet, x=40, y=40)

    def hud_loop():
        if hud.winfo_exists():
            hud.update_bars()
            w.root.after(250, hud_loop)

    hud_loop()
    w.root.mainloop()
