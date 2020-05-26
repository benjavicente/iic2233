'''Clases del los objetos del juego DCCafé'''

from math import floor
from random import random, choice

from PyQt5.QtCore import QObject, pyqtSignal, Qt

from config.parametros import PARAMETROS
from backend.clock import GameClock


def generate_ids():
    '''Genera un id para cada objeto'''
    counter = 0
    while True:
        yield counter
        counter += 1


class GameObject(QObject):
    '''
    Clase abstracta de un objeto del juego.
    Crea un identificador único al objeto.
    Como atributo tiene display_info, que retorna
    toda la información necesaria para
    mostrar el objeto en la pantalla.
    '''

    _cell_size = int(PARAMETROS['mapa']['tamaño celda'])
    id_counter = generate_ids()
    hitbox_reduction = float(PARAMETROS['mapa']['reducción de hitbox'])

    def __init__(self, core, x: int, y: int, width: int, height: int, initial_state: list):
        super().__init__()
        self.id = str(next(GameObject.id_counter))
        self._x = int(x)
        self._y = int(y)
        self.size = (int(width) * self._cell_size, int(height) * self._cell_size)
        self._object_state = [type(self).__name__.lower()] + initial_state
        self.clocks = list()
        self._animation_state = int()
        self._animation_cicle = list()
        self.core = core
        self.connect_to_core()
        self.core.signal_add_new_object.emit(self.display_info)

    def __repr__(self):
        return type(self).__name__ + self.id

    def update_object(self):
        '''Actualiza el objeto en el ui.'''
        self.core.signal_update_object.emit(self.display_info)

    def delete_object(self):
        '''Elimina el objeto en el ui.'''
        self.core.signal_delete_object.emit(self.display_info)

    def connect_to_core(self):
        '''Conecta las señales con su core asociado'''
        self.core.signal_pause_objects.connect(self.object_clock_pause)
        self.core.signal_resume_objects.connect(self.object_clock_continue)

    def disconnect_to_core(self):
        '''Desconecta las señales del core asociado'''
        self.core.signal_pause_objects.disconnect(self.object_clock_pause)
        self.core.signal_resume_objects.disconnect(self.object_clock_continue)

    def object_clock_pause(self):
        '''Método para pausar los relojes del objeto'''
        for clock in self.clocks:
            clock.pause_()

    def object_clock_continue(self):
        '''Método para pausar los relojes del objeto'''
        for clock in self.clocks:
            clock.continue_()

    def animation(self):
        '''Animación/sprite siguiente'''
        act = self._animation_state
        self._animation_state = (self._animation_state + 1) % len(self._animation_cicle)
        return self._animation_cicle[act]

    def update_animation(self, animation_index: int):
        '''Cambia la animación'''
        self._object_state[animation_index] = self.animation()
        self.update_object()

    @property
    def hit_box(self):
        '''Caja que detecta las colisiones'''
        width, height = self.size
        fact = self.hitbox_reduction
        return (self._x + width * fact / 2,
                self._y + height * fact / 2,
                width * (1 - fact),
                height * (1 - fact))

    @property
    def pos(self):
        '''Posición del objeto'''
        return (self._x, self._y)

    @property
    def display_info(self):
        '''Información que se manda al frontend'''
        return {
            'id': self.id,
            'pos': self.pos,
            'size': self.size,
            'state': tuple(self._object_state),
        }


class Cafe(QObject):
    '''Café que se administra en el juego'''
    def __init__(self):
        super().__init__()
        self.money = int()
        self.rep = int()
        self.rounds = int()
        self.open = True
        self.completed_orders = 0
        self.total_orders = 0

    @property
    def stats(self):
        '''Estadísticas a mostrar en el interfaz'''
        return {
            'money': str(self.money),
            'rep': str(self.rep),
            'round': str(self.rounds),
            'open': str(self.open),
            'completed_orders': str(self.completed_orders),
            'total_orders': str(self.total_orders),
            'failed_orders': str(self.total_orders - self.completed_orders),
        }

    @property
    def round_clients(self):
        '''Clientes de la ronda'''
        alpha = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['factor'])
        beta = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['base'])
        return alpha * (beta + self.rounds)

    def get_new_rep(self) -> int:
        '''
        Calcula la nueva reputación del Café.
        Guarda el valor en el objeto y lo retorna.
        Solo debe ejecutarse al terminar la ronda.
        '''
        min_value = int(PARAMETROS['DCCafé']['calculos']['reputación']['mínimo'])
        max_value = int(PARAMETROS['DCCafé']['calculos']['reputación']['máximo'])
        alpha = int(PARAMETROS['DCCafé']['calculos']['reputación']['factor'])
        beta = int(PARAMETROS['DCCafé']['calculos']['reputación']['resta'])
        expr = self.rep + floor(alpha * self.completed_orders/self.total_orders - beta)
        self.rep = max(min_value, min(max_value, expr))
        return self.rep


