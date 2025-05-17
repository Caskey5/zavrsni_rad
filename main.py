from tkinter import Tk
from modules.auth import AuthSystem
from modules.shared import configure_window

def start_app():
    root = Tk()
    configure_window(root)
    auth = AuthSystem(root)
    auth.show_welcome_screen()
    root.mainloop()

if __name__ == "__main__":
    start_app()