import streamlit as st
import pandas as pd
from pathlib import Path
from src.preprocessing import load_and_clean

RAW_PATH = Path("data/raw/survey.csv")

@st.cache_data
def load_data() -> pd.DataFrame:
    if not RAW_PATH.exists():
        st.error(f"Datei nicht gefunden: {RAW_PATH}")
        st.stop()
    return load_and_clean(str(RAW_PATH))