import tkinter as tk
from gui import LexicalAnalyzerGUI


def main():
    root = tk.Tk()
    app = LexicalAnalyzerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
