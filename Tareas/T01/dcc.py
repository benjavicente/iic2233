import random
import parametros as PMT
from operator import attrgetter
import procesos as pc
import alimentos as alm
import dccriaturas as ctr


class DCC:
    """
    Es la institución más seria y respetable del mundo mágico.
    Permite fiscalizar a los Magizoólogo y aplicarles multas
    en caso de que incurran en una falta. Además controlan el
    nivel de aprobación de los Magizoólogo, pudiendo quitarles
    su licencia.
    """
    def calcular_aprobacion(self, magizoologo) -> None:
        """
        Calcula la aprobación del Magizoólogo al finalizar el día.
        """
        sanas = 0
        retenidas = 0
        total = 0
        for criatura in magizoologo.criaturas:
            sanas += not criatura.enferma
            retenidas += not criatura.escapado
            total += 1
        min_aprob, max_aprob = PMT.MAGIZOOLOGOS_RANGO_APROBACION
        aprobacion = int(min(max_aprob, max(min_aprob, ((sanas + retenidas)/(2 * total)) * 100)))
        print(f"Tu nuevo nivel de aprobación es: {aprobacion}")
        magizoologo.nivel_aprobacion = aprobacion

    def pagar_magizoologo(self, magizoologo) -> None:
        """
        Paga Sickles al Magizoólogo al finalizar el día.
        """
        pago = int(PMT.DCC_PESO_PAGO["aprobacion"] * magizoologo.nivel_aprobacion
                   + PMT.DCC_PESO_PAGO["alimento"] * len(magizoologo.alimentos)
                   + PMT.DCC_PESO_PAGO["magico"] * magizoologo.nivel_magico)
        magizoologo.sickles += pago
        print(f"EL DCC te ha pagado {pago} Sickles")

    def fiscalizar_magizoologo(self, magizoologo) -> None:
        """
        Fiscaliza al Magizoólogo al finalizar el día, multandolo si es
        necesario. Puede que al DCC se le olvide multar en algunos casos.
        """
        dict_multas = {
            "escape": 0,
            "enfermedad": 0,
            "vida critica": 0,
        }
        for criatura in magizoologo.criaturas:
            if criatura.escapado:
                dict_multas["escape"] +=\
                    PMT.DCC_FISCALIZADO["escape"][1] >= random.random()
            if criatura.enferma:
                dict_multas["enfermedad"] +=\
                    PMT.DCC_FISCALIZADO["enfermedad"][1] >= random.random()
            if criatura.vida_actual == PMT.CRIATURAS_VIDA_MINIMA:
                dict_multas["vida critica"] +=\
                    PMT.DCC_FISCALIZADO["vida critica"][1] >= random.random()
        if sum(dict_multas.values()):
            print("Estas multado por:")
            # Mostrar multas
            for nombre, multas in dict_multas.items():
                if multas:
                    print(f" - {multas} caso{'s' * (multas > 1)} de {nombre}: "
                          f"{PMT.DCC_FISCALIZADO[nombre][0]} Sickles cada una")
            # Pagar multas
            for nombre, multas in dict_multas.items():
                for _ in range(multas):
                    if magizoologo.sickles < PMT.DCC_FISCALIZADO[nombre][0]:
                        print("  No puedes pagar las multas!")
                        if magizoologo.licencia:
                            print("  Te quitaron la licencia!")
                            magizoologo.licencia = False
                        return
                    magizoologo.sickles -= PMT.DCC_FISCALIZADO[nombre][0]
        else:
            print("No recibiste ninguna multa!")

    def vernder_criaturas(self, magizoologo, lista_criaturas: list) -> None:
        """
        Lista criaturas debe ser una lista en la que
        se chequeará si el nombre de la criatura existe con
        nombre == str(lista_criaturas[n])
        """
        if not magizoologo.licencia:
            print("No puedes adoptar, no tienes licencia")
            return
        while True:
            # No de puede realizar un proceso multipaso
            # porque una condición depende del input anterior
            print("Elige una criatura! Los costos son:")
            # Elección
            for key, value in PMT.DCC_PRECIO_CRIATURAS.items():
                print(f" - {key.capitalize()}: {value} Sickles")
            print(f"Tienes: {magizoologo.sickles}")
            criatura = input("-->").strip().lower()
            # Chequeo
            if criatura in PMT.DCC_PRECIO_CRIATURAS:
                if PMT.DCC_PRECIO_CRIATURAS[criatura] <= magizoologo.sickles:
                    razon = None
                else:
                    razon = "Contienes sickles suficientes"
            else:
                razon = "La criatura es válida"
            if razon:
                if pc.volver_a_intentarlo(criatura, razon):
                    continue
                else:
                    break
            # Nombre de la criatura
            while True:
                print("Genial! Cual será el nombre de tu criatura?")
                nombre = input("-->").strip()
                if nombre.isalnum():
                    if nombre.lower() not in map(str.lower, lista_criaturas):
                        lista_criaturas.append(nombre)
                        c = ctr.retornar_clase_criatura(criatura)
                        magizoologo.sickles -= PMT.DCC_PRECIO_CRIATURAS[criatura]
                        magizoologo.adoptar_dccriatura(c(nombre))
                        print(f"Felicidades! Adoptaste a {nombre}")
                        return
                    else:
                        if not pc.volver_a_intentarlo(nombre, "El nombre es único"):
                            break
                else:
                    if not pc.volver_a_intentarlo(nombre, "El nombre es alfanumérico"):
                        break
        return

    def vernder_alimentos(self, magizoologo) -> None:
        while True:
            # Elección
            print("Elige un alimento...")
            for key, value in PMT.DCC_PRECIO_ALIMENTOS.items():
                print(f" - {key.capitalize()}: {value} Sickles")
            alimento = input("-->").strip().lower()
            # Chequeo
            razon = None
            if alimento in PMT.DCC_PRECIO_ALIMENTOS:
                if not PMT.DCC_PRECIO_ALIMENTOS[alimento] <= magizoologo.sickles:
                    razon = "Contienes sickles suficientes"
            else:
                razon = "El alimento es valido"
            if razon:
                if pc.volver_a_intentarlo(alimento, razon):
                    continue
                else:
                    break
            # Compra del alimento
            precio = PMT.DCC_PRECIO_ALIMENTOS[alimento]
            magizoologo.sickles -= precio
            print(f"Has comprado {alimento} por {precio} Sickles!")
            clase_alimento = alm.retornar_clase_alimento(alimento)
            magizoologo.comprar_alimentos(clase_alimento())
            return

    def mostrar_estado(self, magizoologo) -> None:
        """
        Muestra toda la información del Magizoólogo.
        Esta es:
        - Nombre
        - Tipo
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
        datos = ("nombre", "tipo", "sickles", "energia_actual",
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
