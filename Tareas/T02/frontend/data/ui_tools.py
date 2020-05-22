'''
Parámetros y herramientas relacionados con el UI
'''

from os.path import join
from os import getcwd

# TODO: buscar una fuente para los textos

RUTA_LOGO = join(getcwd(), 'sprites', 'otros', 'logo_blanco.png')
RUTA_ESTRELLA_LLENA = join(getcwd(), 'sprites', 'otros', 'estrella_amarilla.png')
RUTA_ESTRELLA_VACIA = join(getcwd(), 'sprites', 'otros', 'estrella_blanca.png')
RUTA_CELDA = join(getcwd(), 'sprites', 'mapa', 'mapa_2_parte_02.png')
RUTA_DEC_1 = join(getcwd(), 'sprites', 'mapa', 'mapa_2_parte_03.png')
RUTA_DEC_2 = join(getcwd(), 'sprites', 'mapa', 'mapa_2_parte_01.png')
RUTA_TIENDA_CHEF = join(getcwd(), 'sprites', 'chef', 'meson_00.png')
RUTA_TIENDA_MESA = join(getcwd(), 'sprites', 'mapa', 'accesorios', 'silla_mesa_roja.png')

# FONT_FAMILY = 'Roboto Slab', 'Rockwell', 'Arial Black'
#           2 = 'HP Simplified', 'Shruti', 'Arial'

# Verde: hsl(161, 98, 70)
# Verde claro: hsl(161, 98, 100)

STYLE_SHEET_VENTANA_INICIO = R'''
#VentanaInicio {
    background-color: black;
    border-radius: 15px;
    padding: 15px;
}
.QPushButton {
    font-family: 'Rockwell';
    font-size: 24px;
    border-radius: 8px;
    background-color: hsl(161, 98, 70);
    color: white;
    margin: 2px;
    height: 35px;
}
.QPushButton:hover{
    background-color: hsl(161, 98, 100);
}
#cuadro {
    background-color: white;
    border-radius: 8px;
    margin: 10px;
}
#bienvenida {
    font-size: 24px;
}
#desarrollador {
    color: rgb(133, 133, 133);
    font-size: 14px;
    font-family: consolas
}
'''

STYLE_SHEET_VENTANA_POSTERIOR = R'''
VentanaPosterior{
    background-color: black;
}
#bloque {
    background-color: white;
    border-radius: 10px;
    padding: 20px 5px;
}
#titulo {
    font-family: 'Rockwell';
    font-size: 38px;
}
#salir, #guardar, #continuar {
    margin: 2px;
    font-size: 20px;
    border-radius: 8px;
    background-color: hsl(161, 98, 70);
    color: white;
    height: 35px;
    width: 120px;
}
#salir:hover, #guardar:hover, #continuar:hover {
    background-color: hsl(161, 98, 100);
}
#pedidos, #atendidos, #dinero {
    font-family: consolas;
    font-size: 20px;
}
#label_pedidos, #label_atendidos, #label_dinero {
    font-size: 20px;
}
#rep{
    font-family: 'Rockwell';
    font-size: 24px;
}
#linea{
    background-color: hsl(161, 98, 70);
    border-radius: 2px;
    margin: 0px 30px 0px 30px;
}
'''

STYLE_SHEET_VENTANA_JUEGO = R'''
#GameWindow {
    background-color: lightgreen;
}
'''