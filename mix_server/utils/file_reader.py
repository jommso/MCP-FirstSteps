# utils/file_reader.py

import pandas as pd
from pathlib import Path

# Basisverzeichnis, wo unsere Daten liegen
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def read_csv_summary(filename: str) -> str:
    """
    Eine CSV-Datei lesen und eine einfache Zusammenfassung zurückgeben.
    
    Args:
        filename: Name der CSV-Datei (z.B. 'sample.csv')
        
    Returns:
        Ein String, der den Inhalt der Datei beschreibt.
    """
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"Datei '{filename}' nicht im Datenverzeichnis gefunden."
    
    try:
        df = pd.read_csv(file_path)
        summary = f"CSV-Datei '{filename}' hat {len(df)} Zeilen und {len(df.columns)} Spalten.\n"
        summary += f"Spalten: {', '.join(df.columns.tolist())}\n"
        summary += f"Erste paar Zeilen:\n{df.head().to_string()}"
        return summary
    except Exception as e:
        return f"Fehler beim Lesen der CSV-Datei '{filename}': {str(e)}"

def read_parquet_summary(filename: str) -> str:
    """
    Eine Parquet-Datei lesen und eine einfache Zusammenfassung zurückgeben.
    
    Args:
        filename: Name der Parquet-Datei (z.B. 'sample.parquet')
        
    Returns:
        Ein String, der den Inhalt der Datei beschreibt.
    """
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"Datei '{filename}' nicht im Datenverzeichnis gefunden."
    
    try:
        df = pd.read_parquet(file_path)
        summary = f"Parquet-Datei '{filename}' hat {len(df)} Zeilen und {len(df.columns)} Spalten.\n"
        summary += f"Spalten: {', '.join(df.columns.tolist())}\n"
        summary += f"Erste paar Zeilen:\n{df.head().to_string()}"
        return summary
    except Exception as e:
        return f"Fehler beim Lesen der Parquet-Datei '{filename}': {str(e)}"
