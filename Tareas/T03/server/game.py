'''Módulo que administra la lógica del juego'''

from generador_de_mazos import sacar_cartas as get_cards
from pprint import pprint


class Player:
    'Jugador'
    def __init__(self, name):
        self.name = name
        self.cards = []

    def __repr__(self):
        return f'<{self.name}>'

    def __eq__(self, other_name):
        return self.name == other_name



class Game:
    'Clase que controla la lógica del juego'
    def __init__(self, **kwards):
        # Parametros de configuración y preparación
        self.__players = []
        self.theme = kwards['tema']
        self.__max_players = kwards['jugadores_partida']
        self.__game_config = {
            'int_cards': kwards['cartas_iniciales'],
            'max_cards': kwards['maximo_cartas']
        }
        # Parámetros del juego
        self.started = False
        self.waiting_to = None
        self.pool = None

    def valid_name(self, name: str) -> True:
        'Ve si el nombre es valido'
        if name in self.__players:
            return False
        return True

    def add_player(self, name: str) -> None:
        'Añade un jugador en la sala de espera'
        if not self.started:
            self.__players.append(Player(name))
            if len(self.__players) == self.__max_players:
                self.start_game()

    def remove_player(self, name: str) -> None:
        'Elimina un jugador en la sala de espera (si es que existe)'
        if not self.started:
            if name in self.__players:
                self.__players.remove(name)

    def get_player_names(self) -> None:  # Property?
        'Retorna una lista de los nombres para la sala de espera'
        # Se extiende la lista para que se entrega una cantidad constante
        names = [player.name for player in self.__players]
        names.extend(['' for _ in range(self.__max_players - len(self.__players))])
        return names

    def start_game(self) -> None:
        'Empieza el juego'
        self.started = True
        self.waiting_to = self.__players[0]
        self.pool = get_cards(1)[0] # Como solo es una carta, se obtiene con [0]
        for player in self.__players:
            player.cards = get_cards(self.__game_config['int_cards'])

    def play(self, player_name: str, index: int) -> None:
        'El jugador juega la carta `index` de su mazo'
        # TODO
        if self.waiting_to == player_name:
            selected = self.waiting_to.cards[index]

    def set_up(self, player_name: str) -> dict:
        '''
        Retorna toda la información que necesita el
        cliente para iniciar su interfaz de juego
        '''
        # TODO:  Tengo que buscar una manera de cumplir lo del enunciado
        # TODO:  (mandar cartas como tipo-numero-imagen) a la vez que mando
        # TODO:  toda la información del juego (jugador actual, cantidad
        # TODO:  de cartas de jugadores, reverse de las carats, entre otros).
        # TODO:  Se debe realizar el procedimiento del enunciado CADA VEZ.
        # ╔═════════════════════╗  - EL jugador `name` esta abajo
        # ║ dcc    2(3°)    act ║  - Los jugadores son sentados en sentido antihorario
        # ║                     ║  - Los jugadores son rellenados en sentido horario
        # ║ 3(1°)   █ █   1(  ) ║  - El orden de jugadores es antihorario
        # ║                     ║  - Solo al jugador `name` se le envían las cartas, para
        # ║ chat   0(2°)   uno! ║  el resto de los jugadores se envía la cantidad de cartas
        # ╚═════════════════════╝  - Se envía información adicional  (jugador y color actual)
        data = {
            'active_color': self.pool[1],
            'active_player': self.waiting_to.name
        }
        # Se busca el índice del jugador (n ->> n+1)
        index = 0
        while self.__players[index] != player_name:
            index += 1
        data['0'] = {
            'name': player_name,
            'n_cards': len(self.__players[index].cards)
        }
        # Se van guardando los demás (n <<- n+1)
        remaining = self.__max_players - 1
        position = 3
        while remaining:
            index = (index - 1) % self.__max_players
            data[str(position)] = {
                'name': self.__players[index].name,
                'n_cards': len(self.__players[index].cards)
            }
            position -= 1
            remaining -= 1
        pprint(data)
        return data
