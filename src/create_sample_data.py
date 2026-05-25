# create_sample_data.py
# Nur zum Testen! Generiert realistische Beispieldaten.
import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)
n = 80

data = {
    "fgs_status": np.random.choice(["Ja", "Nein", "Unsicher"], n, p=[0.4, 0.5, 0.1]),
    "demog_geschlecht": np.random.choice(["Weiblich", "Männlich", "Nicht-binär"], n, p=[0.45, 0.50, 0.05]),
    "demog_alter": np.random.randint(19, 35, n),
    "demog_studiengang": np.random.choice(["Informatik", "Wirtschaftsinformatik", "Data Science"], n),
    "demog_abschlussjahr": np.random.choice([2025, 2026, 2027], n),
    "demog_migration": np.random.choice(["Ja", "Nein"], n, p=[0.35, 0.65]),
    "demog_arbeit": np.random.choice(["Ja, Vollzeit", "Ja, Teilzeit", "Nein"], n, p=[0.1, 0.5, 0.4]),
    # Herausforderungen
    "ch_finanzen":        np.random.randint(1, 6, n),
    "ch_zeitdruck":       np.random.randint(1, 6, n),
    "ch_unsicherheit":    np.random.randint(1, 6, n),
    "ch_zugehoerigkeit":  np.random.randint(1, 6, n),
    "ch_information":     np.random.randint(1, 6, n),
    "ch_akademisch":      np.random.randint(1, 6, n),
    # FGS Likert
    "fgs_familie_support": np.random.randint(1, 6, n),
    "fgs_mehr_leisten":    np.random.randint(1, 6, n),
    "fgs_fin_sorgen":      np.random.randint(1, 6, n),
    # Sense of Belonging
    "sob_willkommen":      np.random.randint(1, 6, n),
    "sob_dazugehoeren":    np.random.randint(1, 6, n),
    "sob_studienricht":    np.random.randint(1, 6, n),
    "sob_respektiert":     np.random.randint(1, 6, n),
    "sob_identifikation":  np.random.randint(1, 6, n),
    "sob_freundschaft":    np.random.randint(1, 6, n),
    "sob_integration":     np.random.randint(1, 6, n),
    "sob_offen":           np.random.randint(1, 6, n),
    "sob_ernst":           np.random.randint(1, 6, n),
    "sob_support_kennen":  np.random.randint(1, 6, n),
    "sob_ansprechperson":  np.random.randint(1, 6, n),
    "sob_unterricht":      np.random.randint(1, 6, n),
    "sob_sichtweisen":     np.random.randint(1, 6, n),
    "sob_fragen":          np.random.randint(1, 6, n),
    "sob_entwicklung":     np.random.randint(1, 6, n),
    "sob_fachlich":        np.random.randint(1, 6, n),
    "sob_herkunft":        np.random.randint(1, 6, n),
    "sob_vielfalt":        np.random.randint(1, 6, n),
    "sob_authentisch":     np.random.randint(1, 6, n),
    # Offene Fragen (Beispiele)
    "open_was_hilft": np.random.choice([
        "Kommilitonen", "Dozierende", "Familie", "Online-Ressourcen", ""
    ], n),
    "open_support_gewuenscht": np.random.choice([
        "Mentoring", "Finanzielle Hilfe", "Mehr Information", ""
    ], n),
}

Path("data/raw").mkdir(parents=True, exist_ok=True)
pd.DataFrame(data).to_csv("data/raw/survey.csv", index=False)
print("✅ Beispieldaten erstellt: data/raw/survey.csv")