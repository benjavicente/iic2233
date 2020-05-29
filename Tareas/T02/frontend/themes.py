'''Parámetros de estílos del programa. Lee los temas de la carpeta themes.'''

from os.path import join
from os import getcwd

# Esto se ejecuta una vez, y no para cada importación del programa
# https://docs.python.org/3/tutorial/modules.html#more-on-modules


def _style_path(file_name) -> str:
    '''Retorna el path completo del archivo css'''
    return join(getcwd(), 'frontend', 'themes', file_name)


with open(_style_path('game_window.css'), 'r', encoding='utf-8') as file:
    GAME_THEME = file.read()

with open(_style_path('initial_window.css'), 'r', encoding='utf-8') as file:
    INITIAL_THEME = file.read()

with open(_style_path('summary_window.css'), 'r', encoding='utf-8') as file:
    SUMMARY_THEME = file.read()
