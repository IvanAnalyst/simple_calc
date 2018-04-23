# coding: utf-8

from constants import UPDATE_DISPLAY
from gui import Calculator
from handlers import KeyHandler

if __name__ == '__main__':
    # TODO сделать строителя?
    click_handler = KeyHandler()
    calc = Calculator(click_handler)
    click_handler.events.subscribe(UPDATE_DISPLAY, calc)
    calc.mainloop()
