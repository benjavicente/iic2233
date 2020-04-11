"""
======================
Clases de Magizoologos
======================
Contiene las clases:
--------------------
    Magizoologo
    MagizoologoDocencio
    MagizoologoTareo
    MagizoologoHibrido
    MagizoologoSuper
Depende de:
-----------
    parametros
    alimentos
"""

from abc import ABC, abstractmethod
import random

import parametros as PMT
import alimentos as alm
import procesos as pc


def retornar_clase_magizoologo(tipo_magizoologo: str):
    """
    Retorna la clase de el magizoólogo
    """
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
    """
    ===========
    Magizoólogo
    ===========
    Son quienes se encargan de cuidar las DCCriaturas con el objetivo de preservar
    su existencia. Todo Magizoólogo puede y debe alimentar a sus DCCriaturas,
    capturarlas en caso de que escapen y sanarlas en caso de que enfermen.
    """
    def __init__(self,
                 nombre,
                 sickles=None,
                 criaturas=None,
                 alimentos=None,
                 licencia=None,
                 nivel_magico=None,
                 destreza=None,
                 energia_max=None,
                 responsabilidad=None,
                 puede_usar_habilidad=None,
                 **kwargs):
        # -------------- #
        # Valores únicos #
        # -------------- #
        self.nombre = str(nombre)
        self.tipo = type(self).__name__.replace("Magizoologo", "")
        # ---------------------------- #
        # Valores de listad de objetos #
        # ---------------------------- #
        if alimentos is None:
            alimento = random.choice((alm.BunueloGusarajo, alm.HigadoDragon, alm.BunueloGusarajo))
            alimentos = [alimento()]
        self.criaturas = criaturas
        self.alimentos = alimentos
        # ------------------------------------------------- #
        # Valores predeterminados en todos los Magizoólogos #
        # ------------------------------------------------- #
        if sickles is None:
            sickles = PMT.MAGIZOOLOGOS_SICKLES_INICIALES
        if licencia is None:
            licencia = PMT.MAGIZOOLOGOS_LICENCIA_INICIAL
        if puede_usar_habilidad is None:
            puede_usar_habilidad = PMT.MAGIZOOLOGOS_HABILIDADES
        if licencia:
            nivel_aprobacion = PMT.DCC_APROBACION
        else:
            nivel_aprobacion = 0
        # Transformación de valores
        self.__sickles = int(sickles)
        self.licencia = licencia == "True"
        self.puede_usar_habilidad = puede_usar_habilidad == "True"
        self.__nivel_aprobacion = int(nivel_aprobacion)
        # ------------------------------------------------- #
        # Valores predeterminados en distintos Magizoólogos #
        # ------------------------------------------------- #
        self.nivel_magico = int(nivel_magico)
        self.destreza = int(destreza)
        self.energia_max = int(energia_max)
        self.responsabilidad = int(responsabilidad)
        # -------------------- #
        # Valores dependientes #
        # -------------------- #
        self.__energia_actual = self.energia_max

    def __str__(self):
        return self.nombre

    def __eq__(self, value):
        if type(value) is str:
            value = value.lower()
        return self.nombre == value

    def __repr__(self):
        return f"{self.nombre} {id(self)}"

    @property
    def energia_actual(self):
        return self.__energia_actual

    @energia_actual.setter
    def energia_actual(self, value):
        if value > self.energia_max:
            self.__energia_actual = self.energia_max
        elif value < PMT.MAGIZOOLOGOS_ENERGIA_MINIMA:
            self.__energia_actual = PMT.MAGIZOOLOGOS_ENERGIA_MINIMA
        else:
            self.__energia_actual = value

    @property
    def nivel_aprobacion(self):
        return self.__nivel_aprobacion

    @nivel_aprobacion.setter
    def nivel_aprobacion(self, value):
        if value > 100:
            self.__nivel_aprobacion = 100
            pass  # Hacer Super Magizoólogo
        elif value < 0:
            self.__nivel_aprobacion = 0
        else:
            self.__nivel_aprobacion = value
        if self.__nivel_aprobacion < PMT.DCC_APROBACION and self.licencia:
            print("Perdiste tu licencia :(")
            self.licencia = False
        elif self.__nivel_aprobacion >= PMT.DCC_APROBACION and not self.licencia:
            print("Recuperaste tu licencia :)")
            self.licencia = True

    @property
    def sickles(self):
        return self.__sickles

    @sickles.setter
    def sickles(self, value):
        if value <= 0:
            self.__sickles = 0
        else:
            self.__sickles = int(value)

    def obtener_dccriatura(self, nombre_criatura):
        """Retorna la DCCriatura a partir del nombre"""
        return self.criaturas[self.criaturas.index(nombre_criatura)]

    def adoptar_dccriatura(self, criatura):
        # Método llamado en dcc.vernder_criaturas,
        # el cual es encargado del proceso de adoptar
        self.criaturas.append(criatura)

    def comprar_alimentos(self, alimento):
        # Método llamado en dcc.vernder_alimentos,
        # el cual es encargado del proceso de comprar
        self.alimentos.append(alimento)

    @abstractmethod
    def alimentar_dccriatura(self):
        """
        El Magizoólogo puede decidir alimentar a una de sus DCCriaturas con
        alguno de sus alimentos, siempre y cuando posea alguno.
        En respuesta a esto, la DCCriatura puede atacar a su dueño.
        El costo energético de alimentar es de 5 puntos.

        Retorna False si no se pudo alimentar,
        un objecto de clase DCCriatura en el caso contrario.
        """
        if not self.alimentos:
            print("No tienes alimentos!")
            return False
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_ALIMENTAR:
            print("No suficiente tienes energía")
            return False
        while True:
            print("Elige una criatura que quieres alimentar")
            for criatura in self.criaturas:
                print(f" - {criatura}: {criatura.nivel_hambre}")
            nombre_criatura = input("--> ").strip()
            if nombre_criatura not in self.criaturas:
                if pc.volver_a_intentarlo(nombre_criatura, "Posees esa criatura"):
                    continue
                else:
                    return False
            while True:
                print("Elige un alimento! Asegurate de escribirlo bien!")
                print(*set(map(lambda x: " - " + str(x), self.alimentos)), sep="\n")
                alimento_elegido = input("--> ").strip()
                for alimento in self.alimentos:
                    if str(alimento).lower() == alimento_elegido.lower():
                        ############################################
                        # Alimenar
                        c = self.obtener_dccriatura(nombre_criatura)
                        print(f"Has tratado de alimentar a {c} con un {alimento}...")
                        self.alimentos.remove(alimento)
                        self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_ALIMENTAR
                        # Se dirige al método en la clase DCCriatura
                        return c.alimentarse(alimento, self)
                if not pc.volver_a_intentarlo(alimento_elegido, "Posees el alimento"):
                    return False

    @abstractmethod
    def recuperar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta recuperar una de sus DCCriaturas.
        El coste energético de intentar recuperar una criatura es de 10 puntos.

        Retorna False si no se pudo recuperar, la criatura en casi contrario
        """
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_RECUPERAR:
            print("No suficiente tienes energía")
            return False
        # Lista de criaturas escapadas
        criaturas_escapadas = list()
        for c in self.criaturas:
            if c.escapado:
                criaturas_escapadas.append(c)
        if not criaturas_escapadas:
            print("No hay criaturas escapadas :)")
            return False
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
            ),),
        )[0]  # Esto es porque proceso multipaso retorna una lista
        if criatura_elegida:
            # Perdida de energía
            self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_RECUPERAR
            # -- Tratar de recuperar -- #
            # Se obtiene la criatura
            c = self.obtener_dccriatura(criatura_elegida)
            print(f"Has tratado de recuperar a {c}...")
            # Formula
            valor = ((self.destreza + self.nivel_magico - c.nivel_magico)
                     / (self.destreza + self.nivel_magico + c.nivel_magico))
            prob = min(1, max(0, valor))
            if prob >= random.random():
                c.escapado = False
                print(f"Has recuperado a {c}!")
                return c  # Retorna la criatura para aplicar efectos pasivos
            else:
                print(f"No has podido recuperar a {c} :(")
                return False

    def sanar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta sanar a alguna de sus DCCriaturas.
        Su coste energético es de 8 puntos.
        """
        if self.energia_actual < PMT.MAGIZOOLOGOS_COSTO_CURAR:
            print("No suficiente tienes energía")
            return False
        # Lista de criaturas enfermas
        criaturas_enfermas = list()
        for c in self.criaturas:
            if c.enferma:
                criaturas_enfermas.append(c)
        if not criaturas_enfermas:
            print("No hay criaturas enfermas :)")
            return False
        # Formateo de lista a str
        criaturas_a_sanar =\
            "\n".join(map(lambda x: " - " + str(x), criaturas_enfermas))
        # Proceso multipaso --> Retorna un str o False
        criatura_elegida = pc.proceso_multipaso(
            (f"Elige una criatura a recuperar \n{criaturas_a_sanar}", (
                ("Tienes a la criatura",
                 lambda x: x in self.criaturas),
                ("La criatura se ha escapado",
                 lambda x: (x in criaturas_enfermas) == (x in self.criaturas)),
            ), ),
        )[0]  # Esto es porque proceso multipaso retorna una lista
        if criatura_elegida:
            # Perdida de energía
            self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_CURAR
            # -- Tratar de curar -- #
            # Se obtiene la criatura
            c = self.obtener_dccriatura(criatura_elegida)
            print(f"Has tratado de sanar a {c}...")
            # Formula
            valor = ((self.nivel_magico - c.vida_actual)
                     / (self.nivel_magico - c.vida_actual))
            prob = min(1, max(0, valor))
            if prob >= random.random():
                c.enferma = False
                print(f"Has sanado a {c}!")
                return c    # Retorna la criatura para aplicar efectos pasivos
            else:
                print(f"No has podido sanar a {c} :(")

    @abstractmethod
    def habilidad_especial(self):
        if self.energia_actual >= PMT.MAGIZOOLOGOS_COSTO_HABILIDAD:
            if self.puede_usar_habilidad:
                print("Has utilizado tu habilidad especial!")
                self.puede_usar_habilidad = False
                self.energia_actual -= PMT.MAGIZOOLOGOS_COSTO_HABILIDAD
                return True
            else:
                print("Ya has usado la habilidad")
                return False
        else:
            print("No tienes energía suficiente")
            return False