class Snack(QObject):
    '''Bocadillo'''
    def __init__(self, chef_exp: int):
        super().__init__()
        self.chef_exp = chef_exp

    def tip_prob(self, wait_time: float):
        '''Cálculo de la propina'''
        min_value = PARAMETROS['bocadillos']['calculos']['calidad pedido']['mínimo']
        base = PARAMETROS['bocadillos']['calculos']['calidad pedido']['base']
        fact = PARAMETROS['bocadillos']['calculos']['calidad pedido']['factor']
        div = PARAMETROS['bocadillos']['calculos']['calidad pedido']['divisor']



# Game Objects

class Player(GameObject):
    '''
    Jugador del juego que empeña el rol de mesero.
    Bonus: Dos jugadores al mismo tiempo.
    '''
    _keys = [
        {Qt.Key_W: 'up', Qt.Key_D: 'right', Qt.Key_S: 'down', Qt.Key_A: 'left'},
        {Qt.Key_I: 'up', Qt.Key_L: 'right', Qt.Key_K: 'down', Qt.Key_J: 'left'}
    ]

    _movemet_direction = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    _movement_speed = PARAMETROS['personaje']['velocidad']

    def __init__(self, core, x: int, y: int):
        # TODO: parametros de disfraz y teclas
        # estado = (jugador, disfraz, libre o ocupado, tipo movimiento, direc movimiento)
        super().__init__(core, x, y, 1, 2, ['a', 'free', 'idle', 'down'])
        self.movemet_keys = self._keys.pop(0)
        self.orders = 0
        self.walked = True
        self._animation_cicle = ['rightfoot', 'idle', 'leftfoot', 'idle']
        self.clock_check_if_walking = GameClock(
            event=self.check_if_walking,
            interval=0.1
        )
        self.clock_check_if_walking.start()
        self.clocks.append(self.clock_check_if_walking)

    def get_order_from_chef(self, order):
        '''Obtine un snack'''
        self._object_state[2] = 'snack'

    def has_key(self, key: int) -> bool:
        '''Ve si tiene la tecla entregada'''
        return key in self.movemet_keys

    def next_pos(self, keys: iter, time_period: float) -> tuple:
        '''Retorna la siguiente posición del objeto luego de moverse'''
        pos_x, pos_y = self._x, self._y
        for key in keys:
            direction = self.movemet_keys[key]
            self._object_state[4] = direction
            direcion_x, direction_y = self._movemet_direction[direction]
            pos_x += direcion_x * (time_period * self._movement_speed)
            pos_y += direction_y * (time_period * self._movement_speed)
        return pos_x, pos_y

    def new_hitbox(self, next_pos: tuple) -> tuple:
        '''Retorna la nueva posición del hitbox'''
        width, height = self.size
        pos_x, pos_y = next_pos
        # No se considera la cabeza en el hitbox del jugador,
        # por lo que se la posición y tamaño del hitbox
        height /= 2
        pos_y += height
        fact = self.hitbox_reduction
        return (pos_x + width * fact / 2,
                pos_y + height * fact / 2,
                width * (1 - fact),
                height * (1 - fact))

    def move(self, pos: tuple):
        '''Mueve al jugador luego de probar que no colisionará en el core.'''
        self._x, self._y = pos
        self.update_object()
        self.core.signal_move_up.emit(self.display_info)
        self.walked = True

    def check_if_walking(self):
        '''Revisa si el jugador camina para cambiar su animación'''
        if self.walked:
            self.walked = False
            self.update_animation(3)
        else:
            self._object_state[3] = 'idle'
            self.update_object()


