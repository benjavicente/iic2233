'''Clase Café'''


from math import floor

from PyQt5.QtCore import QObject

from config.parametros import PARAMETROS


class Cafe(QObject):
    '''Café que se administra en el juego'''
    def __init__(self):
        super().__init__()
        self.money = int()
        self.__rep = int()
        self.round = 1
        self.open = True
        self._completed_orders = 0
        self._failed_orders = 0
        self.total_orders = 0

    @property
    def rep(self):
        '''Reputación del café'''
        return self.__rep

    @rep.setter
    def rep(self, value):
        # La reputación puede cambiar de 3 maneras distintas
        self.__rep = max(0, min(5, value))

    @property
    def completed_orders(self):
        '''Ordenes completadas'''
        return self._completed_orders

    @completed_orders.setter
    def completed_orders(self, value):
        self._completed_orders = value
        self.total_orders += 1

    @property
    def failed_orders(self):
        '''Ordenes fallidas'''
        return self._failed_orders

    @failed_orders.setter
    def failed_orders(self, value):
        self._failed_orders = value
        self.total_orders += 1

    @property
    def stats(self):
        '''Estadísticas del cafe'''
        return {
            'money': self.money,
            'rep': self.rep,
            'round': self.round,
            'open': 'Abierto' if self.open else 'Cerrado',
            'completed_orders': self.completed_orders,
            'total_orders': self.total_orders,
            'failed_orders': self.total_orders - self.completed_orders,
        }

    @property
    def round_clients(self):
        '''Clientes de la ronda'''
        alpha = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['factor'])
        beta = int(PARAMETROS['DCCafé']['calculos']['clientes por ronda']['base'])
        return alpha * (beta + self.round)

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

    def new_round_values(self) -> None:
        '''Reinicia los valores de la ronda'''
        self.open = True
        self._completed_orders = 0
        self._failed_orders = 0
        self.total_orders = 0
        self.round += 1
