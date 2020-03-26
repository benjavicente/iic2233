class Estudiante:
    # Debes completar el constructor de la clase estudiante
    def __init__(self, username, hobbies, deberes):
        self.username = username
        self.hobbies = hobbies
        self.deberes = deberes
        self.rango_felicidad = tuple()
        self.rango_estres = tuple()

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad}")
        print(f"El nivel de estres del estudiante es {self.estres}\
             y el de felicidad {self.felicidad}")

    # Debes rellenar las property felicidad
    @property
    def felicidad(self):
        return self._felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        if nueva_felicidad < self.rango_felicidad[0]:
            # El valor es menor al premitido
            self._felicidad = self.rango_felicidad[0]
        elif nueva_felicidad > self.rango_felicidad[1]:
            # El valor es mayor al permitido
            self._felicidad = self.rango_felicidad[1]
        # Valor en el rango
        self._felicidad = nueva_felicidad

    # Debes rellenar las property estres
    @property
    def estres(self):
        return self._estres

    @estres.setter
    def estres(self, nuevo_estres):
        if nuevo_estres < self.rango_estres[0]:
            # El valor es menor al premitido
            self._estres = self.rango_estres[0]
        elif nuevo_estres > self.rango_estres[1]:
            # El valor es mayor al permitido
            self._estres = self.rango_estres[1]
        # Valor en el rango
        self._estres = nuevo_estres


######## REVISAR LOS PARAMETROS
class Alumno(Estudiante):
    def __init__(self, username, hobbies, deberes):
        # Recuerda iniciar la clase, de manera que herede de Estudiante
        # Definir rangos para alumno
        # Borrar pass cuando lo tengas listo
        super().__init__(username, hobbies, deberes)
        self.rango_felicidad = (0, 200)
        self.rango_estres = (0, 100)
        self._felicidad = 75
        self._estres = 25

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad}")
        # Debes rellenar esto, para que se ajusten los niveles de felicidad y estres
        self._felicidad += actividad.felicidad * 1.5
        self._estres += actividad.estres
        # Hasta acá
        print(f"El nivel de estres del estudiante es {self.estres}\
             y el de felicidad {self.felicidad}")


######## REVISAR LOS PARAMETROS
class Ayudante(Estudiante):
    def __init__(self, username, hobbies, deberes):
        # Recuerda iniciar la clase, de manera que herede de Estudiante
        # Definir rangos para Ayudante
        # Borrar pass cuando lo tengas listo
        super().__init__(username, hobbies, deberes)
        self.rango_felicidad = (0, 100)
        self.rango_estres = (0, 200)
        self._felicidad = 25
        self._estres = 75

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad}")
        # Debes rellenar esto, para que se ajusten los niveles de felicidad y estres
        self._felicidad = actividad.felicidad
        self._estres = actividad.estres * 2
        # Hasta acá
        print(f"El nivel de estres del ayudante es {self.estres}\
             y el de felicidad {self.felicidad}")
