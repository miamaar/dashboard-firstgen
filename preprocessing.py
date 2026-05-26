# preprocessing.py
# Spalten-Mapping basierend auf echten Google-Forms-Spaltennamen
 
import pandas as pd
import numpy as np
from pathlib import Path
from config import *
 
# ── EXAKTES SPALTEN-MAPPING (Google Forms → interne Namen) ──────────────────
COLUMN_MAP = {
    # Sense of Belonging — Allgemein
    "Ich fühle mich an meiner Hochschule willkommen.":                              "sob_willkommen",
    "Ich habe das Gefühl, dass ich als Student:in hier dazugehöre.":               "sob_dazugehoeren",
    "Ich empfinde ein Zugehörigkeitsgefühl gegenüber meiner Studienrichtung.":     "sob_studienricht",
    "Ich werde als Person an der Hochschule wahrgenommen und respektiert.":        "sob_respektiert",
    "Ich identifiziere mich mit der Kultur und den Werten meiner Hochschule.":     "sob_identifikation",
    # Sense of Belonging — Sozial
    "Ich habe im Studium Freundschaften oder soziale Kontakte geknüpft.":          "sob_freundschaft",
    "Ich fühle mich in der Studierendenschaft gut integriert.":                    "sob_integration",
    "Ich habe Mitstudierende, mit denen ich offen über Herausforderungen sprechen kann.": "sob_offen",
    "In Gruppenarbeiten oder im Unterricht fühle ich mich ernst genommen und einbezogen.": "sob_ernst",
    "Ich weiss, wo ich soziale Unterstützung an der Hochschule finden kann.":      "sob_support_kennen",
    "Ich habe im Studium Personen, an die ich mich bei persönlichen oder sozialen Unsicherheiten wenden kann.": "sob_ansprechperson",
    # Sense of Belonging — Akademisch
    "Ich fühle mich im Unterricht / in Lehrveranstaltungen respektiert.":          "sob_unterricht",
    "Ich habe das Gefühl, dass meine Sichtweisen und Beiträgen von Dozierenden gehört werden.": "sob_sichtweisen",
    "Ich kann Fragen stellen oder Beiträge leisten, ohne mich unwohl zu fühlen.":  "sob_fragen",
    "Die Hochschule unterstützt mich in meiner persönlichen und akademischen Entwicklung.": "sob_entwicklung",
    "Ich weiss, an wen ich mich bei fachlichen Fragen oder Unsicherheiten wenden kann.": "sob_fachlich",
    # Sense of Belonging — Identität
    "Meine Herkunft, Sprache oder soziale Situation werden an der Hochschule respektiert.": "sob_herkunft",
    "Ich habe das Gefühl, dass Vielfalt im Studium wertgeschätzt wird.":           "sob_vielfalt",
    "Ich kann mich im Hochschulalltag authentisch zeigen, ohne mich verstellen zu müssen.": "sob_authentisch",
    # FGS-Status
    "Sind Sie die erste Person in Ihrer Familie, die ein Hochschulstudium absolviert?": "fgs_status",
    # Herausforderungen (Matrix-Fragen)
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Finanzielle Belastung]":          "ch_finanzen",
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Zeitdruck durch Arbeit]":         "ch_zeitdruck",
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Unsicherheit im Studium]":        "ch_unsicherheit",
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Fehlendes Zugehörigkeitsgefühl]": "ch_zugehoerigkeit",
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Fehlende Informationen zum Studium]": "ch_information",
    "Wie stark treffen folgende Herausforderungen auf Sie zu?  [Akademische Anforderungen]":      "ch_akademisch",
    # FGS Likert-Items
    "Meine Familie kann mich bei studienbezogenen Fragen unterstützen.": "fgs_familie_support",
    "Ich habe das Gefühl, mehr leisten zu müssen als andere.":           "fgs_mehr_leisten",
    "Finanzielle Sorgen beeinflussen mein Studium.":                     "fgs_fin_sorgen",
    # Offene Fragen
    "Was waren wichtige Gründe für Ihr Studium?":                        "open_gruende",
    "Wie hat Ihre Familie Ihre Entscheidung beeinflusst, ein Studium zu beginnen?": "open_familie_einfluss",
    "Wann empfanden Sie Ihr Studium bisher als besonders herausfordernd?": "open_herausfordernd_wann",
    "Welche Unterstützungsangebote kennen Sie?":                         "open_support_kennen",
    "Welche Angebote haben Sie genutzt?":                                "open_support_genutzt",
    "Welche Unterstützung hätten Sie sich gewünscht?":                   "open_support_gewuenscht",
    "Was hilft Ihnen im Studium besonders?":                             "open_was_hilft",
    # Soziodemografie
    "Haben Sie einen Migrationshintergrund?":                            "demog_migration",
    "Wie alt sind Sie?":                                                 "demog_alter",
    "Wie identifizieren Sie sich geschlechtlich?":                       "demog_geschlecht",
    "In welchem Jahr haben Sie Ihr Studium abgeschlossen bzw. werden es voraussichtlich abschliessen?": "demog_abschlussjahr",
    "Arbeiten Sie neben dem Studium?":                                   "demog_arbeit",
    "Welchen Studiengang studieren Sie?":                                "demog_studiengang",
    # Offene Abschlussfragen
    "Was hat Ihnen bisher geholfen, sich im Studium zugehörig zu fühlen?":         "open_zugehoerig_positiv",
    "Wann oder in welchen Situationen fühlen Sie sich nicht zugehörig?":           "open_zugehoerig_negativ",
    "Was wünschen Sie, um sich an der Hochschule wohler und integrierter zu fühlen?": "open_wuensche",
}
 
