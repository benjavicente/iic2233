import pickle


# ETAPA DE CARGA #
class EquipoDocencia:
    def __init__(self):
        self.ayudantes_normales = []
        self.ayudante_jefe = None

    # Aquí se filtra la lista del objeto al deserializarlo
    def __setstate__(self, estado):
        # Completar
        self.__dict__ = estado
        for ayudante in self.ayudantes_normales:
            if ayudante.cargo == 'Jefe':
                self.ayudantes_normales.remove(ayudante)
                self.ayudante_jefe = ayudante
                break


# Aquí se carga la instancia de EquipoDocencia
def cargar_instancia(ruta):
    with open(ruta, 'rb') as file:
        return pickle.load(file)


# ETAPA DE GUARDADO #
class Ayudante:
    def __init__(self, cargo, usuario_github, pokemon_favorito, pizza_favorita):
        self.cargo = cargo
        self.usuario_github = usuario_github
        self.pokemon_favorito = pokemon_favorito
        self.pizza_favorita = pizza_favorita

    def __repr__(self):
        return f"¡Hola! soy {self.usuario_github} y tengo el cargo de {self.cargo}"


class AyudanteJefe(Ayudante):
    def __init__(self, cargo, usuario_github, pokemon_favorito, pizza_favorita, trabajo_restante, experto, carrera):
        super().__init__(cargo, usuario_github, pokemon_favorito, pizza_favorita)
        self.trabajo_restante = trabajo_restante
        self.experto = experto
        self.carrera = carrera

    # Aquí se definen cambios que sólo se afectan a AyudanteJefe
    def __getstate__(self):
        state = self.__dict__.copy()
        state.update({
            'pizza_favorita': None,
            'trabajo_restante': 'Nada',
            'experto': 'TortugaNinja'
        })
        return state

# Aquí se guarda instancia de EquipoDocencia
def guardar_instancia(ruta, instancia_equipo_docencia):
    with open(ruta, 'wb') as file:
        pickle.dump(instancia_equipo_docencia, file)
    return True
