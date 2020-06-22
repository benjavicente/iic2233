'''Módulo que maneja los logs del servidor'''

class Log:
    '''
    Clase que administra los logs
    '''
    size_entity = 15
    size_event = 25
    size_details = 60
    print_kwargs = {'flush': True}

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

    def __call__(self, event: str, entity: str = 'server', details: str = '') -> None:
        '''
        Muestra en la consola información
        acciones registradas por el servidor
        '''
        # TODO: ver si se puede usar format
        mesage = (
            ' ' + str(entity).ljust(self.size_entity)
            + '│ ' + str(event).ljust(self.size_event)
            + '│ ' + str(details).ljust(self.size_details)
        )
        print(mesage, **self.print_kwargs)