# Textwerte der Herausforderungen-Matrix → Zahlen
CHALLENGE_TEXT_MAP = {
    "Trifft gar nicht zu":   1,
    "Trifft eher nicht zu":  2,
    "Teils":                 3,
    "Trifft eher zu":        4,
    "Trifft voll und ganz zu": 5,
}
 
# Textwerte der Likert-Skala (1–5) → Zahlen
LIKERT_TEXT_MAP = {
    "Stimme gar nicht zu":      1,
    "1":                        1,
    "2":                        2,
    "3":                        3,
    "4":                        4,
    "5":                        5,
    "Stimme voll und ganz zu":  5,
}
 
 
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Bereinigt den Google-Forms-CSV und mappt Spalten auf interne Namen."""
 
    # 1. Timestamp entfernen
    df = df.drop(columns=["Timestamp", "Zeitstempel"], errors="ignore")
 
    # 2. Leerzeichen in Spaltennamen entfernen
    df.columns = [c.strip() for c in df.columns]
 
    # 3. Spalten umbenennen (Mapping anwenden)
    df = df.rename(columns=COLUMN_MAP)
 
    # 4. Herausforderungen: Text → Zahl
    # Robuster Apply statt dtype==object, weil pandas StringDtype != object
    ch_cols = list(CHALLENGES.values())
    for col in ch_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: CHALLENGE_TEXT_MAP.get(str(x).strip(), x) if pd.notna(x) else x
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. SoB-Spalten: Text → Zahl (robuster Apply)
    sob_cols = [c for g in SOB_GROUPS.values() for c in g]
    for col in sob_cols:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: LIKERT_TEXT_MAP.get(str(x).strip(), x) if pd.notna(x) else x
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. FGS-Likert: Text → Zahl (robuster Apply)
    for col in FGS_LIKERT.values():
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: LIKERT_TEXT_MAP.get(str(x).strip(), x) if pd.notna(x) else x
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
 
    # 7. Alter numerisch
    if COL_ALTER in df.columns:
        df[COL_ALTER] = pd.to_numeric(df[COL_ALTER], errors="coerce")
 
    # 8. FGS-Status bereinigen
    if COL_FGS in df.columns:
        df[COL_FGS] = df[COL_FGS].astype(str).str.strip()
 
    # 9. Abschlussjahr numerisch
    if COL_ABSCHLUSSJAHR in df.columns:
        df[COL_ABSCHLUSSJAHR] = pd.to_numeric(df[COL_ABSCHLUSSJAHR], errors="coerce")
 
    return df
 
 
def load_data() -> pd.DataFrame:
    """Lädt echten CSV oder erstellt Beispieldaten."""
    csv_path = Path("data/raw/survey.csv")
    if csv_path.exists():
        try:
            df = pd.read_csv(csv_path)
            df = clean_data(df)
            if COL_FGS in df.columns:
                print(f"Echte Daten geladen: {len(df)} Antworten")
                return df
        except Exception as e:
            print(f"Fehler beim Laden: {e}")
    print("Keine CSV gefunden — Beispieldaten werden verwendet.")
    return create_dummy_data()
 
 
def create_dummy_data(n: int = 80) -> pd.DataFrame:
    """Erstellt realistische Beispieldaten zum Testen."""
    np.random.seed(42)
    fgs = np.random.choice(["Ja", "Nein", "Unsicher"], n, p=[0.4, 0.5, 0.1])
    fgs_mask = fgs == "Ja"
 
    data = {
        COL_FGS:           fgs,
        COL_GESCHLECHT:    np.random.choice(["Weiblich", "Männlich", "Nicht-binär"], n, p=[0.45, 0.50, 0.05]),
        COL_ALTER:         np.random.randint(19, 35, n),
        COL_STUDIENGANG:   np.random.choice(["Informatik", "Wirtschaftsinformatik", "Data Science"], n),
        COL_ABSCHLUSSJAHR: np.random.choice([2025, 2026, 2027], n),
        COL_MIGRATION:     np.random.choice(["Ja", "Nein"], n, p=[0.35, 0.65]),
        COL_ARBEIT:        np.random.choice(["Vollzeit (>50%)", "Teilzeit (≤50%)", "Nicht erwerbstätig"],
                                            n, p=[0.1, 0.5, 0.4]),
        COL_HERAUSFORDERND: np.random.choice(
            ["Studienstart", "Prüfungsphase", "Mitte Studium", "Abschlussphase", "Keine"], n
        ),
    }
    for col in CHALLENGES.values():
        base  = np.random.randint(1, 6, n)
        boost = np.where(fgs_mask, np.random.randint(0, 2, n), 0)
        data[col] = np.clip(base + boost, 1, 5)
 
    for col in FGS_LIKERT.values():
        data[col] = np.random.randint(1, 6, n)
 
    for group_cols in SOB_GROUPS.values():
        for col in group_cols:
            base    = np.random.randint(2, 6, n)
            penalty = np.where(fgs_mask, np.random.randint(0, 2, n), 0)
            data[col] = np.clip(base - penalty, 1, 5)
 
    data[COL_HILFT]              = np.random.choice(
        ["Kommilitonen", "Dozierende", "Online-Ressourcen", "Familie", "Beratung", ""], n)
    data[COL_SUPPORT_GEWUENSCHT] = np.random.choice(
        ["Mentoring", "Finanzielle Hilfe", "Mehr Infos", "Peer-Support", ""], n)
    data[COL_ZUGEHOERIG_POS]     = np.random.choice(
        ["Gruppenarbeiten", "Dozierende", "Events", "Freunde", ""], n)
    data[COL_ZUGEHOERIG_NEG]     = np.random.choice(
        ["Prüfungszeit", "Studienstart", "Abgabefristen", ""], n)
    data[COL_WUENSCHE]           = np.random.choice(
        ["Mentoring", "Finanzielle Beratung", "Mehr Austausch", ""], n)
 
    return pd.DataFrame(data)
 
 
def calculate_belonging_scores(df: pd.DataFrame) -> dict:
    """Berechnet den mittleren SoB-Score je Dimension."""
    scores = {}
    for group_name, group_cols in SOB_GROUPS.items():
        available = [c for c in group_cols if c in df.columns]
        if available:
            scores[group_name] = round(df[available].mean().mean(), 2)
    if scores:
        scores["Gesamt"] = round(np.mean(list(scores.values())), 2)
    return scores
 
 
def apply_privacy_threshold(df: pd.DataFrame):
    """Gibt None zurück wenn Fallzahl zu klein."""
    return None if len(df) < MIN_N else df