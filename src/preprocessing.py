# src/preprocessing.py
import pandas as pd
import re
from config import (
    COL_FGS, CHALLENGES, FGS_LIKERT,
    SOB_GENERAL, SOB_SOCIAL, SOB_ACADEMIC, SOB_IDENTITY,
    COL_MIGRATION, COL_ALTER, COL_GESCHLECHT,
    COL_ABSCHLUSSJAHR, COL_ARBEIT, COL_STUDIENGANG,
    COL_GRUENDE, COL_FAMILIE_EINFL, COL_HERAUSFORDER,
    COL_SUPPORT_KENNT, COL_SUPPORT_GENUTZT,
    COL_SUPPORT_GEWUENSCHT, COL_HILFT,
    COL_ZUGEHOERIG_POS, COL_ZUGEHOERIG_NEG, COL_WUENSCHE,
)


def _strip(text: str) -> str:
    """Leerzeichen und Sonderzeichen am Rand entfernen."""
    return text.strip().rstrip("*").strip()


def build_column_map(df: pd.DataFrame) -> dict:
    """
    Mappt die langen Google-Forms-Spaltenüberschriften auf kurze interne Namen.
    Matching über Keywords — robust gegenüber kleinen Formulierungsänderungen.
    """
    mapping = {}
    cols = {_strip(c): c for c in df.columns}

    def find(keyword: str) -> str | None:
        for stripped, original in cols.items():
            if keyword.lower() in stripped.lower():
                return original
        return None

    # FGS-Status
    col = find("erste Person in Ihrer Familie")
    if col:
        mapping[col] = COL_FGS

    # Herausforderungen-Matrix
    challenge_keys = {
        "Finanzielle Belastung":         "Finanzielle Belastung",
        "Zeitdruck durch Arbeit":         "Zeitdruck",
        "Unsicherheit im Studium":        "Unsicherheit im Studium",
        "Fehlendes Zugehörigkeitsgefühl": "Zugehörigkeitsgefühl",
        "Fehlende Informationen":         "Informationen zum Studium",
        "Akademische Anforderungen":      "Akademische Anforderungen",
    }
    short_names = list(CHALLENGES.values())
    for i, keyword in enumerate(challenge_keys.values()):
        col = find(keyword)
        if col:
            mapping[col] = short_names[i]

    # FGS Likert-Items
    fgs_likert_map = {
        "Familie kann mich bei studienbezogenen": "fgs_familie_support",
        "mehr leisten zu müssen":                 "fgs_mehr_leisten",
        "Finanzielle Sorgen beeinflussen":        "fgs_fin_sorgen",
    }
    for keyword, short in fgs_likert_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # SoB — Allgemein
    sob_gen_map = {
        "fühle mich an meiner Hochschule willkommen": "sob_willkommen",
        "als Student:in hier dazugehöre":              "sob_dazugehoeren",
        "Zugehörigkeitsgefühl gegenüber meiner Studienrichtung": "sob_studienricht",
        "als Person an der Hochschule wahrgenommen":   "sob_respektiert",
        "Kultur und den Werten":                       "sob_identifikation",
    }
    for keyword, short in sob_gen_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # SoB — Sozial
    sob_soc_map = {
        "Freundschaften oder soziale Kontakte":        "sob_freundschaft",
        "in der Studierendenschaft gut integriert":    "sob_integration",
        "offen über Herausforderungen":                "sob_offen",
        "Gruppenarbeiten":                             "sob_ernst",
        "soziale Unterstützung an der Hochschule finden": "sob_support_kennen",
        "persönlichen oder sozialen Unsicherheiten":   "sob_ansprechperson",
    }
    for keyword, short in sob_soc_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # SoB — Akademisch
    sob_ac_map = {
        "Im Unterricht":                              "sob_unterricht",
        "Sichtweisen und Beiträgen":                  "sob_sichtweisen",
        "Fragen stellen oder Beiträge leisten":       "sob_fragen",
        "unterstützt mich in meiner persönlichen":    "sob_entwicklung",
        "fachlichen Fragen oder Unsicherheiten":      "sob_fachlich",
    }
    for keyword, short in sob_ac_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # SoB — Identität
    sob_id_map = {
        "Herkunft, Sprache oder soziale Situation":   "sob_herkunft",
        "Vielfalt im Studium":                         "sob_vielfalt",
        "authentisch zeigen":                          "sob_authentisch",
    }
    for keyword, short in sob_id_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # Demografie
    demog_map = {
        "Migrationshintergrund":         COL_MIGRATION,
        "Wie alt sind Sie":              COL_ALTER,
        "geschlechtlich":                COL_GESCHLECHT,
        "Studium abgeschlossen":         COL_ABSCHLUSSJAHR,
        "neben dem Studium":             COL_ARBEIT,
        "Studiengang":                   COL_STUDIENGANG,
    }
    for keyword, short in demog_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    # Offene Fragen
    open_map = {
        "wichtige Gründe für Ihr Studium":         COL_GRUENDE,
        "Familie Ihre Entscheidung beeinflusst":   COL_FAMILIE_EINFL,
        "besonders herausfordernd":                COL_HERAUSFORDER,
        "Unterstützungsangebote kennen":           COL_SUPPORT_KENNT,
        "Angebote haben Sie genutzt":              COL_SUPPORT_GENUTZT,
        "Unterstützung hätten Sie sich gewünscht": COL_SUPPORT_GEWUENSCHT,
        "hilft Ihnen im Studium":                  COL_HILFT,
        "geholfen, sich im Studium zugehörig":     COL_ZUGEHOERIG_POS,
        "nicht zugehörig":                         COL_ZUGEHOERIG_NEG,
        "wünschen, um sich":                       COL_WUENSCHE,
    }
    for keyword, short in open_map.items():
        col = find(keyword)
        if col:
            mapping[col] = short

    return mapping


