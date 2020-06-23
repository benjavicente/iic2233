'''Módulo que administra la lógica del juego'''

class Player:
    'Jugador'
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.name}>'

    def __eq__(self, other_name):
        return self.name == other_name



class Game:
    'Clase que controla la lógica del juego'
    def __init__(self, **kwards):
        self.__players = []
        self.__max_players = kwards['jugadores_partida']
        self.started = False

    def valid_name(self, name: str):
        'Ve si el nombre es valido'
        if name in self.__players:
            return False
        return True

    def add_player(self, name: str):
        'Añade un jugador en la sala de espera'
        self.__players.append(Player(name))
        if len(self.__players) == self.__max_players:
            self.start_game()

    def remove_player(self, name: str):
        'Elimina un jugador en la sala de espera'
        self.__players.remove(name)

    def start_game(self):
        'Empieza el juego'
        self.started = True

    def get_player_names(self):  # Property?
        'Retorna una lista de los nombres para la sala de espera'
        names = [player.name for player in self.__players]
        names.extend(['~~~' for _ in range(self.__max_players - len(self.__players))])
        return names
