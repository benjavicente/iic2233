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
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        if nueva_felicidad < self.rango_felicidad[0]:
            # El valor es menor al premitido
            self.__felicidad = self.rango_felicidad[0]
        elif nueva_felicidad > self.rango_felicidad[1]:
            # El valor es mayor al permitido
            self.__felicidad = self.rango_felicidad[1]
        # Valor en el rango
        self.__felicidad = nueva_felicidad

    # Debes rellenar las property estres
    @property
    def estres(self):
        return self.__estres

    @estres.setter
    def estres(self, nuevo_estres):
        if nuevo_estres < self.rango_estres[0]:
            # El valor es menor al premitido
            self.__estres = self.rango_estres[0]
        elif nuevo_estres > self.rango_estres[1]:
            # El valor es mayor al permitido
            self.__estres = self.rango_estres[1]
        # Valor en el rango
        self.__estres = nuevo_estres


######## REVISAR LOS PARAMETROS
class Alumno(Estudiante):
    def __init__(self, username, hobbies, deberes):
        # Recuerda iniciar la clase, de manera que herede de Estudiante
        # Definir rangos para alumno
        # Borrar pass cuando lo tengas listo
        super().__init__(username, hobbies, deberes)
        self.rango_felicidad = (0, 200)
        self.rango_estres = (0,100) 
        self.__felicidad = 75
        self.__estres = 25

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad}")
        # Debes rellenar esto, para que se ajusten los niveles de felicidad y estres
        self.__felicidad += actividad.felicidad * 1.5 
        self.__estres += actividad.estres
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
        self.__felicidad = 25
        self.__estres = 75
        pass

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad}")
        # Debes rellenar esto, para que se ajusten los niveles de felicidad y estres
        self.__felicidad = actividad.felicidad
        self.__estres = actividad.estres * 2
        # Hasta acá
        print(f"El nivel de estres del ayudante es {self.estres}\
             y el de felicidad {self.felicidad}")
