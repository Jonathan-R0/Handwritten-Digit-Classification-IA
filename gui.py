from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from tkinter import ttk
from PIL import ImageGrab, Image
import numpy as np

model = load_model('mnist.h5')


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.textdata = ""
        self.title("Handwritten Digit Classificator")
        self.iconbitmap('./media/logo.ico')
        self.x = self.y = 0

        self.configure(background='black')
        self.canvas = tk.Canvas(
            self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Procesando",
                              bg="black", font=("Times New Roman", 48), fg="white")
        self.classify_btn = tk.Button(
            self, text="Detectar", command=self.popup_bonus)

        self.canvas.grid(row=0, column=0, pady=10, padx=10, sticky=W, )
        self.classify_btn.grid(row=1, column=0, pady=2, padx=2)

        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def popup_bonus(self):
        self.classify_handwriting()
        win = tk.Toplevel()
        win.configure(background='black')
        win.wm_title("Predicción")
        win.iconbitmap('./media/logo.ico')
        win.geometry("550x165")
        win.label = tk.Label(win, text=self.textdata, font=(
            "Times New Roman", 48), bg="black", fg="white")
        win.label.grid(row=0, column=1, pady=2, padx=2)
        self.clear_all()

    def clear_all(self):
        self.canvas.delete("all")

    def _predict_digit(self, img):
        img = img.resize((28, 28))\
                 .convert('L')
        img = 1 - np.array(img).reshape(1, 28, 28, 1)/255.0
        res = model.predict([img])[0]
        return np.argmax(res), max(res)

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)

        digit, acc = self._predict_digit(im)
        self.textdata = f"El número es {str(digit)}\n con certeza del {str(int(acc*100))}%"
        self.label.configure(text=self.textdata)

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(
            self.x-r, self.y-r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
