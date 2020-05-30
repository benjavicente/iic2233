'''Clases del los objetos del juego DCCafé'''

from random import random, choice
from time import time

from PyQt5.QtCore import QObject, Qt

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
        super().__init__(core)  # QObject toma como argumento el QObject padre
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

    def __repr__(self):
        return type(self).__name__ + self.id

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

    def update_object(self) -> None:
        '''Actualiza el objeto en el ui.'''
        self.core.signal_update_object.emit(self.display_info)

    def connect_to_core(self) -> None:
        '''Conecta las señales con su core asociado'''
        self.core.signal_add_new_object.emit(self.display_info)
        self.core.signal_pause_objects.connect(self.object_clock_pause)
        self.core.signal_resume_objects.connect(self.object_clock_continue)

    def delete_object(self) -> None:
        '''Elimina el objeto en el ui y desconecta sus señales'''
        self.core.signal_delete_object.emit(self.display_info)
        self.core.signal_pause_objects.disconnect(self.object_clock_pause)
        self.core.signal_resume_objects.disconnect(self.object_clock_continue)
        self.deleteLater()  # No se si esto tiene efecto

    def object_clock_pause(self) -> None:
        '''Método para pausar los relojes del objeto'''
        for clock in self.clocks:
            clock.pause_()

    def object_clock_continue(self) -> None:
        '''Método para pausar los relojes del objeto'''
        for clock in self.clocks:
            clock.continue_()

    def update_animation(self, animation_index: int) -> None:
        '''Cambia la animación'''
        act = self._animation_state % len(self._animation_cicle)
        self._animation_state = (self._animation_state + 1) % len(self._animation_cicle)
        self._object_state[animation_index] = self._animation_cicle[act]
        self.update_object()


class Snack(QObject):
    '''Bocadillo'''
    def __init__(self, chef_exp: int):
        super().__init__()
        self.chef_exp = chef_exp

    # El calculo del tiempo de preparación dr realiza en el chef

    def quality(self, wait_time: float) -> int:
        '''Cálculo de la calidad'''
        min_value = PARAMETROS['bocadillos']['calculos']['calidad pedido']['mínimo']
        base = PARAMETROS['bocadillos']['calculos']['calidad pedido']['base']
        fact = PARAMETROS['bocadillos']['calculos']['calidad pedido']['factor']
        div = PARAMETROS['bocadillos']['calculos']['calidad pedido']['divisor']
        return max(min_value, (self.chef_exp * (base - wait_time * fact))/div)


# Game Objects

class Player(GameObject):
    '''Jugador del juego que empeña el rol de mesero'''
    _keys = [
        {Qt.Key_W: 'up', Qt.Key_D: 'right', Qt.Key_S: 'down', Qt.Key_A: 'left'},
        {Qt.Key_I: 'up', Qt.Key_L: 'right', Qt.Key_K: 'down', Qt.Key_J: 'left'}
    ]
    _skins = ['a', 'b']

    _movemet_direction = {'up': (0, -1), 'right': (1, 0), 'down': (0, 1), 'left': (-1, 0)}
    _movement_speed = PARAMETROS['personaje']['velocidad']

    def __init__(self, core: object, x: int, y: int):
        super().__init__(core, x, y, 1, 2, [self._skins.pop(0), 'free', 'idle', 'down'])
        self.movemet_keys = self._keys.pop(0)
        self.orders = 0
        self.current_order = None
        self.walked = False
        self._animation_cicle = ['rightfoot', 'idle', 'leftfoot', 'idle']
        self.clock_check_if_walking = GameClock(
            self, interval=0.2,
            event=self.check_if_walking
        )
        self.clocks.append(self.clock_check_if_walking)
        self.clock_check_if_walking.start()

    def get_order_from_chef(self, snack: object) -> None:
        '''Obtiene un snack'''
        self._object_state[2] = 'snack'
        self.current_order = snack
        self.update_object()

    def give_order_to_client(self) -> object:
        '''Entrega un snack'''
        snack = self.current_order
        self._object_state[2] = 'free'
        self.update_object()
        self.current_order = None
        return snack

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
        height /= 2      # Se modifica el alto y la posición
        pos_y += height  # para crear un hitbox menor y más natural
        return (pos_x + width * self.hitbox_reduction / 2,
                pos_y + height * self.hitbox_reduction / 2,
                width * (1 - self.hitbox_reduction),
                height * (1 - self.hitbox_reduction))

    def move(self, pos: tuple) -> None:
        '''Mueve al jugador luego de probar que no colisionará en el core.'''
        self._x, self._y = pos
        self.update_object()
        self.core.signal_move_up.emit(self.display_info)
        self.walked = True

    def check_if_walking(self) -> None:
        '''Revisa si el jugador está caminando para cambiar su animación'''
        if self.walked:
            self.walked = False
            self.update_animation(3)
        else:
            self._object_state[3] = 'idle'
            self.update_object()