class Chef(GameObject):
    '''
    Preparan la comida.
    Tienen un nivel de experiencia relacionado con los platos preparador
    '''
    initial_level = PARAMETROS['chef']['nivel inicial']

    def __init__(self, core, x: int, y: int):
        super().__init__(core, x, y, 4, 4, ['idle'])
        self._level = self.initial_level
        self._dishes = int()
        self.order = None
        self.cooking = False

    @property
    def dishes(self):
        '''Platos preparados por el Chef'''
        return self._dishes

    @dishes.setter
    def dishes(self, value):
        self._dishes = value
        if value >= PARAMETROS['chef']['niveles'][self._level]['platos siguiente nivel']:
            self._level = PARAMETROS['chef']['niveles'][self._level]['siguiente nivel']
            print('el chef subió de nivel')

    @property
    def exp(self):
        '''Experiencia del chef'''
        return int(PARAMETROS['chef']['niveles'][self._level]['experiencia'])

    def interact(self, player):
        '''Interación con jugadores'''
        if not self.cooking:
            if self.order:
                player.get_order_from_chef(self.order)
                self._object_state[1] = 'idle'
            else:
                self.start_cooking()
                self.cooking = True

    def start_cooking(self):
        '''El chef prepara un plato'''
        animation_type = choice(['A', 'B'])
        self._animation_cicle = [f'cooking{animation_type}{i}' for i in range(3)]
        # Reloj de cocina
        cooking_animation_time = 0.2
        min_value = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['mínimo'])
        base = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['base'])
        fact = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['factor'])
        total_time = max(min_value, base - self.core.cafe.rep - self.exp * fact)
        self.cook_clock = GameClock(
            interval=cooking_animation_time,
            rep=total_time//cooking_animation_time,
            event=lambda: self.update_animation(1),
            final_event=self.try_recipes
        )
        self.clocks.clear()
        self.clocks.append(self.cook_clock)
        self.cook_clock.start()

    def try_recipes(self):
        '''El chef prueba una receta, donde puede fallar'''
        alpha = float(PARAMETROS['chef']['probabilidad fallar']['factor'])
        beta = float(PARAMETROS['chef']['probabilidad fallar']['suma'])
        gamma = self.exp
        probability = (alpha)/(gamma + beta)
        if random() > probability:
            # EL chef fall y empieza de nuevo
            self.start_cooking()
            print('Receta fallida')
        else:
            self.finish_order()

    def finish_order(self):
        '''Termina la orden y la deja en su mesa'''
        self.cooking = False
        self.dishes += 1
        self._object_state[1] = 'done'
        self.order = Snack(self.exp)
        self.update_object()



class Table(GameObject):
    '''Mesa donde se asignan los clientes'''
    def __init__(self, core, x: int, y: int):
        super().__init__(core, x, y + self._cell_size, 1, 1, [])
        self.free = True
        self.customer = None
        self.table = Chair(core, self._x, self._y - self._cell_size)

    def add_customer(self, customer_type: str, wait_time: int):
        '''Añade un cliente a la mesa y lo retorna'''
        self.free = False
        self.customer = Customer(self.core, *self.pos, self, customer_type, wait_time)
        self.core.signal_stack_under.emit(self.customer.display_info, self.display_info)
        self.core.signal_stack_under.emit(self.table.display_info, self.customer.display_info)
        print(f'Cliente {customer_type} asignado en la mesa con id {self.id}')
        return self.customer

    @property
    def hit_box(self):
        '''Overrite. Permite considada la silla como parte de la mesa'''
        width, height = self.size
        fact = self.hitbox_reduction
        return (self._x + width * fact / 2,
                (self._y - self._cell_size) + height * fact / 2,
                width * (1 - fact),
                (self._cell_size + height) * (1 - fact))


class Chair(GameObject):
    '''Silla de los clientes'''
    def __init__(self, core, x: int, y: int):
        super().__init__(core, x, y, 1, 1, [])


class Customer(GameObject):
    '''Cliente. Es asignado a una mesa aleatoria'''
    def __init__(self, core, x: int, y: int, table, customer_type: str, wait_time: int):
        super().__init__(core, x, y - self._cell_size * 1.5, 1, 2, [customer_type, '1'])
        self.table = table
        self.wait_time = wait_time
        self.customer_type = customer_type
        self._animation_cicle = ['0', '1', '2']
        self._animation_state = 0
        self.wait_clock = GameClock(
            event=lambda: self.update_animation(2),
            interval=wait_time/3,
            final_event=self.exit_cafe,
            rep=3)
        self.clocks.append(self.wait_clock)
        self.wait_clock.start()

    def exit_cafe(self):
        '''Cliente se retira de la mesa'''
        print('me voy >:(')
        self.table.free = True
        self.table.customer = None
        self.clocks.remove(self.wait_clock)
        self.disconnect_to_core()
        self.delete_object()
