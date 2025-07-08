# tools/csv_tools.py

from server import mcp
from utils.file_reader import read_csv_summary

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Eine CSV-Datei zusammenfassen, indem die Anzahl der Zeilen, Spalten gemeldet und eine Vorschau gezeigt wird.
    
    Args:
        filename: Name der CSV-Datei im /data-Verzeichnis (z.B. 'sample.csv')
        
    Returns:
        Ein String, der den Inhalt und die Struktur der Datei beschreibt.
    """
    return read_csv_summary(filename)
