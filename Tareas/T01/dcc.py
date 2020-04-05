import random


class DCC:
    """
    Es la institución más seria y respetable del mundo mágico.
    Permite fiscalizar a los Magizoólogo y aplicarles multas
    en caso de que incurran en una falta. Además controlan el
    nivel de aprobación de los Magizoólogo, pudiendo quitarles
    su licencia.
    """

    """TODO:
    Tengo la duda es si se necesita crear un objeto DCC
    Talvez se pueda usar la clase DCC directamente?
    Por ejemplo:
    ````
    DCC.calcular_aprobación(magizoologo)
    ```
    y no tener que usar
    ```
    dcc = DCC()
    dcc.calcular_aprobación(magizoologo)
    ```
    """
    def calcular_aprobación(self):
        """
        Calcula la aprobación del Magizoólogo al finalizar el día.
        """
        pass

    def pagar_magizoologo(self):
        """
        Paga Sicklets al Magizoólogo al finalizar el día.
        """
        pass

    def fiscalizar_magizoologo(self):
        """
        Fiscaliza al Magizoólogo al finalizar el día, multandolo si es
        necesario. Puede que al DCC se le olvide multar en algunos casos.
        """
        pass

    def vernder_alimentos(self):
        """
        Vende alimentos al Magizoólogo.
        """
        pass

    def mostrar_estado(self):
        """
        Muestra toda la información del Magizoólogo.
        Esta es:
        - Nombre
        - Sickles
        - Energía actual
        - Licencia
        - Nivel de aprobación
        - Nivel mágico
        - Destreza
        - Responsabilidad
        - Lista de los alimentos
          - Tipos
          - Efectos a la salud
        - Lista de DCCriaturas
          - Nombre
          - Nivel mágico
          - Puntos de salud actual
          - Estado de salud
          - Nivel de hambre
          - Nivel de agresividad
        """
        pass
