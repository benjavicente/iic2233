class Actividad:
    def __init__(self, nombre, felicidad, estres):
        self.nombre = nombre
        self.felicidad = felicidad
        self.estres = estres

    def __str__(self):
        return f"{type(self).__name__} - {self.nombre} - "\
               f"Felicidad: {self.felicidad} - Estres: {self.estres}"

    def __repr__(self):
        # Por la representación pedida al ejecutar cargar.py
        return f"'Objeto {type(self).__name__} con nombre {self.nombre}"\
               f", felicidad {self.felicidad} y estres {self.estres}'"


class Hobby(Actividad):
    def __init__(self, nombre, felicidad, estres):
        super().__init__(nombre, felicidad, estres)


class Deber(Actividad):
    def __init__(self, nombre, felicidad, estres):
        super().__init__(nombre, felicidad, estres)
