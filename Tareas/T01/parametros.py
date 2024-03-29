"""
========================================
Parametros del Programa Zoológico Mágico
========================================
"""

from os import path

# ============================================ #
# Parámetros relacionados con los Archivos     #
# ============================================ #

# --------- #
#  PATH     #
# --------- #
PATH_CARPETA = "data"
PATH_CRIATURAS = path.join(PATH_CARPETA, "criaturas.csv")
PATH_MAGIZOOLOGOS = path.join(PATH_CARPETA, "magizoologos.csv")

# --------- #
#  Formato  #
# --------- #
# Esto permite cambiar el orden a los datos en los archivos
FORMATO_CRIATURAS = ("nombre", "tipo", "nivel_magico", "prob_escaparse",
                     "prob_enfermarse", "enferma", "escapado",
                     "vida_max", "vida_actual", "nivel_hambre",
                     "agresividad", "dias_sin_comer", "nivel_cleptomania")

FORMATO_MAGIZOOLOGOS = ("nombre", "tipo", "sickles", "criaturas",
                        "alimentos", "licencia", "nivel_magico",
                        "destreza", "energia_max", "responsabilidad",
                        "puede_usar_habilidad")


# ============================================ #
# Parámetros relacionados con el UI            #
# ============================================ #
UI_ANCHO = 50  # En caracteres

# ============================================ #
# Parámetros relacionados con el DCC           #
# ============================================ #
DCC_PRECIO_CRIATURAS = {"augurey": 75, "niffler": 100, "erkling": 125}
DCC_PRECIO_ALIMENTOS = {"tarta de melaza": 10, "higado de dragon": 15, "buñuelo de gusarajo": 3}
DCC_FISCALIZADO = {"escape": (50, 0.5), "enfermedad": (70, 0.7), "vida critica": (150, 1)}
DCC_PESO_PAGO = {"aprobacion": 4, "alimento": 15, "magico": 3}
DCC_APROBACION = 60


# ============================================ #
# Parámetros relacionados con los Magizoólogos #
# ============================================ #
MAGIZOOLOGOS_NOMBRES = {"docencio", "tareo", "hibrido"}
MAGIZOOLOGOS_SICKLES_INICIALES = 500
MAGIZOOLOGOS_LICENCIA_INICIAL = "True"
MAGIZOOLOGOS_HABILIDADES = "True"
MAGIZOOLOGOS_ENERGIA_MINIMA = 0
MAGIZOOLOGOS_COSTO_ALIMENTAR = 5
MAGIZOOLOGOS_COSTO_RECUPERAR = 10
MAGIZOOLOGOS_COSTO_CURAR = 8
MAGIZOOLOGOS_COSTO_HABILIDAD = 15
MAGIZOOLOGOS_RANGO_APROBACION = (0, 100)

# ---------------------- #
#  Magizoólogos Docencio #
# ---------------------- #
DOCENCIO_RANGO_NIVEL_MAGICO = (40, 60)
DOCENCIO_RANGO_DESTREZA = (30, 40)
DOCENCIO_RANGO_ENERGIA_MAX = (40, 50)
DOCENCIO_RANGO_RESPONSABILIDAD = (15, 20)
DOCENCIO_PASIVO_SANAR_VIDA = 5
DOCENCIO_PASIVO_MERMAN = 7

# ---------------------- #
#  Magizoólogo Tareo     #
# ---------------------- #
TAREO_RANGO_NIVEL_MAGICO = (40, 55)
TAREO_RANGO_DESTREZA = (40, 50)
TAREO_RANGO_ENERGIA_MAX = (35, 45)
TAREO_RANGO_RESPONSABILIDAD = (10, 25)
TAREO_PASIVO_PROB_SANAR = 0.7

