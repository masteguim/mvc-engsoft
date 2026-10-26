import tkinter as tk

from model.model import BookstoreModel
from view.view import BookstoreView
from controller.controller import BookstoreController


def main():
    root = tk.Tk()

    model = BookstoreModel()
    view = BookstoreView(root)
    BookstoreController(model, view)

    root.mainloop()


if __name__ == "__main__":
    main()