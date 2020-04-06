"""
========================================
Parametros del Programa Zoológico Mágico
========================================
"""

from os import path

# ============================================ #
# Parámetros relacionados con los PATH         #
# ============================================ #
PATH_CARPETA = "data"
PATH_CRIATURAS = path.join(PATH_CARPETA, "criaturas.csv")
PATH_MAGIZOOLOGOS = path.join(PATH_CARPETA, "magizoologos.csv")


# ============================================ #
# Parámetros relacionados con el UI            #
# ============================================ #
UI_ANCHO = 20


# ============================================ #
# Parámetros relacionados con los Magizoólogos #
# ============================================ #
MAGIZOOLOGOS_SICKLES_INICIALES = 500

# ---------------------- #
#  Magizoólogos Docencio #
# ---------------------- #
DOCENCIO_RANGO_NIVEL_MAGICO = (40, 60)
DOCENCIO_RANGO_DESTREZA = (30, 40)
DOCENCIO_RANGO_ENERGIA_MAX = (40, 50)
DOCENCIO_RANGO_RESPONSABILIDAD = (15, 20)

# ---------------------- #
#  Magizoólogo Tareo     #
# ---------------------- #
TAREO_RANGO_NIVEL_MAGICO = (40, 55)
TAREO_RANGO_DESTREZA = (40, 50)
TAREO_RANGO_ENERGIA_MAX = (35, 45)
TAREO_RANGO_RESPONSABILIDAD = (10, 25)

# ---------------------- #
#  Magizoólogos Híbrido  #
# ---------------------- #
HIBRIDO_RANGO_NIVEL_MAGICO = (35, 45)
HIBRIDO_RANGO_DESTREZA = (30, 50)
HIBRIDO_RANGO_ENERGIA_MAX = (50, 55)
HIBRIDO_RANGO_RESPONSABILIDAD = (15, 25)


# ============================================ #
# Parámetros relacionados con las criaturas    #
# ============================================ #

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

# ---------------- #
#  Erkling         #
# ---------------- #
ERKLING_RANGO_NIVEL_MAGICO = (30, 45)
ERKLING_PROB_ESCAPARSE = 0.5
ERKLING_PROP_ENFERMARSE = 0.3
ERKLING_RANGO_VIDA_MAXIMA = (50, 60)
ERKLING_TIEMPO_SATISFECHA = 2
ERKLING_NIVEL_AGRESIVIDAD = "arisca"
ERKLING_RANGO_CLEPTOMANIA = (5, 10)
