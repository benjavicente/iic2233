import datetime

# https://docs.python.org/3.7/library/datetime.html#datetime.date.today
x = str(datetime.date.today()).replace("-", "/")
print(x)


class PrograPost:
    def __init__(self, usuario, fecha_emision, mensaje):
        self.usuario = usuario
        self.fecha_emision = fecha_emision
        self.mensaje = mensaje