# ---------------------- #
#  Magizoólogos Híbrido  #
# ---------------------- #
HIBRIDO_RANGO_NIVEL_MAGICO = (35, 45)
HIBRIDO_RANGO_DESTREZA = (30, 50)
HIBRIDO_RANGO_ENERGIA_MAX = (50, 55)
HIBRIDO_RANGO_RESPONSABILIDAD = (15, 25)
HIBRIDO_PASIVO_SANAR_VIDA = 10


# ============================================ #
# Parámetros relacionados con las criaturas    #
# ============================================ #
CRIATURAS_NOMBRES = {"augurey", "niffler", "erkling"}
ALIMENTARSE_EFECTO_HAMBRE = {"satisfecha": 0, "hambrienta": 15}
ALIMENTARSE_EFECTO_AGRESIVIDAD = {"inofensiva": 0, "arisca": 20, "peligrosa": 40}
ALIMENTARSE_MINIMO_ATAQUE = 10
ESCAPARSE_EFECTO_HAMBRE = {"satisfecha": 0, "hambrienta": 20}
CRIATURAS_PENALISACION_VIDA_ENFERMEDAD = 7
CRIATURAS_PENALISACION_VIDA_HAMBRIENTA = 3
CRIATURAS_VIDA_MINIMA = 1

# ---------------- #
#  Augurey         #
# ---------------- #
AUGUREY_RANGO_NIVEL_MAGICO = (20, 50)
AUGUREY_PROB_ESCAPARSE = 0.2
AUGUREY_PROP_ENFERMARSE = 0.3
AUGUREY_RANGO_VIDA_MAXIMA = (35, 45)
AUGUREY_TIEMPO_SATISFECHA = 3
AUGUREY_NIVEL_AGRESIVIDAD = "inofensiva"

# ---------------- #
#  Niffler         #
# ---------------- #
NIFFLER_RANGO_NIVEL_MAGICO = (10, 20)
NIFFLER_PROB_ESCAPARSE = 0.3
NIFFLER_PROP_ENFERMARSE = 0.2
NIFFLER_RANGO_VIDA_MAXIMA = (20, 30)
NIFFLER_TIEMPO_SATISFECHA = 2
NIFFLER_NIVEL_AGRESIVIDAD = "arisca"
NIFFLER_RANGO_CLEPTOMANIA = (5, 10)
NIFFLER_PESO_SICKLES_ROBADOS = 2

# ---------------- #
#  Erkling         #
# ---------------- #
ERKLING_RANGO_NIVEL_MAGICO = (30, 45)
ERKLING_PROB_ESCAPARSE = 0.5
ERKLING_PROP_ENFERMARSE = 0.3
ERKLING_RANGO_VIDA_MAXIMA = (50, 60)
ERKLING_TIEMPO_SATISFECHA = 2
ERKLING_NIVEL_AGRESIVIDAD = "peligrosa"


# ============================================ #
# Parámetros relacionados con los alimentos    #
# ============================================ #
ALIMENTOS_TARTA_MALEZA_PNT = 15
ALIMENTOS_HIGADO_DRAGON_PNT = 10
ALIMENTOS_BUNUELO_GUSARAJO_PNT = 5
ALIMENTOS_TARTA_PROB_PACIFICAR_NIFFLER = 0.15
ALIMENTOS_BUNUELO_PROB_CONSUMIR = 0.65


# ============================================ #
# Parámetros relacionados con las Peleas       #
# ============================================ #
PELEAS_APUESTA = 30
PELEAS_ATAQUE = {"inofensiva": 0.25, "arisca": 0.3, "peligrosa": 0.35}
PELEAS_PROB_ESQUIVAR = 0.5
PELEAS_EL_DCC_ELIGE = False  # True --> Sí elige | False --> No elige (Pauta)
PELEAS_INICIAL = 1  # 1 --> Magizoólogo | 0 --> DCC

# ============================================ #
# Parámetros relacionados con SuperMagizoólogo #
# ============================================ #
SUPERMAGIZOOLOGO_ACTIVO = True
SUPERMAGIZOOLOGO_APROBACION = MAGIZOOLOGOS_RANGO_APROBACION[1]  # Aprobación máxima
