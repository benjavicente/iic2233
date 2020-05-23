'''
Parámetros de estílos del programa.
Lee los temas de la carpeta themes.
'''
from os.path import join
from os import getcwd


def style_path(file_name) -> str:
    '''Retorna el path completo del archivo css'''
    return join(getcwd(), 'frontend', 'themes', file_name)


with open(style_path('game_window.css'), 'r', encoding='utf-8') as file:
    GAME_THEME = file.read()

with open(style_path('initial_window.css'), 'r', encoding='utf-8') as file:
    INITIAL_THEME = file.read()

with open(style_path('summary_window.css'), 'r', encoding='utf-8') as file:
    SUMMARY_THEME = file.read()
