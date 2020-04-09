"""
=========
Clase DDC
=========
Contiene la clase:
------------------
    DCC
Depende de:
-----------
    parametros
    procesos
    alimentos
    dccriaturas
"""

# TODO:
# Testear

# IMPORTANTE:
# Puede ser que me convenga unir la clase DCC con Magizoológico,
# ya que atributos de la clase Magizoológico son esenciales
# en los métodos de DCC

import random
import parametros as PMT
from operator import attrgetter
import procesos as pc
import alimentos as ams
import dccriaturas as ctr


class DCC:
    """
    Es la institución más seria y respetable del mundo mágico.
    Permite fiscalizar a los Magizoólogo y aplicarles multas
    en caso de que incurran en una falta. Además controlan el
    nivel de aprobación de los Magizoólogo, pudiendo quitarles
    su licencia.
    """
    def calcular_aprobación(self, magizoologo):
        """
        Calcula la aprobación del Magizoólogo al finalizar el día.
        """
        sanas = 0
        retenidas = 0
        total = 0
        for criaturas in magizoologo.criaturas:
            sanas += criaturas.enferma
            retenidas += criaturas.escapado
            total += 1
        aprobacion = min(100, max(0, (sanas + retenidas)//(2 * total) * 100))
        print(f"Tu nuevo nivel de aprobación es: {aprobacion}")
        magizoologo.nivel_aprobacion = aprobacion
        return True

    def pagar_magizoologo(self, magizoologo):
        """
        Paga Sicklets al Magizoólogo al finalizar el día.
        """
        pago = (PMT.DCC_PESO_PAGO["aprobacion"] * magizoologo.nivel_aprobacion
                + PMT.DCC_PESO_PAGO["alimento"] * len(magizoologo.alimentos)
                + PMT.DCC_PESO_PAGO["magico"] * magizoologo.nivel_magico)
        magizoologo.sickles += pago//1
        return True

    def fiscalizar_magizoologo(self, magizoologo):
        """
        Fiscaliza al Magizoólogo al finalizar el día, multandolo si es
        necesario. Puede que al DCC se le olvide multar en algunos casos.
        """
        dict_multas = {
            "escapes": 0,
            "enfermedad": 0,
            "vida critica": 0,
        }
        for criatura in magizoologo.criaturas:
            if criatura.escapado:
                dict_multas["escapes"] +=\
                    PMT.DCC_FISCALIZADO["escapes"][1] >= random.random()
            if criatura.enferma:
                dict_multas["enfermedad"] +=\
                    PMT.DCC_FISCALIZADO["enfermedad"][1] >= random.random()
            if criatura.vida_actual == 1:
                dict_multas["vida critica"] +=\
                    PMT.DCC_FISCALIZADO["vida critica"][1] >= random.random()
        if sum(dict_multas.values()):
            print("Estas multado por:")
            # Mostrar multas
            for nombre, multas in dict_multas.items():
                if multas:
                    print(f" - {multas} casos de {nombre}: "
                          f"{PMT.DCC_FISCALIZADO[nombre][0]} Sickles cada una")
            # Pagar multas
            for nombre, multas in dict_multas.items():
                for _ in range(multas):
                    if magizoologo.sickles < PMT.DCC_FISCALIZADO[nombre][0]:
                        print("No puedes pagar las multas, te quitaron la licencia!")
                        magizoologo.licencia = False
                        return False
                    magizoologo.sickles -= PMT.DCC_FISCALIZADO[nombre][0]
        else:
            print("No recibiste ninguna multa!")
        return True

    def vernder_criaturas(self, magizoologo, lista_criaturas):
        if not magizoologo.licencia:
            print("No puedes adoptar, no tienes licencia")
        while True:
            print("Elige una criatura! Los costos son...")
            criatura = input("-->").strip().lower()
            if criatura in PMT.CRIATURAS_TIPOS:
                if PMT.DCC_PRECIO_CRIATURAS[criatura] <= magizoologo.sickles:
                    razon = None
                else:
                    razon = "Contiene sickles suficientes"
            else:
                razon = "La criatura es válida"
            if razon:
                if pc.volver_a_intentarlo(criatura, razon):
                    continue
                else:
                    break
            while True:
                print("Genial! Cual será el nombre de tu criatura?")
                nombre = input("-->").strip()
                if nombre not in lista_criaturas:
                    c = ctr.retornar_clase_criatura(criatura)
                    magizoologo.adoptar_dccriatura(c(nombre))
                    return True
                else:
                    if not pc.volver_a_intentarlo(nombre, "Nombre único"):
                        break

    def vernder_alimentos(self, magizoologo):
        while True:
            print("Elige un alimento...")
            alimento = input("-->").strip().lower()
            if alimento in PMT.ALIMENTOS_TIPOS:
                if PMT.DCC_PRECIO_ALIMENTOS[alimento] <= magizoologo.sickles:
                    razon = None
                else:
                    razon = "Contiene sickles suficientes"
            else:
                razon = "El alimento es valido"
            if razon:
                if pc.volver_a_intentarlo(alimento, razon):
                    continue
                else:
                    break
            clase_alimento = ams.retornar_clase_alimento(alimento)
            magizoologo.comprar_alimentos(clase_alimento())
            return True

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
        return True
