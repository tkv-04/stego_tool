import sys
import os
from ttkthemes import ThemedTk
from tkinter import ttk

from ui.main_window import MainWindow
from ui.styles import apply_styles

def main():
    root = ThemedTk(theme="black")
    apply_styles()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
