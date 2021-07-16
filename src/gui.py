from pencil import Pencil
from keras.models import load_model
from tkinter import *
import tkinter as tk
import win32gui
from tkinter import ttk
from PIL import ImageGrab, Image
import numpy as np

model = load_model('../mnist.h5')
SCREEN_SIZE = "550x165"
CANVAS_SIZE = 300


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.textdata = ""
        self.title("Handwritten Digit Classificator")
        self.iconbitmap('../media/logo.ico')
        self.pencil = Pencil()

        self.configure(background='black')
        self.canvas = tk.Canvas(
            self, bg="white", cursor="cross", width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.label = tk.Label(self, text="Procesando",
                              bg="black", font=("Times New Roman", 48), fg="white")
        self.boton = tk.Button(
            self, text="Detectar", command=self.popup_bonus)

        self.canvas.grid(row=0, column=0, pady=10, padx=10, sticky=W, )
        self.boton.grid(row=1, column=0, pady=2, padx=2)

        self.canvas.bind("<B1-Motion>", self.draw)

    def popup_bonus(self):
        self.classify()
        window = tk.Toplevel()
        window.configure(background='black')
        window.wm_title("Predicción")
        window.iconbitmap('../media/logo.ico')
        window.geometry(SCREEN_SIZE)
        window.label = tk.Label(window, text=self.textdata, font=(
            "Times New Roman", 48), bg="black", fg="white")
        window.label.grid(row=0, column=1, pady=2, padx=2)
        self.canvas.delete("all")

    def _predict_digit(self, imagen):
        """Ajustamos la imagen y hacemos la predicción"""
        imagen = imagen.resize((28, 28))\
                       .convert('L')
        imagen = 1 - np.array(imagen).reshape(1, 28, 28, 1)/255.0
        res = model.predict([imagen])[0]
        return np.argmax(res), max(res)

    def classify(self):
        resultado, porcentaje = self._predict_digit(
            ImageGrab.grab(win32gui.GetWindowRect(self.canvas.winfo_id())))
        self.textdata = f"El número es {resultado}\n con certeza del {int(porcentaje*100)}%"
        self.label.configure(text=self.textdata)

    def draw(self, event):
        self.pencil.update(event)
        self.pencil.draw(self.canvas.create_oval)
