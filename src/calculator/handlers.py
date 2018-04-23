# encoding: utf-8
from __future__ import division

from abc import ABCMeta, abstractmethod
from math import pi, e
from re import search

from constants import UPDATE_DISPLAY
from observer import EventManager
from utils import symbol


class IKeyHandler(object):
    # TODO написать документацию для всех интерфейсов, методов и классов
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle_click(self, key):
        pass


class IEventHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def state(self):
        pass

    @abstractmethod
    def add(self, elem):
        pass

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def clear(self):
        pass


class KeyHandler(IKeyHandler):
    UNREPEATABLE_KEYS = ('.', '+', '-', '*', '/', '%', '^', 'e', symbol('pi'))

    def __init__(self):
        self.event_handler = EventHandler()
        self.events = EventManager()

    def handle_click(self, key):
        if key in self.UNREPEATABLE_KEYS and self.event_handler.state \
                and self.event_handler.state[-1] == key:
            return

        elif key == '=':
            self.event_handler.calculate()

        elif key == symbol('<-'):
            self.event_handler.undo()

        elif key == 'C':
            self.event_handler.calculate()

        else:
            self.event_handler.add(key)

        self.events.notify(UPDATE_DISPLAY, self.event_handler.state)


class EventHandler(IEventHandler):
    ELEMENTS_MAPPING = {'^': '**', symbol('pi'): str(pi), 'e': str(e)}

    def __init__(self):
        self.__state = ''
        self.need_clear = False

    @property
    def state(self):
        return self.__state

    @property
    def math_state(self):
        state = self.state
        for elem, math_elem in self.ELEMENTS_MAPPING.items():
            state = state.replace(elem, math_elem)
        return state

    def set_state(self, value):
        self.__state = value

    def add(self, elem):
        if self.need_clear:
            self.clear()
        self.set_state(self.state + elem)

    def clear(self):
        self.set_state('')
        self.need_clear = False

    def undo(self):
        if not self.state:
            return
        if self.need_clear:
            self.clear()
            return
        self.set_state(self.state[:-1])

    def formatted_result(self, result):
        if result % 1 == 0:
            f_result = '{:g}'.format(result)
        elif float(result) < 10 ** 6:
            f_result = '{:.3f}'.format(result)
            f_result = search(r'([\d\.]+?)(0*)$', f_result).groups()[0]
        else:
            f_result = '{:e}'.format(result)
        return '{} = {}'.format(self.state.encode('utf-8'), f_result)

    def calculate(self):
        # TODO не удалять результат вычисления (после '=' можно продолжить
        # работать с полученным числом - через частичную очистку state?
        if self.need_clear:
            self.clear()
        if not self.state:
            return
        try:
            result = eval(self.math_state)
            self.set_state(self.formatted_result(result))
        except (SyntaxError, TypeError):
            self.set_state('Expression is not valid')
        except ZeroDivisionError:
            self.set_state('Division by zero')
        finally:
            self.need_clear = True
