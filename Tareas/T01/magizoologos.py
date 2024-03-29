from abc import ABC, abstractmethod
import random
import parametros as PMT
import alimentos as alm
import procesos as pc


def retornar_clase_magizoologo(tipo_magizoologo: str):
    """ Retorna la clase de el magizoólogo """
    tipo_magizoologo = tipo_magizoologo.lower()
    for a, b in zip("áéíúóñ", "aeioun"):
        tipo_magizoologo = tipo_magizoologo.replace(a, b)
    tipos = {
        "docencio": MagizoologoDocencio,
        "tareo": MagizoologoTareo,
        "hibrido": MagizoologoHibrido,
        "super": MagizoologoSuper,
    }
    if tipo_magizoologo in tipos:
        return tipos[tipo_magizoologo]


class Magizoologo(ABC):
    def __init__(self, nombre, criaturas,
                 sickles=None, alimentos=None,
                 licencia=None, nivel_magico=None, destreza=None,
                 energia_max=None, responsabilidad=None,
                 puede_usar_habilidad=None, **kwargs):
        # --- Valores únicos --- #
        self.nombre = str(nombre)
        self.tipo = type(self).__name__.replace("Magizoologo", "")
        # --- Valores de listad de objetos --- #
        if alimentos is None:  # Alimento al azar si se creo por primera vez
            alimento = random.choice((alm.BunueloGusarajo, alm.HigadoDragon, alm.BunueloGusarajo))
            alimentos = [alimento()]  # Si inicia el alimento y se guarda
        self.criaturas = criaturas  # Siempre debe existir una criatura
        self.alimentos = alimentos
        # --- Valores predeterminados en todos los Magizoólogos --- #
        if sickles is None:
            sickles = PMT.MAGIZOOLOGOS_SICKLES_INICIALES
        if licencia is None:
            licencia = PMT.MAGIZOOLOGOS_LICENCIA_INICIAL
        if puede_usar_habilidad is None:
            puede_usar_habilidad = PMT.MAGIZOOLOGOS_HABILIDADES
        if "nivel_aprobacion" in kwargs:  # Esto solo es verdadero si se crea un SuperMagizoólogo
            self.__nivel_aprobacion = kwargs["nivel_aprobacion"]  # el cual conserva este atributo
        else:
            self.__nivel_aprobacion = int(PMT.DCC_APROBACION) * bool(licencia)
        self.__sickles = int(sickles)
        self.licencia = str(licencia).capitalize() == "True"
        self.puede_usar_habilidad = str(puede_usar_habilidad).capitalize() == "True"
        # --- Valores predeterminados en distintos Magizoólogos --- #
        self.nivel_magico = int(nivel_magico)
        self.destreza = int(destreza)
        self.energia_max = int(energia_max)
        self.responsabilidad = int(responsabilidad)
        # --- Valores dependientes -- #
        self.__energia_actual = self.energia_max

    def __str__(self):
        return self.nombre

    def __repr__(self):
        return f"{self.nombre} {id(self)}"

    def __eq__(self, value):
        if type(value) is str:
            value = value.lower()
        return self.nombre.lower() == value

    @property
    def energia_actual(self):
        return self.__energia_actual

    @energia_actual.setter
    def energia_actual(self, value):
        self.__energia_actual = min(self.energia_max, max(PMT.MAGIZOOLOGOS_ENERGIA_MINIMA, value))

    @property
    def nivel_aprobacion(self):
        return self.__nivel_aprobacion

    @nivel_aprobacion.setter
    def nivel_aprobacion(self, value):
        min_aprob, max_aprob = PMT.MAGIZOOLOGOS_RANGO_APROBACION
        self.__nivel_aprobacion = min(max_aprob, max(min_aprob, value))

    @property
    def sickles(self):
        return self.__sickles

    @sickles.setter
    def sickles(self, value):
        self.__sickles = max(0, value)

    def obtener_dccriatura(self, nombre_criatura: str) -> object:
        """Retorna la DCCriatura a partir del nombre"""
        return self.criaturas[self.criaturas.index(nombre_criatura)]

    def adoptar_dccriatura(self, criatura) -> None:
        # Método llamado en dcc.vernder_criaturas,
        # el cual es encargado del proceso de adoptar
        self.criaturas.append(criatura)

    def comprar_alimentos(self, alimento) -> None:
        # Método llamado en dcc.vernder_alimentos,
        # el cual es encargado del proceso de comprar
        self.alimentos.append(alimento)

    def sanar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta sanar a alguna de sus DCCriaturas.
        Su coste energético es de 8 puntos.
        Retorna None si no se pudo sanar, la criatura en casi contrario.
        """
        # --- Verificación --- #
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_CURAR:
            print("No suficiente tienes energía")
            return  # Salir por falta de energía
        # Lista de criaturas enfermas
        criaturas_enfermas = list()
        for c in self.criaturas:
            if c.enferma:
                criaturas_enfermas.append(c)
        if not criaturas_enfermas:
            print("No hay criaturas enfermas :)")
            return  # Salir por falta de criaturas enfermas
        # Formateo de lista a str
        criaturas_a_sanar = "\n".join(map(lambda x: " - " + str(x), criaturas_enfermas))
        # Proceso multipaso --> Retorna un str o False
        criatura_elegida = pc.proceso_multipaso(
            (f"Elige una criatura a recuperar \n{criaturas_a_sanar}", (
                ("Tienes a la criatura",
                 lambda x: x in self.criaturas),
                ("La criatura se está enferma",
                 lambda x: (x in criaturas_enfermas) == (x in self.criaturas)),
            ), ),
        )
        if criatura_elegida:
            criatura_elegida = criatura_elegida[0]  # De lista a str
            # --- Tratar de curar --- #
            self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_CURAR  # Perdida de energía
            c = self.obtener_dccriatura(criatura_elegida)  # Se obtiene la criatura
            print(f"Has tratado de sanar a {c}...")
            valor = ((self.nivel_magico - c.vida_actual)
                     / (self.nivel_magico + c.vida_max))
            prob = min(1, max(0, valor))  # Formula
            if prob >= random.random():
                c.enferma = False
                print(f"Has sanado a {c}!")
            else:
                print(f"No has podido sanar a {c} :(")

    @abstractmethod
    def alimentar_dccriatura(self):
        """
        El Magizoólogo puede decidir alimentar a una de sus DCCriaturas con
        alguno de sus alimentos, siempre y cuando posea alguno.
        En respuesta a esto, la DCCriatura puede atacar a su dueño.
        El costo energético de alimentar es de 5 puntos.

        Retorna None si no se pudo alimentar,
        un objecto de clase DCCriatura en el caso contrario.
        """
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_ALIMENTAR:  # No se cumple por energía
            print("No suficiente tienes energía")
            return  # Sale
        elif not self.alimentos:  # No se cumple por alimentos
            print("No tienes alimentos!")
            return  # Sale
        while True:
            print("Elige una criatura que quieres alimentar")
            for criatura in self.criaturas:
                print(f" - {criatura}: {criatura.nivel_hambre}, "
                      f"{criatura.vida_actual}/{criatura.vida_max}HP")
            nombre_criatura = input("--> ").strip()
            if nombre_criatura not in self.criaturas:
                if pc.volver_a_intentarlo(nombre_criatura, "Posees esa criatura"):
                    continue  # Volver a pedir la criatura
                return  # Salir si no volvió en la linea anterior
            while True:
                print("Elige un alimento! Asegurate de escribirlo bien!")
                print(*set(map(lambda x: f" - {x}: +{x.pnt_vida}HP", self.alimentos)), sep="\n")
                alimento_elegido = input("--> ").strip()
                for alimento in self.alimentos:
                    if str(alimento).lower() == alimento_elegido.lower():
                        # --- Alimenar --- #
                        c = self.obtener_dccriatura(nombre_criatura)  # Criatura a alimentar
                        print(f"Has tratado de alimentar a {c}\ncon un {alimento}...")
                        self.alimentos.remove(alimento)  # Eliminar alimento
                        self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_ALIMENTAR
                        c.alimentarse(alimento, self)  # Se dirige a DCCriatura
                        return c
                if not pc.volver_a_intentarlo(alimento_elegido, "Posees el alimento"):
                    return

    @abstractmethod
    def recuperar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta recuperar una de sus DCCriaturas.
        El coste energético de intentar recuperar una criatura es de 10 puntos.
        Retorna None si no se pudo recuperar, la criatura en casi contrario.
        """
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_RECUPERAR:
            print("No suficiente tienes energía")
            return
        # Lista de criaturas escapadas
        criaturas_escapadas = [c for c in self.criaturas if c.escapado]
        if not criaturas_escapadas:
            print("No hay criaturas escapadas :)")
            return
        # Formateo de lista a str
        criaturas_a_recuperar =\
            "\n".join(map(lambda x: " - " + str(x), criaturas_escapadas))
        # Proceso multipaso --> Retorna un str o False
        criatura_elegida = pc.proceso_multipaso(
            (f"Elige una criatura a recuperar \n{criaturas_a_recuperar}", (
                ("Tienes a la criatura",
                    lambda x: x in self.criaturas),
                ("La criatura se ha escapado",
                    lambda x: (x in criaturas_escapadas) == (x in self.criaturas)),
            ), ),
        )
        if criatura_elegida:
            criatura_elegida = criatura_elegida[0]  # Lista a str
            # Perdida de energía
            self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_RECUPERAR
            # -- Tratar de recuperar -- #
            c = self.obtener_dccriatura(criatura_elegida)  # Se obtiene la criatura
            print(f"Has tratado de recuperar a {c}...")
            valor = ((self.destreza + self.nivel_magico - c.nivel_magico)
                     / (self.destreza + self.nivel_magico + c.nivel_magico))
            prob = min(1, max(0, valor))  # Formula
            if prob >= random.random():
                c.escapado = False
                print(f"Has recuperado a {c}!")
                return c  # Retorna la criatura para aplicar efectos pasivos
            else:
                print(f"No has podido recuperar a {c} :(")
                return

    @abstractmethod
    def habilidad_especial(self):
        if self.puede_usar_habilidad:
            if self.energia_actual >= PMT.MAGIZOOLOGOS_COSTO_HABILIDAD:
                print("Has utilizado tu habilidad especial!")
                self.puede_usar_habilidad = False
                self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_HABILIDAD
                return True
            else:
                print("No tienes energía suficiente")
        else:
            print("Ya has usado la habilidad!")
        return False

