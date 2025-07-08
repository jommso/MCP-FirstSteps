# tools/parquet_tools.py

from server import mcp
from utils.file_reader import read_parquet_summary

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Eine Parquet-Datei zusammenfassen, indem die Anzahl der Zeilen, Spalten gemeldet und eine Vorschau gezeigt wird.
    
    Args:
        filename: Name der Parquet-Datei im /data-Verzeichnis (z.B. 'sample.parquet')
        
    Returns:
        Ein String, der den Inhalt und die Struktur der Datei beschreibt.
    """
    return read_parquet_summary(filename)
