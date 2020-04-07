from abc import ABC, abstractmethod
import random
import parametros as PMT
import alimentos as alm

class Magizoologo(ABC):
    """
    ===========
    Magizoólogo
    ===========
    Son quienes se encargan de cuidar las DCCriaturas con el objetivo de preservar
    su existencia. Todo Magizoólogo puede y debe alimentar a sus DCCriaturas,
    capturarlas en caso de que escapen y sanarlas en caso de que enfermen.

    Atributos
    ---------
    `nombre` : `str`
        Es el identificador único del Magizoólogo.
        Ningún otro Magizoólogo puede tener el nombre
        de uno ya existente y este debe estar formado
        exclusivamente por caracteres alfanuméricos,
        y sin distinción entre mayúsculas y minúsculas.
    `criaturas` : `list`
        Son las distintas DCCriaturas que están a su
        cuidado. Todo Magizoólogo tiene al menos una
        criatura bajo su cuidado.
    `alimentos` : `list`
        Son los productos esenciales para el cuidado
        de tus DCCriaturas. Cada nuevo Magizoólogo
        parte con 1 alimento aleatorio.
    `sickles` : `int`
        Los Sickles son la moneda principal en la
        economía del mundo mágico. Todo Magizoólogo
        no puede tener saldo negativo y todos comienzan
        con una cantidad inicial de 500 Sickles.
    `energia_actual` : `int`
        Es el recurso energético que se regenera día a
        día para ejecutar acciones, puede estar entre
        0 y su valor máximo y disminuye por cada
        acción que se realiza. Su valor inicial diario
        y máximo dependera de cada Magizoólogo.
    `licencia` : `bool`
        Indica si el Magizoólogo está certificado como
        cuidador. Cada nuevo Magizoólogo comienza con su
        licencia, pero si la pierde el DCC no le permitirá
        adoptar nuevas criaturas hasta que la recupere.
    `nivel_aprobacion` : `int`
        Corresponde a la calificación diaria otorgada por
        el DCC según el estado de las DCCriaturas que se
        posee. Varía entre 0 y 100, y si es menor a 60 el
        Magizoólogo pierde su licencia.
    `nivel_magico` : `int`
        Indicará que tan apto es el Magizoólogo para
        alimentar, recuperar y sanar a sus DCCriaturas.
    `destreza` : `int`
        Cuando una de tus DCCriaturas huye,
        el nivel de destreza influirá en las
        posibilidades de recuperarla.
    `energia_max` : `int`
        El nivel de energía inicial y máxima que determina
        la cantidad de acciones que un Magizoólogo puede
        hacer por día. Cada vez que comienza un día nuevo,
        la energía actual se recupera a este nivel.
    `responsabilidad` : `int`
        Influirá en las posibilidades de enfermar y
        escapar que tienen las DCCriaturas que se poseen.

    Acciones (Métodos)
    ------------------
        `adoptar_dccriatura()`
        `comprar_alimentos()`
        `alimentar_dccriatura()`
        `recuperar_dccriatura()`
        `sanar_dccriatura()`
        `habilidad_especial()`
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
                 nivel_aprobacion=None,
                 **kwargs):
        # -------------- #
        # Valores únicos #
        # -------------- #
        self.nombre = str(nombre)
        self.tipo = type(self).__name__.replace("Magizoologo", "")
        # ---------------------------- #
        # Valores de listad de objetos #
        # ---------------------------- #
        if criaturas is None:
            criaturas = list()
        if alimentos is None:
            alimento = random.choice((alm.BunueloGusarajo,
                                           alm.HigadoDragon,
                                           alm.BunueloGusarajo))
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
        if nivel_aprobacion is None:
            nivel_aprobacion = PMT.MAGIZOOLOGOS_APROBACION_INICIAL
        # Transformación de valores
        self._sickles = int(sickles)
        self.licencia = licencia == "True"
        self.puede_usar_habilidad = puede_usar_habilidad == "True"
        self._nivel_aprobacion = int(nivel_aprobacion)
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
        self.energia_actual = energia_max

    def __str__(self):
        return self.nombre

    def __eq__(self, value):
        return self.nombre == value

    def __repr__(self):
        return f"{type(self).__name__} {self.nombre}: Sicklets={self.sickles}"

    @property
    def nivel_aprobacion(self):
        return self._nivel_aprobacion

    @nivel_aprobacion.setter
    def nivel_aprobacion(self, value):
        if value >= 100:
            self._nivel_aprobacion = 100
            pass  # Hacer Super Magizoólogo
        elif value < 0:
            self._nivel_aprobacion = 0
        if (not self.licencia) and value >= 60:
            self.licencia = True
        elif self.licencia and value < 60:
            self.licencia = False

    @property
    def sickles(self):
        return self._sickles

    @sickles.setter
    def sickles(self, value):
        if value >= 0:
            self._sickles = 0
        else:
            self._sickles = value

    def adoptar_dccriatura(self, criatura=None):
        if criatura:
            # Ya eligió una criatura
            self.criaturas.append(criatura)
        else:
            # Tiene que elegir una criatura
            if not self.licencia:
                print("No puedes adoptar, no tienes licencia")
                return
            # TODO
            # dcc.vender_criarura()
            """
            El Magizoólogo puede adoptar nuevas DCCriaturas al DCC,
            solo si posee actualmente su licencia. Además, esta acción está
            limitada por la capacidad monetaria del usuario que queda
            sujeta al precio de cada criatura.
            """

    def comprar_alimentos(self):
        """
        El Magizoólogo puede comprar alimentos al DCC.
        Esta acción solo está limitada por la capacidad
        monetaria del usuario que la ja el precio del alimento.
        """
        pass

    @abstractmethod
    def alimentar_dccriatura(self):
        """
        El Magizoólogo puede decidir alimentar a una de sus DCCriaturas con
        alguno de sus alimentos, siempre y cuando posea alguno.
        En respuesta a esto, la DCCriatura puede atacar a su dueño.
        El costo energético de alimentar es de 5 puntos.
        """
        pass

    @abstractmethod
    def recuperar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta recuperar una de sus DCCriaturas.
        El coste energético de intentar recuperar una criatura es de 10 puntos.
        """
        # FORMULA EN TODO
        pass

    def sanar_dccriatura(self):
        """
        Cuando un Magizoólogo intenta sanar a alguna de sus DCCriaturas.
        Su coste energético es de 8 puntos.
        """
        # FORMULA EN TODO
        pass

    @abstractmethod
    def habilidad_especial(self):
        """
        Cada Magizoólogo tiene una habilidad especial que depende de su
        especialización. El costo energético de cualquiera
        de estas habilidades es de 15 puntos.
        """
        pass


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
        pass

    def recuperar_dccriatura(self):
        pass

    def habilidad_especial(self):
        pass


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
        pass

    def recuperar_dccriatura(self):
        pass

    def habilidad_especial(self):
        pass


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
        pass

    def recuperar_dccriatura(self):
        pass

    def habilidad_especial(self):
        pass


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
