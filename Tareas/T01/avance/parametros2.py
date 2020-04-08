
MAGIZOOLOGOS = {
    "PRETERMINADOS":{
        "SICKLES": 500,
        "LICENCIA": "True",
        "HABILIDADES": "True",
        "APROBACION INICIAL": 60,
        "DOCENCIO": {
            "RANGO NIVEL MAGICO": (40, 60),
            "RANGO DESTREZA": (30, 40),
            "RANGO ENERGIA MAX": (40, 50),
            "RANGO RESPONSABILIDAD": (15, 20),
        },
        "TAREO": {
            "RANGO NIVEL MAGICO": (40, 55),
            "RANGO DESTREZA": (40, 50),
            "RANGO ENERGIA MAX": (35, 45),
            "RANGO RESPONSABILIDAD": (10, 25),
        },
        "HIBRIDO": {
            "RANGO NIVEL MAGICO": (35, 45),
            "RANGO DESTREZA": (30, 50),
            "RANGO ENERGIA MAX": (50, 55)
            "RANGO RESPONSABILIDAD": (15, 25),
        }
    }
}


CRIATURAS = {
    "ALIMENTARSE": {
        "EFECTO HAMBRE": {"satisfecha": 0, "hambrienta": 15},
        "EFECTO AGRESIVIDAD": {"satisfecha": 0, "hambrienta": 20},
    },
    "ESCAPARSE": {
        "EFECTO HAMBRE": {"satisfecha": 0, "hambrienta": 20},
    },
    "PRETERMINADOS": {
        "AUGUREY": {
            "RANGO NIVEL MAGICO": (20, 50),
            "PROP ESCAPARSE": 0.2,
            "PROP ENFERMARSE": 0.3,
            "RANGO VIDA MAXIMA": (35, 45),
            "TIEMPO SATISFECHA": 3,
            "NIVEL AGRESIVIDAD": "inofensiva",
        },
        "NIFFLER": {
            "RANGO NIVEL MAGICO": (10, 20),
            "PROP ESCAPARSE": 0.3,
            "PROP ENFERMARSE": 0.2,
            "RANGO VIDA MAXIMA": (20, 30),
            "TIEMPO SATISFECHA": 2,
            "NIVEL AGRESIVIDAD": "arisca",
            "RANGO CLEPTOMANIA": (5, 10),
        },
        "ERKLING": {
            "RANGO NIVEL MAGICO": (30, 45),
            "PROP ESCAPARSE": 0.5,
            "PROP ENFERMARSE": 0.3,
            "RANGO VIDA MAXIMA": (50, 60),
            "TIEMPO SATISFECHA": 2,
            "NIVEL AGRESIVIDAD": "peligrosa",
        },
    }
}