# Inicio Clases heredadas

class MagizoologoDocencio(Magizoologo):
    """
    ======================
    Magizoólogos Docencios
    ======================

    Habilidad pasiva
    ----------------
    Los Magizoólogos Docencios tienen la peculiaridad de que al
    momento de alimentar a sus DCCriaturas logran aumentar en 5 puntos
    los puntos de salud totales de la criatura en cuestión.
    Por otra parte, siempre han tenido problemas al intentar recuperar alguna
    de sus DCCriaturas que han escapado, por lo que al capturarlas
    merman la salud actual de la criatura en 7 puntos.

    Habilidad especial
    ------------------
    Los Magizoólogos de esta especialidad tienen la habilidad especial de
    saciar el hambre de todas sus criaturas sin la necesidad de darles alimentos
    y disminuyendo a cero la cantidad de días que llevan sin comer.
    Esto lo pueden hacer una sola vez como usuario.

    Atributos
    ---------
    - El nivel mágico de los Docencios varia entre 40 y 60.
    - Su destreza oscila entre 30 y 40.
    - Su energía total estará entre 40 y 50.
    - Su responsabilidad variaría entre 15 y 20.
    """
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

    def alimentar_dccriatura(self):
        criatura_alimentada = super().alimentar_dccriatura()
        if criatura_alimentada:
            print("Habilidad pasiva: Has sanado 5pts de vida adicionales!")
            criatura_alimentada.vida_actual += PMT.DOCENCIO_PASIVO_SANAR_VIDA

    def recuperar_dccriatura(self):
        criatura_recuperada = super().recuperar_dccriatura()
        if criatura_recuperada:
            criatura_recuperada.vida_actual -= PMT.DOCENCIO_PASIVO_MERMAN

    def habilidad_especial(self):
        if super().habilidad_especial():
            print("Has saciado el hambre de todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.dias_sin_comer = 0


class MagizoologoTareo(Magizoologo):
    """
    =================
    Magizoólogo Tareo
    =================

    Habilidad pasiva
    ----------------
    Los Magizoólogo Tareos poseen la ventaja de que al alimentar a
    sus DCCriaturas poseen un 70% de probabilidad de recuperar toda la
    alud actual de la criatura que recibió el alimento.
    Por otra parte, al recuperar a una de sus DCCriaturas que haya escapado
    esta no se verá afectada de forma negativa, a diferencia de los Docencios.

    Habilidad especial
    ------------------
    Estos Magizoólogo tienen la habilidad especial de
    poder recuperar a todas las criaturas que hayan escapado que
    aún no hayan sido recuperadas con un 100% de efectividad.
    Esta habilidad solo se puede realizar una sola vez como usuario.

    Atributos
    ---------
    - El nivel mágico de los Tareos varia entre 40 y 55.
    - Su destreza oscila entre 40 y 50
    - Su energía total estará entre 35 y 45.
    - Por último, su responsabilidad variará entre 10 y 25.
    """
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

    def alimentar_dccriatura(self):
        criatura_alimentada = super().alimentar_dccriatura()
        if criatura_alimentada and PMT.TAREO_PASIVO_PROB_SANAR >= random.random():
            print("Habilidad pasiva: Has sanado toda su vida!")
            criatura_alimentada.vida_actual = criatura_alimentada.vida_max

    def recuperar_dccriatura(self):
        super().recuperar_dccriatura()

    def habilidad_especial(self):
        if super().habilidad_especial():
            print("Has recuperado todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.escapado = False


class MagizoologoHibrido(Magizoologo):
    """
    ====================
    Magizoólogos Híbrido
    ====================

    Habilidad pasiva
    ----------------
    Al alimentar una de sus DCCriaturas, los Magizoólogos Híbrido logran
    que la criatura en cuestión logre recuperar 10 puntos de salud.
    Además, al igual que los Tareos, cuando capturan una DCCriatura que
    haya escapado no provocan ningún tipo de efecto secundario en ella.

    Habilidad especial
    ------------------
    La habilidad especial de los Magizoólogos Híbrido es la de poder sanar
    a todas sus criaturas que se encuentren enfermas con un 100% de efectividad.
    Esta acción solo puede realizarse una sola vez como usuario.

    Atributos
    ---------
    - El nivel mágico de los Híbrido varia entre 35 y 45.
    - Su destreza oscila entre 30 y 50.
    - Su energía total estará entre 50 y 55.
    - Su responsabilidad variará entre 15 y 25
    """
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

    def alimentar_dccriatura(self):
        criatura_alimentada = super().alimentar_dccriatura()
        if criatura_alimentada:
            print("Habilidad pasiva: Has sanado 10pts de vida adicionales!")
            criatura_alimentada.vida_actual += PMT.DOCENCIO_PASIVO_SANAR_VIDA

    def recuperar_dccriatura(self):
        super().recuperar_dccriatura()

    def habilidad_especial(self):
        if super().habilidad_especial():
            print("Has sanado a todas tus criaturas!")
            for criatura in self.criaturas:
                criatura.enferma = False


class MagizoologoSuper(MagizoologoTareo, MagizoologoHibrido, MagizoologoDocencio):
    """
    Al pasar al día siguiente, si un Magizoólogo alcanza un nivel de aprobación
    igual a 100 entonces se convertirá en un Magizoólogo DocencioTareoHíbrido,
    notificando al usuario. El nuevo Magizoólogo DocencioTareoHíbrido deberá
    conservar los mismos atributos que tenía antes de la transformación.
    Además, podría tener los mismos beneficios que tienen los Magizoólogo
    Docencios, Tareos e Híbridos por separado, siendo estos los
    que se ven a continuación:
    - Al alimentar una criatura, existe una probabilidad
      del 70% de que recupere toda su salud.
    - Al alimentar una criatura, ésta recupera 10 puntos de salud en
      caso de que no haya recuperado su total en el criterio anterior.
    - Al capturar una DCCriatura, ésta no pierde salud.
    Otras características propias son:
    - Debe mantener sus atributos pasados
    - Puede volver a utilizar la habilidad especial
    - En el archibo para a llamarse "super"
    """
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
        pass

    """
    TODO: No tengo bien entendido si esta es una manera valida de realizar el bonus
    Los 3 métodos los definí como métodos abstractos es la clase principal,
    entonces los tendré que definir aquí también (creo)
    """
    def alimentar_dccriatura(self):
        pass

    def recuperar_dccriatura(self):
        pass

    def habilidad_especial(self):
        """
        Debe elegir entre cualquiera de las habilidades especiales
        de los Magizoólogo que heredó.
        """
        pass
