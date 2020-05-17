'''
Parámetros y herramientas relacionados con el UI
'''

RUTA_LOGO = R'sprites\otros\logo_blanco.png'

# FONT_FAMILY = 'Roboto Slab', 'Rockwell', 'Arial Black'
#           2 = 'HP Simplified', 'Shruti', 'Arial'

# Verde: hsl(161, 98, 70)
# Verde claro: hsl(161, 98, 100)

STYLE_SHEET_VENTANA_INICIO = R'''
.VentanaInicio {
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
.QLabel .QFrame .QToolTip{
    font-family: 'HP Simplified';
}
.QFrame {
    background-color: white;
    border-radius: 8px;
    margin: 10px;
}
QFrame > .QLabel {
    font-size: 24px;
}
QToolTip {
    font-size: 14px;
}
VentanaInicio > .QLabel {
    color: rgb(133, 133, 133);
    font-size: 14px;
    font-family: consolas
}
'''