class Chef(GameObject):
    '''Preparan la comida'''
    initial_level = PARAMETROS['chef']['nivel inicial']

    def __init__(self, core: object, x: int, y: int):
        super().__init__(core, x, y, 4, 4, ['idle'])
        self._level = self.initial_level
        self._dishes = int()
        self.order = None
        self.cooking = False
        self.cook_clock = GameClock(self)  # Se define el cocinar

    @property
    def dishes(self):
        '''Platos preparados por el Chef'''
        return self._dishes

    @dishes.setter
    def dishes(self, value):
        self._dishes = value
        if value >= PARAMETROS['chef']['niveles'][self._level]['platos siguiente nivel']:
            self._level = PARAMETROS['chef']['niveles'][self._level]['siguiente nivel']
            print(f'El chef subió de nivel a {self._level} ({value})')

    @property
    def exp(self):
        '''Experiencia del chef'''
        return int(PARAMETROS['chef']['niveles'][self._level]['experiencia'])

    def stop_cooking(self) -> None:
        '''Termina todo lo que está haciendo. Llamado al terminar la ronda'''
        self.order = None
        self.cooking = False
        self.cook_clock.stop()
        self._object_state[1] = 'idle'
        self.update_object()

    def interact(self, player: object) -> None:
        '''Interación con jugadores'''
        if not self.cooking and not player.current_order:
            if self.order:
                player.get_order_from_chef(self.order)
                self.order = None
                self._object_state[1] = 'idle'
                self.update_object()
            elif player.orders:
                player.orders -= 1
                self.start_cooking()
                self.cooking = True

    def start_cooking(self) -> None:
        '''El chef prepara un plato'''
        animation_type = choice(['A', 'B'])
        self._animation_cicle = [f'cooking{animation_type}{i}' for i in range(3)]
        # Calculo del tiempo de preparación
        min_value = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['mínimo'])
        base = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['base'])
        fact = float(PARAMETROS['bocadillos']['calculos']['tiempo preparación']['factor'])
        total_time = max(min_value, base - self.core.cafe.rep - self.exp * fact)
        # Reloj de cocina
        cooking_animation_time = 0.2
        self.cook_clock = GameClock(
            self,
            interval=cooking_animation_time,
            rep=total_time//cooking_animation_time,
            event=lambda: self.update_animation(1),
            final_event=self.try_recipes
        )
        self.clocks.clear()
        self.clocks.append(self.cook_clock)
        self.cook_clock.start()

    def try_recipes(self) -> None:
        '''El chef prueba una receta, donde puede fallar'''
        alpha = float(PARAMETROS['chef']['probabilidad fallar']['factor'])
        beta = float(PARAMETROS['chef']['probabilidad fallar']['suma'])
        gamma = self.exp
        probability = (alpha)/(gamma + beta)
        if probability > random():
            self.start_cooking()  # Falló el pedido, inicia nuevamente
        else:
            self.finish_order()

    def finish_order(self) -> None:
        '''Termina la orden y la deja en su mesa'''
        self.clocks.remove(self.cook_clock)
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
        self.chair = Chair(core, self._x, self._y - self._cell_size)

    def add_customer(self, *args) -> object:
        '''Añade un cliente a la mesa y lo retorna'''
        self.free = False
        self.customer = Customer(self.core, *self.pos, self, *args)
        self.core.signal_stack_under.emit(self.customer.display_info, self.display_info)
        self.core.signal_stack_under.emit(self.chair.display_info, self.customer.display_info)
        return self.customer

    @property
    def hit_box(self) -> tuple:
        '''Overrite. Permite considada la silla como parte de la mesa'''
        width, height = self.size
        fact = self.hitbox_reduction
        return (self._x + width * fact / 2,
                (self._y - self._cell_size) + height * fact / 2,
                width * (1 - fact),
                (self._cell_size + height) * (1 - fact))

    def interact(self, player: object) -> None:
        '''Interactúa con el jugador'''
        if not self.free:
            if not self.customer.gave_order:
                player.orders += 1
                self.customer.gave_order = True
            if player.current_order:
                self.customer.get_order(player.give_order_to_client())


class Chair(GameObject):
    '''Silla de los clientes'''
    def __init__(self, core: object, x: int, y: int):
        super().__init__(core, x, y, 1, 1, [])


class Customer(GameObject):
    '''Cliente. Es asignado a una mesa aleatoria'''
    def __init__(self, core: object, x: int, y: int, table, customer_type: str,
                 customer_name: str, wait_time: int, influence: int = 0):
        super().__init__(core, x, y - self._cell_size * 1.5, 1, 2,
                         [customer_type, customer_name, '1'])
        self.initial_time = time()
        self.table = table
        self.gave_order = False
        self.received_order = False
        self.influence = influence
        self._animation_cicle = ['0', '1', '2']
        self.wait_clock = GameClock(
            self, rep=3, interval=wait_time/3,
            event=lambda: self.update_animation(3),
            final_event=self.exit_cafe
        )
        self.happy_clock = GameClock(
            self, rep=1,
            final_event=self.exit_cafe
        )
        self.clocks.append(self.wait_clock)
        self.clocks.append(self.happy_clock)
        self.wait_clock.start()

    def exit_cafe(self) -> None:
        '''Cliente se retira de la mesa'''
        if self.received_order:
            self.core.cafe.completed_orders += 1
        else:
            self.core.cafe.failed_orders += 1
        self.core.cafe.rep += self.influence * (2 * self.received_order - 1)
        self.table.free = True
        self.delete_object()
        self.wait_clock.stop()  # En el caso que no se paró
        self.clocks.clear()
        self.core.update_ui_information()
        self.table.customer = None  # Elimina la referencia en la mesa

    def get_order(self, snack: object) -> None:
        '''El cliente recibe el bocadillo del jugador'''
        self.received_order = True
        prob_tip = snack.quality(time() - self.initial_time)
        del snack  # Se come el snack
        payment = int(PARAMETROS['bocadillos']['precio'])
        if prob_tip > random():
            payment += int(PARAMETROS['clientes']['propina'])
        self.core.cafe.money += payment
        self.wait_clock.stop()
        self.happy_clock.start()
        self._animation_cicle = ['H']
        self.update_animation(3)
