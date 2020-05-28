'''
Ventana del Juego DCCafé
'''

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QPixmap, QCursor, QTransform, QDrag
from PyQt5.QtWidgets import QLabel, QWidget, QFrame, QGridLayout, QSizePolicy

from frontend.paths import SPRITE_PATH
from frontend.themes import GAME_THEME

from config.parametros import PARAMETROS


class GameWindow(*uic.loadUiType(SPRITE_PATH['ui', 'game_window'])):
    '''Ventana del juego'''

    signal_key_press = pyqtSignal(int)
    signal_key_relase = pyqtSignal(int)

    signal_pause_continue = pyqtSignal()

    signal_buy_object = pyqtSignal(dict)  # Tipo & pos
    signal_sell_object = pyqtSignal(tuple) # pos

    signal_start_round = pyqtSignal()

    cell_size = PARAMETROS['mapa']['tamaño celda']

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Mapa
        self.y_game_offset = self.cell_size * 4
        # SetUp
        self.add_special_ui()
        self.add_style()
        # Objetos del juego a mostrar en el cuadro de juego
        self.game_objects = dict()
        # Pausa/Continuar
        self.paused = False
        self.button_time.pressed.connect(self.signal_pause_continue.emit)
        # Continuar de pre-fase
        self.start_round.pressed.connect(self.signal_start_round.emit)

    def add_style(self):
        '''
        Añade las imágenes, el estilo de la ventana y algunas animaciones.
        Se realiza en código ya que no se pudo realizar fácilmente en
        designer o porque permite cambios rápidos en algún path o estilo.
        '''
        # Logo
        self.logo.setPixmap(QPixmap(SPRITE_PATH['logo']))
        # Estrellas
        self.filed_star_pixmap = QPixmap(SPRITE_PATH['star', 'filed'])
        self.empty_star_pixmap = QPixmap(SPRITE_PATH['star', 'empty'])
        # Es raro que PointingHandCursor no este disponible en Designer...
        self.button_exit.setCursor(QCursor(Qt.PointingHandCursor))
        self.button_time.setCursor(QCursor(Qt.PointingHandCursor))
        self.start_round.setCursor(QCursor(Qt.PointingHandCursor))
        self.setStyleSheet(GAME_THEME)

    def add_special_ui(self):
        '''Añade widgets especiales que no se pueden añadir en designer'''
        # Habilitar Drop
        game_grid = QGridLayout()
        game_grid.setContentsMargins(*[0] * 4)
        game_grid.setSpacing(0)
        self.game_area = DropArea(
            self.game_frame,
            y_offset=self.y_game_offset,
            drop_signal=self.signal_buy_object,
            double_click_signal=self.signal_sell_object
        )
        self.game_area.setAcceptDrops(True)
        self.game_area.setLayout(game_grid)
        self.game_area.setObjectName('game_area')
        self.game_area.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.game_frame.layout().addWidget(self.game_area)
        # Habilitar Drag
        # Chef
        self.chef = DragItem(self.shop)
        self.chef.setFixedSize(*[self.cell_size * 4] * 2)
        self.chef.setObjectName('chef')
        self.chef.setPixmap(QPixmap(SPRITE_PATH['shop', 'chef']))
        self.chef_layout.addWidget(self.chef)
        # Tabla
        self.table = DragItem(self.shop)
        self.table.setFixedSize(self.cell_size, self.cell_size * 2)
        self.table.setObjectName('table')
        self.table.setPixmap(QPixmap(SPRITE_PATH['shop', 'table']))
        self.table_layout.addWidget(self.table)

    def start(self, map_size: tuple):
        '''Inicia el juego'''
        # TODO: música?
        self.make_map(*map_size)  # Como es tupla se puede separar
        self.grabKeyboard()
        self.show()

    def keyPressEvent(self, key_event):
        # TODO: ver como implementar sin método los eventos
        '''Entrega las teclas apretadas al backend'''
        self.signal_key_press.emit(key_event.key())

    def keyReleaseEvent(self, key_event):
        # TODO: ver como implementar sin método los eventos
        '''Entrega las teclas soltadas al backend'''
        self.signal_key_relase.emit(key_event.key())

    def paused_ui(self, paused: bool):
        '''
        Pausa o continua el juego.
        Cambia el texto del botón.
        '''
        self.game_area.setDisabled(paused)
        if paused:
            self.button_time.setText('Seguir')
        else:
            self.button_time.setText('Pausar')

    def enable_shop(self, enable: bool):
        '''Desactiva o activa la tienda'''  #* Puede ser desactivar mejor
        self.chef.setDisabled(not enable)
        self.table.setDisabled(not enable)
        self.start_round.setHidden(not enable)
        self.game_area.set_disable_double_clicks(not enable)

    def update_cafe_stats(self, stats: dict):
        '''Actualiza los datos del Café en la ventana'''
        for name, value in stats.items():
            if name == 'rep':
                value = int(value)
                for i in range(5):
                    if value:
                        #! Obtener un widget de un layout
                        #! https://stackoverflow.com/a/16707157
                        self.stars_layout.itemAt(i).widget().setPixmap(self.filed_star_pixmap)
                        value -= 1
                    else:
                        self.stars_layout.itemAt(i).widget().setPixmap(self.empty_star_pixmap)
            if name == 'round_clients':
                self.day_progress.setMaximum(int(value))
            elif name == 'remaining_clients':
                self.day_progress.setValue(int(value))
            else:
                #! Obtener un atributo sin causar error
                #! https://stackoverflow.com/a/611708
                label = getattr(self, name, False)
                if label:
                    label.setText(str(value))

    def add_new_object(self, obj: dict):
        '''Crea un nuevo objeto en el area de juego'''
        new_object = QLabel(self.game_area)
        pos_x, pos_y = obj['pos']
        new_object.setGeometry(pos_x, pos_y + self.y_game_offset, *obj['size'])
        new_object.setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        new_object.setScaledContents(True)
        new_object.show()
        self.game_objects[obj['id']] = new_object

    def update_object(self, obj: dict):
        '''Actualiza el sprite y la posición del objeto'''
        self.game_objects[obj['id']].setPixmap(QPixmap(SPRITE_PATH[obj['state']]))
        pos_x, pos_y = obj['pos']
        self.game_objects[obj['id']].move(pos_x, pos_y + self.y_game_offset)

    def delete_object(self, obj: dict):
        '''Elimina un objeto'''
        self.game_objects[obj['id']].hide()
        self.game_objects[obj['id']].deleteLater()
        del self.game_objects[obj['id']]

    def stack_under(self, obj_below: dict, obj_above: dict):
        '''Mueve un objeto detrás de otro'''
        self.game_objects[obj_below['id']].stackUnder(self.game_objects[obj_above['id']])

    def move_up(self, obj: dict):
        '''Mueve el objeto hacia adelante'''
        self.game_objects[obj['id']].raise_()

    def make_map(self, width: int, height: int):
        '''Crea el mapa del juego a partir de los mapámetros dados'''
        if width % self.cell_size or height % self.cell_size:
            raise ValueError('El tamaño de la celda no es factor del tamaño del mapa')

        grid_width = width // self.cell_size
        grid_height = height // self.cell_size

        if grid_width % 2:
            raise ValueError('La cantidad de celdas en el eje X debe ser múltiplo de 2')

        self.game_frame.setFixedSize(width, height + self.y_game_offset)

        area_grid = self.game_area.layout()

        window = QPixmap(SPRITE_PATH['map', 'window'])
        wall = QPixmap(SPRITE_PATH['map', 'wall'])
        tile = QPixmap(SPRITE_PATH['map', 'tile'])
        border = QPixmap(SPRITE_PATH['map', 'border'])

        # Se añade decoración
        for x_pos in range(0, grid_width, 2):
            decoration = QLabel(self.game_area)
            if x_pos % 4:
                decoration.setPixmap(window)
            else:
                decoration.setPixmap(wall)
            decoration.setFixedSize(self.cell_size * 2, self.cell_size * 4)
            decoration.setScaledContents(True)
            area_grid.addWidget(decoration, 0, x_pos, 1, 2)

        # Se crean las celdas y se añaden al grid del juego
        for x_pos in range(grid_width):
            for y_pos in range(grid_height):
                cell = QLabel(self.game_area)
                if y_pos:
                    cell.setPixmap(tile)
                else:
                    rotation = QTransform().rotate(90)
                    cell.setPixmap(border.transformed(rotation))
                cell.setFixedSize(self.cell_size, self.cell_size)
                cell.setScaledContents(True)
                area_grid.addWidget(cell, y_pos + 1, x_pos, 1, 1)



