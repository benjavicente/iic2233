'Módulo que administra la lógica del juego'

from collections import deque
from generador_de_mazos import sacar_cartas as get_cards

class Player:
    'Jugador'
    def __init__(self, name: str, id_: int):
        self.name = name
        self.id = id_
        self.uno = False
        self.cards = []
        self.cards_to_steal = 0  # Esto debe cambiar a medida que se tomen ciertas acciones
        self.playing = True
        self.color_change_index = 0

    def __repr__(self):
        return f'<{self.name}>'

    def __eq__(self, other_name):
        return self.name == other_name



class Game:
    'Clase que controla la lógica del juego'
    def __init__(self, **kwards):
        # Parametros de configuración y preparación
        self.__players = []
        self.theme = kwards['tema_inicial']  #! Esto es por cada jugador
        self.__game_config = {
            'players': kwards['jugadores_partida'],
            'int_cards': kwards['cartas_iniciales'],
            'max_cards': kwards['maximo_cartas'],
            'penalty_correct': kwards['penalización_uno_correcto'],
            'penalty_incorrect': kwards['penalización_uno_incorrecto']
        }
        self.set_game()

    def set_game(self):
        'Establece el juego con los parámetros iniciales'
        # Parámetros del juego
        self.__players = []
        self.started = False
        self.pool = (None, None)
        self._clockwise = False
        self._plus_2_count = 0
        self.__requesting_color = False
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
        else:
            for player in filter(lambda p: p == name, self.__players):
                if player is self.waiting_to:
                    self._player_rotation()
                player.playing = False


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
        while not self.pool[1]:
            self.pool = get_cards(1)[0] # Como solo es una carta, se obtiene con [0]
        for player in self.__players:
            player.cards = get_cards(self.__game_config['int_cards'])
        for i in range(self.__game_config['int_cards']):
            for player in self.__players:
                self.__cards_to_add.append((player, player.cards[i]))

    def play(self, player_name: str, index: int) -> str:
        '''
        El jugador juega la carta `index` de su mazo.
        Retorna un string con lo que pasó en la jugada.
        Si el index es -1 se roba una carta.
        En el caso que un jugador ganó porque los demás quedaron con
        muchas cartas, se retorna el nombre con un espacio al inicio.
        '''  #* Esto es un desastre
        # -> REGLAS
        # Una carta con igual color o número puede ser añadida al pozo
        # +2: el siguiente jugador tiene que robar +2 o tirar un +2
        # Cambio de sentido: cambia el sentido
        # Cambio de color: el jugador cambia el color del poso
        #! robar es voluntario
        # Se ve si el jugador ganó por falta de jugadores
        if len(list(filter(lambda p: p.playing, self.__players))) <= 1:
            return 'win'
        # Se ven las condiciones de juego
        if self.waiting_to == player_name and not self.__requesting_color:
            # Roba
            if index == -1:
                if self._plus_2_count:
                    # Se añaden las cartas a robar si decidió robar en (+2)
                    self.waiting_to.cards_to_steal = self._plus_2_count
                    self._plus_2_count = 0
                # Obtiene la carta del mazo
                new_card = get_cards(1)[0]
                self.waiting_to.cards.append(new_card)
                self.__cards_to_add.append((self.waiting_to, new_card))
                # Ver si el jugador perdió
                if len(self.waiting_to.cards) > self.__game_config['max_cards']:
                    self.waiting_to.playing = False
                    self._player_rotation()
                    #! chequear si queda solo un jugador
                    remaining = list(filter(lambda p: p.playing, self.__players))
                    if len(remaining) == 1:
                        # Se añade el espacio para que sea imposible que el nombre
                        # sea uno de los comandos que se mandan (demasiado parche)
                        self.set_game()
                        return ' ' + remaining[0].name
                    return 'lose'
                if self.waiting_to.cards_to_steal:
                    # No se avanza el juego, necesita robar más
                    self.waiting_to.cards_to_steal -= 1
                    if not self.waiting_to.cards_to_steal:
                        # Se termina de robar
                        self._player_rotation()
                else:
                    self._player_rotation()
                return 'draw'
            # Juega un carta
            selected = self.waiting_to.cards[index]
            print(selected)
            if self.is_valid_card(selected) and not self.waiting_to.cards_to_steal:
                # Se elimina la carta
                self.waiting_to.cards.pop(index)
                # Se establece que el jugador no ha dicho uno
                self.waiting_to.uno = False
                # Se cambia la carta del pozo
                self.pool = selected
                # Ve si es de cambio de color:
                if selected[0] == 'color':
                    self.waiting_to.color_change_index = index
                    self.__requesting_color = True
                    return 'request_color'
                # Ve si es cambio de sentido
                if selected[0] == 'sentido':
                    self._clockwise = not self._clockwise
                # Ve si es +2
                if selected[0] == '+2':
                    self._plus_2_count += 2
                # Ve si el jugador ganó
                if not self.waiting_to.cards:
                    self.set_game()
                    return 'win'
                # Se cambia el jugador
                self._player_rotation()
                return 'play'
        return ''

    def receive_color(self, color: str) -> int:
        'Recibe el color pedido'
        if self.__requesting_color:
            self.pool = ('', color)
            index = self.waiting_to.color_change_index
            self.__requesting_color = False
            self._player_rotation()
            return index


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

    def is_valid_card(self, card: tuple) -> bool:
        'Ve si la carta seleccionada es válida'
        has_valid_color = card[1] == self.pool[1]
        has_valid_type = card[0] == self.pool[0]
        played_plus_2_before = bool(self._plus_2_count)
        return (
            ((has_valid_color or has_valid_type)
             and (not played_plus_2_before or card[0] == '+2'))
            or (card[0] == 'color' and not played_plus_2_before)
        )

    def cards_to_add(self) -> tuple:
        'Generador de las cartas que se tienen que añadir en el interfaz'
        while self.__cards_to_add:
            player, card = self.__cards_to_add.popleft()
            yield player.name, card

    def _player_rotation(self) -> None:
        'Cambia de turno' # Generador?
        last_player = self.waiting_to
        while not self.waiting_to.playing or last_player is self.waiting_to:
            index = self.__players.index(self.waiting_to)
            direction = -1 if self._clockwise else 1
            new_index = (index + direction) % len(self.__players)
            self.waiting_to = self.__players[new_index]

    def call_uno(self, player_name: str) -> None:
        'El jugador `name` llamó uno'
        correct = False
        # Se verifica si existe un jugador con una carta
        for player in self.__players:
            if player == player_name:
                if not player.playing:
                    return  # El jugador no esta jugando...
                # Si es que existe y es el mismo jugador, no se hace nada
                player.uno = True
                player_pointer = player
            else:
                if not player.uno and len(player.cards) == 1:
                    # Si es que existe, se penaliza
                    correct = True
                    player.cards_to_steal = self.__game_config['penalty_correct']
        # Si es que no existe, el jugador `name` roba cartas
        if not correct:
            player_pointer.cards_to_steal = self.__game_config['penalty_incorrect']
