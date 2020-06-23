'Servidor'

from json import load
from server import Server


with open('parametros.json', encoding='utf-8') as file:
    PARAMETERS = load(file)

SERVER = Server(**PARAMETERS)

SERVER.run()

while True:
    pass
