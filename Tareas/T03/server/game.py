'''Módulo que administra la lógica del juego'''

from collections import deque
from generador_de_mazos import sacar_cartas as get_cards

class Player:
    'Jugador'
    def __init__(self, name: str, id_: int):
        self.name = name
        self.id = id_
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
        self.__game_config = {
            'players': kwards['jugadores_partida'],
            'int_cards': kwards['cartas_iniciales'],
            'max_cards': kwards['maximo_cartas']
        }
        # Parámetros del juego
        self.started = False
        self.waiting_to = None
        self.pool = None
        self._clockwise = False
        self._plus_2 = False  # TODO: cambiar esto y ver sus condiciones
        # Parámetros de flujo
        self.__cards_to_add = deque()

    def valid_name(self, name: str) -> True:
        'Ve si el nombre es valido'
        if name not in self.__players and name.isalnum():
            return True
        return False

    def add_player(self, name: str, id_: int) -> None:
        'Añade un jugador en la sala de espera'
        if not self.started:
            self.__players.append(Player(name, id_))
            if len(self.__players) == self.__game_config['players']:
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
        names.extend(['' for _ in range(self.__game_config['players'] - len(self.__players))])
        return names

    def start_game(self) -> None:
        'Empieza el juego'
        self.started = True
        self.waiting_to = self.__players[0]
        self.pool = get_cards(1)[0] # Como solo es una carta, se obtiene con [0]
        for player in self.__players:
            player.cards = get_cards(self.__game_config['int_cards'])
        for i in range(self.__game_config['int_cards']):
            for player in self.__players:
                self.__cards_to_add.append((player, player.cards[i]))

    def play(self, player_name: str, index: int) -> bool:
        '''
        El jugador juega la carta `index` de su mazo.
        Retorna true si se pudo jugar'.
        Si el index es -1 se roba una carta (TODO).
        '''
        # TODO: podria añadir un kwarg que indique el color si es que se está cambiando
        # -> REGLAS
        # Una carta con igual color o número puede ser añadida al pozo
        # TODO: +2: el siguiente jugador tiene que robar +2 o tirar un +2
        # Cambio de sentido: cambia el sentido
        # TODO: cambio de color: el jugador cambia el color del poso
        #! robar tiene que ser voluntario
        if self.waiting_to == player_name:  #* Aquí debe estar la condición del bonus
            selected = self.waiting_to.cards[index]
            if self.is_valid_card(selected):  # La carta es válida, se hacen cosas
                # Se elimina la carta
                self.waiting_to.cards.pop(index)
                # Robar cartas
                # Se cambia la carta del pozo
                self.pool = selected  # TODO: falta ver la carta color
                # Cambia el sentido
                if selected[0] == 'sentido':
                    self._clockwise = not self._clockwise
                elif selected[0] == '+2':
                    self._plus_2 = True
                # Se cambia el jugador
                self._player_rotation()
                return True
        return False

    def get_relative_players(self, player_name: str) -> str:
        'Ordena los jugadores según la vista del interfaz'
        # ╔═════════════════════╗  - EL jugador `name` esta abajo
        # ║ dcc    2(3°)    act ║  - Los jugadores son sentados en sentido antihorario
        # ║                     ║  - Los jugadores son rellenados en sentido horario
        # ║ 1(1°)   █ █   3(  ) ║  - El orden de jugadores es antihorario
        # ║                     ║  - Solo al jugador `name` se le envían las cartas, para
        # ║ chat   0(2°)   uno! ║  el resto de los jugadores se envía la cantidad de cartas
        # ╚═════════════════════╝  - Se envía información adicional  (jugador y color actual)
        player_list = list()
        # Se busca el índice del jugador (n ->> n+1)
        index = 0
        while self.__players[index] != player_name:
            index += 1
        player_list.append(self.__players[index])
        # Se van guardando los demás (n <<- n+1)
        position = 3
        for _ in range(self.__game_config['players'] - 1):
            index = (index - 1) % self.__game_config['players']
            player_list.append(self.__players[index])
            position -= 1
        return tuple(player_list)

    def set_up_names(self, player_name: str) -> dict:
        'Añade los jugadores al interfaz, con los nombres en orden'
        players = self.get_relative_players(player_name)
        return {str(i): ply.name for i, ply in enumerate(players)}

    def set_up_cards(self) -> dict:
        '''
        Prepara las catas el inicio del juego
        Entrega un diccionario con instrucciones para el servidor
        '''
        pass

    def is_valid_card(self, card: tuple):
        'Ve si la carta seleccionada es válida'
        return card[0] == self.pool[0] or card[1] == self.pool[1]

    def cards_to_add(self) -> dict:
        'Generador de las cartas que se tienen que añadir en el interfaz'
        while self.__cards_to_add:
            player, card = self.__cards_to_add.popleft()
            yield player.name, card

    def _player_rotation(self) -> None:
        'Cambia de turno'
        index = self.__players.index(self.waiting_to)
        direction = -1 if self._clockwise else 1
        new_index = (index + direction) % len(self.__players)
        self.waiting_to = self.__players[new_index]
