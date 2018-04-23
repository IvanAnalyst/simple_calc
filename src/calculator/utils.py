from constants import SYMBOLS


def symbol(sym):
    return SYMBOLS.get(sym, sym)


def position(index, columns_number):
    """Returns row number and column number"""
    return index // columns_number, index % columns_number