#! Esta parte fue realizada con la respuesta de David Wallace, que
#! es una adaptación de la respuesta de Avaris, en StackOverflow
#! https://stackoverflow.com/q/14395799
#! https://stackoverflow.com/a/48203489

class DragItem(QLabel):
    '''QLabel con drag and drop'''
    def __init__(self, *args):
        super().__init__(*args)
        self.setCursor(QCursor(Qt.OpenHandCursor))
        self.setScaledContents(True)

    def mouseMoveEvent(self, event):
        '''Drag del objeto (Overrite)'''
        # Infromación del label
        mime_data = QMimeData()
        mime_data.setText(','.join(map(str, [
            self.objectName(), event.x(), event.y(), self.width(), self.height()
        ])))
        # Drag
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(QWidget.grab(self))
        drag.setHotSpot(event.pos())
        drag.exec_()


class DropArea(QFrame):
    '''Área donde se puede recibir un drop'''
    def __init__(self, *args, y_offset, drop_signal, double_click_signal):
        super().__init__(*args)
        self.y_offset = y_offset
        self.drop_signal = drop_signal
        self.double_click_signal = double_click_signal
        self.accept_double_clicks = True  # Para borrar objetos en preronda

    def set_disable_double_clicks(self, value):
        '''Establece el valor de accept_double_clicks'''
        self.accept_double_clicks = not value

    def mouseDoubleClickEvent(self, event):
        '''Permite ver donde se realizó un double-click (Overrite)'''
        if self.accept_double_clicks:
            self.double_click_signal.emit((event.x(), event.y() - self.y_offset))

    def dragEnterEvent(self, event):
        '''Acepta los drops (Overrite)'''
        event.accept()

    def dropEvent(self, event):
        '''Recibe los drops (Overrite)'''
        # Datos del label
        mime_data = event.mimeData().text().split(',')
        name = mime_data[0]
        relative_x, relative_y, size_x, size_y = map(int, mime_data[1:])
        # Información del drop
        drop_pos = event.pos()
        drop_x, drop_y = map(int, [drop_pos.x(), drop_pos.y()])
        # Ver si la posición final es válida
        final_x = drop_x - relative_x
        final_y = drop_y - relative_y - self.y_offset
        is_valid = all([
            final_x > 0, final_y > 0,
            final_x + size_x < self.width(),
            final_y + size_y < self.height()  - self.y_offset
        ])
        if is_valid:
            event.accept()
            self.drop_signal.emit({
                'type': name,
                'pos': (final_x, final_y),
                'size': (size_x, size_y)
            })
