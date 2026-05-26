# config.py
COLORS = {
    "dark_blue": "#1E2A44",
    "teal":      "#00A896",
    "blue":      "#2D9CDB",
    "violet":    "#7B61FF",
    "orange":    "#F2994A",
    "coral":     "#EB5757",
    "bg":        "#F5F7FB",
    "card":      "#FFFFFF",
}

MIN_N = 5

COL_FGS          = "fgs_status"
COL_GESCHLECHT   = "demog_geschlecht"
COL_ALTER        = "demog_alter"
COL_STUDIENGANG  = "demog_studiengang"
COL_ABSCHLUSSJAHR= "demog_abschlussjahr"
COL_MIGRATION    = "demog_migration"
COL_ARBEIT       = "demog_arbeit"
COL_HERAUSFORDERND = "open_herausfordernd_wann"

CHALLENGES = {
    "Finanzielle Belastung":         "ch_finanzen",
    "Zeitdruck durch Arbeit":        "ch_zeitdruck",
    "Unsicherheit im Studium":       "ch_unsicherheit",
    "Fehlendes Zugehörigkeitsgefühl":"ch_zugehoerigkeit",
    "Fehlende Informationen zum Studium": "ch_information",
    "Akademische Anforderungen":     "ch_akademisch",
}

FGS_LIKERT = {
    "Familienunterstützung": "fgs_familie_support",
    "Mehr leisten müssen":   "fgs_mehr_leisten",
    "Finanzielle Sorgen":    "fgs_fin_sorgen",
}

SOB_GROUPS = {
    "Allgemeine Zugehörigkeit": {
        "sob_willkommen": "Willkommen",
        "sob_dazugehoeren": "Dazugehören",
        "sob_studienricht": "Studienrichtung",
        "sob_respektiert": "Respektiert",
        "sob_identifikation": "Identifikation",
    },
    "Soziale Integration": {
        "sob_freundschaft": "Freundschaften",
        "sob_integration": "Integration",
        "sob_offen": "Offenheit",
        "sob_ernst": "Ernst genommen",
        "sob_support_kennen": "Support kennen",
        "sob_ansprechperson": "Ansprechperson",
    },
    "Akademische Zugehörigkeit": {
        "sob_unterricht": "Unterricht",
        "sob_sichtweisen": "Sichtweisen",
        "sob_fragen": "Fragen stellen",
        "sob_entwicklung": "Entwicklung",
        "sob_fachlich": "Fachlich",
    },
    "Identität & Vielfalt": {
        "sob_herkunft": "Herkunft",
        "sob_vielfalt": "Vielfalt",
        "sob_authentisch": "Authentisch",
    },
}

COL_SUPPORT_GEWUENSCHT  = "open_support_gewuenscht"
COL_HILFT               = "open_was_hilft"
COL_ZUGEHOERIG_POS      = "open_zugehoerig_positiv"
COL_ZUGEHOERIG_NEG      = "open_zugehoerig_negativ"
COL_WUENSCHE            = "open_wuensche"