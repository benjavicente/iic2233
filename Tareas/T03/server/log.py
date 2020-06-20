'''Módulo que maneja los logs del servidor'''

class Log:
    '''Clase que administra los logs'''
    size_entity = 15
    size_event = 20
    size_details = 60
    print_kwargs = {}

    def __init__(self):
        print('Iniciando log')
        title = (
            ' ' + 'Entidad'.ljust(self.size_entity)
            + '│ ' + 'Evento'.ljust(self.size_event)
            + '│ ' + 'Detalles'.ljust(self.size_details)
        )
        h_bar = (
            '═' * self.size_entity + '═╪'
            + '═' * self.size_event + '═╪'
            + '═' * self.size_details
        )
        print(title, h_bar, sep='\n', **self.print_kwargs)

    def add(self, event: str, entity: str = 'server', details: str = '') -> None:
        '''
        Muestra en la consola información
        acciones registradas por el servidor
        '''
        mesage = (
            ' ' + entity.ljust(self.size_entity)
            + '│ ' + event.ljust(self.size_event)
            + '│ ' + details.ljust(self.size_details)
        )
        print(mesage, **self.print_kwargs)
