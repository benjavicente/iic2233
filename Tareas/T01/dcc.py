import random
import parametros as PMT
from operator import attrgetter


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
    def calcular_aprobación(self, magizoologo):
        """
        Calcula la aprobación del Magizoólogo al finalizar el día.
        """
        pass

    def pagar_magizoologo(self, magizoologo):
        """
        Paga Sicklets al Magizoólogo al finalizar el día.
        """
        pass

    def fiscalizar_magizoologo(self, magizoologo):
        """
        Fiscaliza al Magizoólogo al finalizar el día, multandolo si es
        necesario. Puede que al DCC se le olvide multar en algunos casos.
        """
        pass

    def vernder_criaturas(self, magizoologo):
        """
        Un Magizoólogo puede adquirir nuevas DCCriaturas a través
        del DCC siempre y cuando este posea su licencia. El costo
        de cada criatura es de 75 Sickles para un Augurey, 100
        Sickles para un Nier y 125 Sickles para un Erkling.
        """
        pass

    def vernder_alimentos(self, magizoologo):
        """
        Vende alimentos al Magizoólogo.
        """
        pass

    def mostrar_estado(self, magizoologo):
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
        # Datos Magizoólogo
        print("Estas son tus estadísticas:")
        datos = ("nombre", "sickles", "energia_actual",
                 "licencia", "nivel_aprobacion", "nivel_magico",
                 "destreza", "responsabilidad")
        extractor_datos = attrgetter(*datos)
        for key, value in zip(datos, extractor_datos(magizoologo)):
            key = key.replace("_", " ").capitalize()
            print(f" - {key}: {value}")
        # Criaturas
        print(f" - Criaturas:")
        for criatura in magizoologo.criaturas:
            print(f"   - {criatura.nombre}")
            datos = ("tipo", "nivel_magico", "vida_actual",
                     "enferma", "escapado", "nivel_hambre", "agresividad")
            extractor_datos = attrgetter(*datos)
            for k, v in zip(datos, extractor_datos(criatura)):
                k = k.replace("_", " ").capitalize()
                print(f"     - {k}: {v}")
        # Alimentos
        if magizoologo.alimentos:
            print(" - Alimentos:")
            d = dict()
            for alimento in magizoologo.alimentos:
                if str(alimento) not in d:
                    d[str(alimento)] = [1, alimento.pnt_vida]
                else:
                    d[str(alimento)][0] += 1
            for alimento, datos in d.items():
                nombre = str(alimento)
                if datos[0] >= 2:
                    nombre = nombre.replace(" ", "s ", 1)
                    if " " not in nombre:
                        nombre = nombre + "s"
                print(f"   - {datos[0]} {nombre}: +{datos[1]}hp")
        else:
            print(" - Sin alimentos")

