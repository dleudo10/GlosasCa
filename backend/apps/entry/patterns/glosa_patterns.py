GLOSA_PATTERNS = {

    "emisor": {
        "keywords": [
            "suramericana",
            "sura",
            "eps sura",
            "eps y medicina prepagada suramericana",
        ],
        "patterns": [
            r"\bSURAMERICANA\b",
            r"\bSURA\b",
        ],
        "weight": 10,
        "min_matches": 1,
        "strong": False,
    },

    "glosa": {
        "keywords": [
            "numero de glosa",
            "valor de glosa",
            "fecha notificacion",
            "fecha radicacion",
        ],
        "patterns": [
            r"N[ÚU]MERO\s+DE\s+GLOSA",
            r"VALOR\s+DE\s+GLOSA",
            r"FECHA\s+NOTIFICACI[ÓO]N",
            r"FECHA\s+RADICACI[ÓO]N",
        ],
        "weight": 25,
        "min_matches": 2,
        "strong": True,
    },

    "factura": {
        "keywords": [
            "factura",
            "fecha de la factura",
            "valor facturado",
        ],
        "patterns": [
            r"\bFACTURA\b",
            r"FECHA\s+DE\s+LA\s+FACTURA",
            r"VALOR\s+FACTURADO",
        ],
        "weight": 15,
        "min_matches": 1,
        "strong": True,
    },

    "servicios": {
        "keywords": [
            "informacion del servicio",
            "informacion del servicio",
            "codigo cups",
            "cups/cum",
            "valor cobrado",
            "valor glosa",
        ],
        "patterns": [
            r"INFORMACI[ÓO]N\s+DEL\s+SERVICIO",
            r"C[ÓO]DIGO\s+CUPS",
            r"CUPS\s*/\s*CUM",
            r"VALOR\s+COBRADO",
            r"VALOR\s+GLOSA",
        ],
        "weight": 20,
        "min_matches": 1,
        "strong": True,
    },

    "causas": {
        "keywords": [
            "causa general",
            "causa especifica",
            "detalle causa",
            "descripcion causa",
        ],
        "patterns": [
            r"CAUSA\s+GENERAL",
            r"CAUSA\s+ESPEC[ÍI]FICA",
            r"DETALLE\s+CAUSA",
            r"DESCRIPCI[ÓO]N\s+CAUSA",
        ],
        "weight": 20,
        "min_matches": 1,
        "strong": True,
    },

    "observaciones": {
        "keywords": [
            "observaciones generales",
            "observacion",
            "total glosas",
        ],
        "patterns": [
            r"OBSERVACIONES\s+GENERALES",
            r"OBSERVACI[ÓO]N(?:ES)?",
            r"TOTAL\s+GLOSAS",
        ],
        "weight": 10,
        "min_matches": 1,
        "strong": False,
    },
}