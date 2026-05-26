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

# ── QUALITATIVE CODIERUNG (manuell editierbar) ──────────────────────────────
# Format: {exakte Antwort aus CSV: Kategorie}  |  None = nicht anzeigen
# → Hier prüfen und anpassen, nachdem neue Daten importiert wurden.

CODING_POS = {
    "Gute Leute um sich herum zu haben":
        "Kontakt zu Mitstudierenden",
    "Ich empfinde nicht wirklich eine zugehörigkeit zu meinem Studium.":
        None,   # fehlcodiert: keine Ressource; für manuelle Prüfung markiert
    "Präsenzunterricht (man sieht mal alle Gesichter)":
        "Präsenz & Begegnung",
    "Meine Mitstudierenden":
        "Kontakt zu Mitstudierenden",
    "Austausch mit anderen Studierenden":
        "Kontakt zu Mitstudierenden",
    "Ungezwungene Gruppenarbeiten":
        "Gemeinsame Aktivitäten",
    "Zeit mit anderen Studenten verbringen":
        "Kontakt zu Mitstudierenden",
    'Die richtigen Freunde zu finden, die auf der gleichen "Wellenlänge" sind und unter gleichen Umständen studieren.':
        "Kontakt zu Mitstudierenden",
    "Die anderen Studenten":
        "Kontakt zu Mitstudierenden",
    "freunde / mitstudierende":
        "Kontakt zu Mitstudierenden",
    "neue freunde":
        "Kontakt zu Mitstudierenden",
    "Harzhi":
        None,   # identifizierend (Name), nicht auswertbar
}

CODING_NEG = {
    "Wenn ich mit Herr Sucur rede.":
        None,   # identifizierend (Name), nicht direkt auswertbar
    "Sehr häufig wenn ich Pflichtmodule besuchen muss, welche für mich persönlich nicht relevant für meinen Arbeitsaltag sind(Systemtechnik vs. Softwareentwicklung)":
        "Wenig passende Pflichtmodule",
    "ich kenne keine konkrete Situation, aber das Imposter-syndrom ist massiv während der Prüfungsphase....":
        "Imposter-Syndrom & Leistungsdruck",
    "Wenn keine Transparenz durch Dozierende betreffend Modulaufbau und -ablauf gemacht werden, da ich als Teilzeitstudent nicht jede Vorlesung immer besuchen kann. ":
        "Fehlende Transparenz & Teilzeit",
    "Wenn wir teilzeitstundenten systematisch von infoanlässen ausgeschlossen werden":
        "Fehlende Transparenz & Teilzeit",
    "Spontane Gruppenübungen":
        "Spontane Gruppenarbeiten",
    "Wenn ich mich mit anderen Studierenden vergleiche":
        "Imposter-Syndrom & Leistungsdruck",
    "Nie":
        None,   # keine Barriere genannt
    "wenn ich nicht verstehe um was es geht, und die privaten Interessen oder der Humor der Mitstudierenden und mir sich grundlegend unterscheiden, was aber im Ordnung ist. Es stört mich nicht.":
        "Unterschiedliche Interessen",
    "Bei Informatik studis ":
        None,   # zu vage, für manuelle Prüfung markiert
}

CODING_WUENSCHE = {
    "Noch mehr Partys.":
        "Mehr Veranstaltungen & Kennenlernangebote",
    "Mehr Kennenlern-Momente":
        "Mehr Veranstaltungen & Kennenlernangebote",
    "Weniger Pflichtmodule und mehr Module welche dadurch frei gewählt werden können und eine in seinem persönlichen Kariereweg wirklich weiterbringen.":
        "Mehr Wahlfreiheit bei Modulen",
    "Ich habe aktuell nicht die Kapazität mich mit dieser Frage zu beschäftigen, ich wünschte ich hätte eine Antwort...":
        None,   # keine auswertbare Aussage
    "Transparenz betreffend Modulen, also Ablauf des Semester, behandelte Themen":
        "Mehr Transparenz zu Modulen",
    "Am besten, in dem mann rücksicht auf teilzeit studenten nimmt":
        "Mehr Rücksicht auf Teilzeitstudierende",
    "-":
        None,   # keine Aussage
    "Passt so wie es ist":
        None,   # kein Wunsch geäussert
    "Mehr Events":
        "Mehr Veranstaltungen & Kennenlernangebote",
}

# Anonymisierte Beispielaussagen – manuell geprüft und generalisiert.
# Keine Namen, keine konkreten Modulnummern, keine eindeutig identifizierenden Details.
ANON_EXAMPLES = {
    "pos": [
        "Austausch mit anderen Studierenden und das Knüpfen von Freundschaften.",
        "Gemeinsame, ungezwungene Gruppenarbeiten.",
    ],
    "neg": [
        "Das Imposter-Syndrom ist besonders während der Prüfungsphase stark spürbar.",
        "Als Teilzeitstudierende*r von Informationsveranstaltungen ausgeschlossen zu werden.",
    ],
    "wuensche": [
        "Mehr Transparenz zum Modulaufbau und den behandelten Themen im Semester.",
        "Mehr Kennenlernangebote und soziale Veranstaltungen.",
    ],
}