###################################
# --- Inicio Clases heredadas --- #
###################################


class MagizoologoDocencio(Magizoologo):
    def __init__(self, nombre, **kwargs):
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.DOCENCIO_RANGO_NIVEL_MAGICO)
        if "destreza" not in kwargs:
            kwargs["destreza"] = random.randint(*PMT.DOCENCIO_RANGO_DESTREZA)
        if "energia_max" not in kwargs:
            kwargs["energia_max"] = random.randint(*PMT.DOCENCIO_RANGO_ENERGIA_MAX)
        if "responsabilidad" not in kwargs:
            kwargs["responsabilidad"] = random.randint(*PMT.DOCENCIO_RANGO_RESPONSABILIDAD)
        super().__init__(nombre, **kwargs)

    def alimentar_dccriatura(self) -> None:
        # Habilidad pasiva: Sana a sus criaturas al alimentarlas
        criatura = super().alimentar_dccriatura()
        if criatura and criatura.vida_actual < criatura.vida_max:
            sanado = min(PMT.DOCENCIO_PASIVO_SANAR_VIDA, criatura.vida_max - criatura.vida_actual)
            print(f"Habilidad pasiva: Has sanado {sanado}pts de vida adicionales!")
            criatura.vida_actual += sanado

    def recuperar_dccriatura(self) -> None:
        # Habilidad pasiva: Hiere a sus criaturas al recuperarlas
        criatura_recuperada = super().recuperar_dccriatura()
        if criatura_recuperada:
            criatura_recuperada.vida_actual -= PMT.DOCENCIO_PASIVO_MERMAN

    def habilidad_especial(self) -> None:
        # Habilidad especial: Saciar a todas sus criaturas
        if super().habilidad_especial():
            print("Has saciado el hambre de todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.dias_sin_comer = 0


class MagizoologoTareo(Magizoologo):
    def __init__(self, nombre, **kwargs):
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.TAREO_RANGO_NIVEL_MAGICO)
        if "destreza" not in kwargs:
            kwargs["destreza"] = random.randint(*PMT.TAREO_RANGO_DESTREZA)
        if "energia_max" not in kwargs:
            kwargs["energia_max"] = random.randint(*PMT.TAREO_RANGO_ENERGIA_MAX)
        if "responsabilidad" not in kwargs:
            kwargs["responsabilidad"] = random.randint(*PMT.TAREO_RANGO_RESPONSABILIDAD)
        super().__init__(nombre, **kwargs)

    def alimentar_dccriatura(self) -> None:
        # Habilidad pasiva: Posibilidad de sanar toda su vida
        criatura_alimentada = super().alimentar_dccriatura()
        if criatura_alimentada and PMT.TAREO_PASIVO_PROB_SANAR >= random.random():
            print("Habilidad pasiva: Has sanado toda su vida!")
            criatura_alimentada.vida_actual = criatura_alimentada.vida_max

    def recuperar_dccriatura(self) -> None:
        super().recuperar_dccriatura()

    def habilidad_especial(self) -> None:
        # Habilidad especial: Sanar a todas sus criaturas
        if super().habilidad_especial():
            print("Has recuperado todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.escapado = False


class MagizoologoHibrido(Magizoologo):
    def __init__(self, nombre, **kwargs):
        if "nivel_magico" not in kwargs:
            kwargs["nivel_magico"] = random.randint(*PMT.HIBRIDO_RANGO_NIVEL_MAGICO)
        if "destreza" not in kwargs:
            kwargs["destreza"] = random.randint(*PMT.HIBRIDO_RANGO_DESTREZA)
        if "energia_max" not in kwargs:
            kwargs["energia_max"] = random.randint(*PMT.HIBRIDO_RANGO_ENERGIA_MAX)
        if "responsabilidad" not in kwargs:
            kwargs["responsabilidad"] = random.randint(*PMT.HIBRIDO_RANGO_RESPONSABILIDAD)
        super().__init__(nombre, **kwargs)

    def alimentar_dccriatura(self) -> None:
        # Habilidad pasiva: Sana salud a sus criaturas al alimentarlas
        criatura = super().alimentar_dccriatura()
        if criatura and criatura.vida_actual < criatura.vida_max:
            sanado = min(PMT.HIBRIDO_PASIVO_SANAR_VIDA, criatura.vida_max - criatura.vida_actual)
            print(f"Habilidad pasiva: Has sanado {sanado}pts de vida adicionales!")
            criatura.vida_actual += sanado

    def recuperar_dccriatura(self) -> None:
        super().recuperar_dccriatura()

    def habilidad_especial(self) -> None:
        # Habilidad especial: Sana a todas sus criaturas
        if super().habilidad_especial():
            print("Has sanado a todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.enferma = False


class MagizoologoSuper(MagizoologoDocencio, MagizoologoTareo, MagizoologoHibrido):
    def __init__(self, **kwargs):
        kwargs["puede_usar_habilidad"] = True
        super().__init__(**kwargs)

    def alimentar_dccriatura(self) -> None:
        criatura_alimentada = super().alimentar_dccriatura()
        if criatura_alimentada:
            if PMT.TAREO_PASIVO_PROB_SANAR >= random.random():
                print("Habilidad pasiva: Has sanado toda su vida!")
                criatura_alimentada.vida_actual = criatura_alimentada.vida_max
            else:
                recuperar = max(PMT.DOCENCIO_PASIVO_SANAR_VIDA, PMT.HIBRIDO_PASIVO_SANAR_VIDA)
                print(f"Habilidad pasiva: Has sanado {recuperar}pts de vida adicionales!")
                criatura_alimentada.vida_actual += recuperar

    def recuperar_dccriatura(self) -> None:
        super().recuperar_dccriatura()

    def habilidad_especial(self) -> None:
        if self.puede_usar_habilidad:
            if self.energia_actual >= PMT.MAGIZOOLOGOS_COSTO_HABILIDAD:
                habilidades = (" - Docencio: Saciar a todas tus criaturas\n" +
                               " - Tareo: Recuperar a todas tus criaturas\n" +
                               " - Hibrido: Sanar a todas tus criaturas")
                cual = pc.proceso_multipaso(
                    (f"Elige una habilidad especial: \n{habilidades}", (
                        ("Es Docencio, Tareo o Hibrido",
                         lambda x: x.lower() in {"docencio", "tareo", "hibrido"}),
                    ), ),
                )
                if cual:
                    cual = cual[0].lower()
                    if cual == "docencio":
                        MagizoologoDocencio.habilidad_especial(self)
                    elif cual == "tareo":
                        MagizoologoTareo.habilidad_especial(self)
                    elif cual == "hibrido":
                        MagizoologoHibrido.habilidad_especial(self)
            else:
                print("No tienes energía para usar una habilidad")
        else:
            print("Ya usaste la habilidad!")
