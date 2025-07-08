# Mix Server - Lokales MCP-System

Ein vollständig lokales MCP (Model Context Protocol) System mit Server und Client, das mit Ollama und LlamaIndex arbeitet.

## Überblick

Dieses Projekt demonstriert, wie man ein komplettes lokales MCP-System baut, das:
- Einen MCP-Server mit benutzerdefinierten Tools für CSV- und Parquet-Dateien
- Einen lokalen Client mit LlamaIndex und Ollama
- Vollständig lokale Verarbeitung ohne externe API-Aufrufe

## Projektstruktur

```
mix_server/
│
├── data/                 # Beispiel-CSV- und Parquet-Dateien
│   ├── sample.csv
│   └── sample.parquet
│
├── tools/                # MCP-Tool-Definitionen
│   ├── __init__.py
│   ├── csv_tools.py
│   └── parquet_tools.py
│
├── utils/                # Wiederverwendbare Datei-Leselogik
│   ├── __init__.py
│   └── file_reader.py
│
├── server.py             # MCP-Server-Instanz
├── main.py               # Server-Einstiegspunkt
├── client.py             # Lokaler MCP-Client
├── generate_parquet.py   # Hilfsskript für Parquet-Datei
└── README.md             # Diese Datei
```

## Installation und Setup

### Voraussetzungen

1. **Ollama installieren**
   ```bash
   # Gehe zu https://ollama.ai und folge den Anweisungen
   ollama pull llama3.2
   ```

2. **Python-Abhängigkeiten installieren**
   ```bash
   uv add "mcp[cli]" pandas pyarrow llama-index llama-index-llms-ollama llama-index-tools-mcp nest-asyncio
   ```

3. **Parquet-Datei generieren**
   ```bash
   uv run generate_parquet.py
   ```

## Verwendung

### 1. MCP-Server starten

```bash
uv run main.py
```

### 2. Ollama-Service starten (falls nicht laufend)

```bash
ollama serve
```

### 3. Client starten

```bash
uv run client.py
```

## Verfügbare Tools

- **summarize_csv_file**: Liest und fasst CSV-Dateien zusammen
- **summarize_parquet_file**: Liest und fasst Parquet-Dateien zusammen

## Beispiel-Interaktionen

```
💬 Gib deine Nachricht ein: Fasse die CSV-Datei namens sample.csv zusammen
💬 Gib deine Nachricht ein: Vergleiche sample.csv und sample.parquet
💬 Gib deine Nachricht ein: Wie viele Zeilen hat sample.csv?
```

## Erweiterung

Das System ist modular aufgebaut und kann einfach erweitert werden:

1. **Neue Tools hinzufügen**: Erstelle neue Python-Dateien im `tools/`-Ordner
2. **Neue Datenformate unterstützen**: Erweitere die `utils/file_reader.py`
3. **Neue Funktionalitäten**: Füge Datenbank-Zugriff, API-Calls oder andere Features hinzu

## Funktionsweise

1. Der MCP-Server stellt Tools über das Model Context Protocol zur Verfügung
2. Der Client verbindet sich mit dem Server und ruft verfügbare Tools ab
3. Ein lokales LLM (über Ollama) entscheidet, welche Tools aufgerufen werden
4. LlamaIndex orchestriert die Kommunikation zwischen LLM, Client und Server
5. Alle Daten bleiben vollständig lokal auf deinem System

## Fehlerbehebung

- **Server-Verbindungsfehler**: Stelle sicher, dass der Server auf Port 8000 läuft
- **Ollama-Probleme**: Überprüfe mit `ollama list`, ob das Modell verfügbar ist
- **Import-Fehler**: Führe `uv sync` aus, um alle Abhängigkeiten zu installieren