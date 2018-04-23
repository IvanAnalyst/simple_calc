# coding: utf-8
from __future__ import unicode_literals

from observer import IListener
from utils import symbol, position

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    # Python 2
    import Tkinter as tk
    import ttk


class Calculator(tk.Tk, IListener):
    # TODO сделать чистый класс - граф. интерфейс:
    # вынести добавление команд в другой класс; разделить на создание клавиш
    # и дисплея (?) Чтобы можно было менять квавиши и вид дисплея
    # сделать кнопку "Вид" и уменьшенный калькулятор на 2+2=4
    GRID_SIZE = 4, 6

    _buttons = [
        '7', '8', '9', '/', '<-', 'C',
        '4', '5', '6', '*', '(', ')',
        '1', '2', '3', '-', '^', 'e',
        '0', '.', '%', '+', '=', 'pi']

    def buttons(self):
        for b in self._buttons:
            yield symbol(b)

    def __init__(self, click_handler):
        try:
            super(Calculator, self).__init__()
        except TypeError:
            # Python 2
            tk.Tk.__init__(self)

        self.title('Simple Mouse Calculator')
        self.resizable(width=False, height=False)

        self.click_handler = click_handler
        self._set_body()
        self.display = self.new_display()

    def _set_body(self):
        for ind, b in enumerate(self.buttons()):
            button_style = 'raised'

            def action(key=b):
                return self.click_handler.handle_click(key)

            row, col = position(ind, self.GRID_SIZE[1])
            tk.Button(self, text=b, width=3, height=3, relief=button_style,
                      command=action).grid(row=row + 1, column=col,
                                           sticky='news')

    def new_display(self):
        display = tk.Label(self, width=40, bg="white", anchor='e')
        display.grid(row=0, column=0, columnspan=self.GRID_SIZE[1])
        return display

    def update_it(self, value):
        self.display['text'] = value