def load_and_clean(csv_path: str) -> pd.DataFrame:
    """
    Lädt den Google-Forms-CSV, benennt Spalten um und konvertiert Datentypen.
    Gibt einen bereinigten DataFrame zurück.
    """
    df = pd.read_csv(csv_path)

    # Timestamp-Spalte entfernen (Google Forms fügt diese automatisch ein)
    if "Timestamp" in df.columns or "Zeitstempel" in df.columns:
        df = df.drop(columns=["Timestamp", "Zeitstempel"], errors="ignore")

    # Spalten umbenennen
    col_map = build_column_map(df)
    df = df.rename(columns=col_map)

    # Likert-Spalten: Strings → Integer (Google Forms exportiert manchmal als Text)
    likert_cols = (
        list(CHALLENGES.values())
        + list(FGS_LIKERT.values())
        + list(SOB_GENERAL.values())
        + list(SOB_SOCIAL.values())
        + list(SOB_ACADEMIC.values())
        + list(SOB_IDENTITY.values())
    )
    for col in likert_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Alter: String → numerisch
    if COL_ALTER in df.columns:
        df[COL_ALTER] = pd.to_numeric(df[COL_ALTER], errors="coerce")

    # FGS-Spalte: einheitliche Werte sicherstellen
    if COL_FGS in df.columns:
        df[COL_FGS] = df[COL_FGS].str.strip()

    return df


def get_fgs_df(df: pd.DataFrame) -> pd.DataFrame:
    """Gibt nur die FGS-Antwortenden zurück."""
    if COL_FGS not in df.columns:
        return df
    return df[df[COL_FGS].str.lower() == "ja"].copy()


def get_non_fgs_df(df: pd.DataFrame) -> pd.DataFrame:
    """Gibt nur die Nicht-FGS-Antwortenden zurück."""
    if COL_FGS not in df.columns:
        return df
    return df[df[COL_FGS].str.lower() == "nein"].copy()