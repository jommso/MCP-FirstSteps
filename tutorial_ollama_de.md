# Dein erstes lokales MCP-System bauen: Server + Client mit Ollama

Das werden wir bauen:

- Einen kleinen MCP-Server mit Python und dem MCP SDK mit zwei nützlichen Tools, die Daten lesen aus:
  - Einer CSV-Datei (ideal für Tabellenkalkulationen und tabellarische Daten)
  - Einer Parquet-Datei (ein Format, das oft in der Datentechnik und Analytik verwendet wird)
- Einen lokalen MCP-Client mit LlamaIndex und Ollama, der sich mit deinem Server verbindet
- Ein vollständig lokales KI-System, das auf deinem Rechner läuft, ohne Daten an externe Dienste zu senden
- Eine saubere Ordnerstruktur, die es einfach macht, neue Tools oder Features hinzuzufügen

Du wirst deiner lokalen KI solche Fragen stellen können: 
> "Fasse den Inhalt meiner Datendatei zusammen" 
> "Wie viele Zeilen und Spalten hat diese CSV?"

## Warum hier anfangen?
Dieses Tutorial ist perfekt für dich, wenn:

- Du KI-Tools bauen möchtest, die vollständig offline arbeiten und deine Daten privat halten
- Du neugierig auf MCP bist und sehen möchtest, wie es in der Praxis mit lokalen LLMs funktioniert
- Du einen soliden Ausgangspunkt für das Bauen fortgeschrittener Tool-Server und -Clients möchtest

Wir verwenden reines Python, pandas und lokale LLM-Tools wie Ollama und LlamaIndex, ohne Web-Frameworks oder Cloud-Dienste. Alles läuft lokal auf deinem Rechner.

Am Ende wirst du einen vollständig funktionierenden lokalen MCP-Server und -Client haben, plus ein besseres Verständnis dafür, wie man KI-Tools erstellt, die über Textvorhersage hinausgehen — und tatsächlich nützliche Arbeit leisten, während deine Daten vollständig privat bleiben.

Lass uns anfangen!

## Was ist MCP (und warum sollte es dich interessieren)?
Lass uns das aufschlüsseln, bevor wir mit dem Programmieren beginnen.

MCP steht für Model Context Protocol. Es ist eine Möglichkeit, KI-Anwendungen sicher mit externen Daten und benutzerdefinierten Tools interagieren zu lassen, die du definierst.

Stell es dir wie das Bauen deiner eigenen Mini-API vor — aber anstatt sie dem ganzen Internet zugänglich zu machen, stellst du sie einem lokalen KI-Assistenten zur Verfügung, der auf deinem Rechner läuft.

Mit MCP kannst du:

- Dein lokales LLM eine Datei lesen oder eine Datenbank abfragen lassen
- Tools erstellen, die nützliche Dinge tun (wie einen Datensatz zusammenfassen oder eine API abrufen)
- Wiederverwendbare Prompts hinzufügen, um zu steuern, wie sich deine KI in bestimmten Aufgaben verhält

Für dieses Projekt konzentrieren wir uns auf Tools — den Teil von MCP, der es dir ermöglicht, kleine Python-Funktionen zu schreiben, die ein lokales LLM aufrufen kann.

## Was wir bauen
Hier ist eine kurze Vorschau darauf, was du am Ende haben wirst:

- Einen lokalen MCP-Server namens `mix_server`
- Zwei Tools: eines, das eine CSV-Datei liest, und eines, das eine Parquet-Datei liest
- Einen lokalen MCP-Client mit LlamaIndex, der sich mit deinem Server verbindet
- Ollama, das ein lokales LLM (wie Llama 3.2) betreibt, um den Client zu steuern
- Ein sauberes, modulares Ordnerlayout, sodass du einfach weitere Tools hinzufügen kannst
- Ein vollständig lokales System, mit dem du mit deinen Daten in natürlicher Sprache chatten kannst

Lass uns mit der Einrichtung deines Projekts beginnen.

## Projekt-Setup (Schritt-für-Schritt)
Wir verwenden uv — einen schnellen, modernen Python-Projektmanager — um unsere Umgebung zu erstellen und zu verwalten. Er handhabt Abhängigkeiten, virtuelle Umgebungen und Skriptausführung, alles an einem Ort.

Wenn du schon einmal pip oder virtualenv verwendet hast, ist uv wie beide zusammen — aber viel schneller und ergonomischer.

### Schritt 1: Ollama installieren
Zuerst müssen wir Ollama installieren, um lokale LLMs auszuführen. Gehe zu [ollama.ai](https://ollama.ai) und folge den Installationsanweisungen für dein Betriebssystem.

Nach der Installation lade ein geeignetes Modell herunter:

```bash
ollama pull llama3.2
```

Dies lädt das Llama 3.2-Modell herunter, das gut für Tool-Calling-Aufgaben funktioniert.

### Schritt 2: uv installieren
Alternativ lässt sich uv auch über pip installieren:
pip install uv

Um uv zu installieren, führe dies in deinem Terminal aus:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Für Windows (PowerShell):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Starte dann dein Terminal neu, damit der uv-Befehl verfügbar ist.

Du kannst überprüfen, ob es funktioniert mit:

```bash
uv --version
```

### Schritt 3: Das Projekt erstellen
Lass uns einen neuen Ordner für unser MCP-System erstellen:

```bash
uv init mix_server
cd mix_server
```

Dies erstellt ein einfaches Python-Projekt mit einer pyproject.toml-Datei zur Verwaltung von Abhängigkeiten.

### Schritt 4: Virtuelle Umgebung einrichten
Wir erstellen jetzt eine virtuelle Umgebung für unser Projekt:

```bash
uv venv
```

Unter Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

Unter Mac/Linux:
```bash
source .venv/bin/activate
```

Dies hält deine Abhängigkeiten vom Rest deines Systems isoliert.

### Schritt 5: Erforderliche Abhängigkeiten hinzufügen
Wir installieren die notwendigen Pakete:

- `mcp[cli]`: Das offizielle MCP SDK und Kommandozeilen-Tools
- `pandas`: Zum Lesen von CSV- und Parquet-Dateien
- `pyarrow`: Fügt Unterstützung für das Lesen von Parquet-Dateien über Pandas hinzu
- `llama-index`: Zum Bauen des MCP-Clients
- `llama-index-llms-ollama`: Ollama-Integration für LlamaIndex
- `llama-index-tools-mcp`: MCP-Tools-Integration für LlamaIndex
- `nest-asyncio`: Zum Ausführen von async-Code in Jupyter-ähnlichen Umgebungen

Installiere sie mit:

```bash
uv add "mcp[cli]" pandas pyarrow llama-index llama-index-llms-ollama llama-index-tools-mcp nest-asyncio
```

Dies aktualisiert deine pyproject.toml und installiert die Pakete in deine Umgebung.

### Schritt 6: Saubere Ordnerstruktur erstellen
Wir verwenden das folgende Layout, um organisiert zu bleiben:

```
mix_server/
│
├── data/                 # Beispiel-CSV- und Parquet-Dateien
│
├── tools/                # MCP-Tool-Definitionen
│
├── utils/                # Wiederverwendbare Datei-Leselogik
│
├── server.py             # Erstellt den MCP-Server
├── main.py               # Einstiegspunkt für den MCP-Server
├── client.py             # Lokaler MCP-Client mit LlamaIndex
└── README.md             # Optionale Dokumentation
```

Erstelle die Ordner:

```bash
mkdir data tools utils
```

Deine Umgebung ist jetzt bereit. Im nächsten Abschnitt erstellen wir ein paar kleine Datendateien, mit denen wir arbeiten können — eine CSV- und eine Parquet-Datei — und verwenden sie, um unsere Tools anzutreiben.

## Beispiel-Datendateien erstellen
Um unsere ersten Tools zu bauen, brauchen wir etwas, womit sie arbeiten können. In diesem Abschnitt erstellen wir zwei einfache Dateien:

- Eine CSV-Datei (ideal für Tabellenkalkulationen und tabellarische Daten)
- Eine Parquet-Datei (ein effizienteres Format, das in der Datentechnik verwendet wird)

Beide Dateien enthalten denselben Mock-Datensatz — eine kurze Liste von Benutzern. Du wirst diese Dateien später verwenden, wenn du Tools baust, die ihre Inhalte zusammenfassen.

### Schritt 1: Den data/ Ordner erstellen
Falls du den Ordner für unsere Daten noch nicht erstellt hast, tue es jetzt von deinem Projektverzeichnis aus:

```bash
mkdir data
```

### Schritt 2: Eine Beispiel-CSV-Datei erstellen
Jetzt fügen wir eine Beispiel-CSV-Datei mit einigen gefälschten Benutzerdaten hinzu.

Erstelle eine neue Datei namens `sample.csv` im `data/`-Ordner:

**data/sample.csv**
```csv
id,name,email,signup_date
1,Alice Johnson,alice@example.com,2023-01-15
2,Bob Smith,bob@example.com,2023-02-22
3,Carol Lee,carol@example.com,2023-03-10
4,David Wu,david@example.com,2023-04-18
5,Eva Brown,eva@example.com,2023-05-30
```

Diese Datei gibt uns strukturierte, lesbare Daten — perfekt für ein Tool zum Analysieren.

### Schritt 3: Die CSV in Parquet konvertieren
Wir erstellen jetzt eine Parquet-Version derselben Daten mit Python. Dies zeigt, wie einfach du beide Dateitypen in deinen Tools unterstützen kannst.

Erstelle ein kurzes Skript im Hauptverzeichnis deines Projekts namens `generate_parquet.py`:

```python
# generate_parquet.py

import pandas as pd

# CSV lesen
df = pd.read_csv("data/sample.csv")

# Als Parquet speichern
df.to_parquet("data/sample.parquet", index=False)

print("Parquet-Datei erfolgreich erstellt!")
```

Führe das Skript aus:

```bash
uv run generate_parquet.py
```

Danach sollte dein `data/`-Ordner so aussehen:

```
data/
├── sample.csv
└── sample.parquet
```

### Was ist der Unterschied zwischen CSV und Parquet?
- **CSV**: Einfache, menschenlesbare Textdatei. Ideal für kleine Datensätze und schnelle Inspektion.
- **Parquet**: Ein binäres, spaltenbasiertes Format. Viel schneller für große Datensätze und üblich in Analytics-Pipelines (z.B. mit Apache Spark oder Dremio).

Die Unterstützung beider Formate macht deine Tools flexibler, und dieses Beispiel zeigt, wie wenig zusätzlicher Aufwand dafür nötig ist.

Als Nächstes schreiben wir einige wiederverwendbare Hilfsfunktionen, die diese Dateien lesen und eine kurze Zusammenfassung ihrer Inhalte zurückgeben können — bereit, als MCP-Tools verpackt zu werden.

## Hilfsfunktionen zum Lesen von CSV- und Parquet-Dateien schreiben
Jetzt, da wir einige Daten haben, mit denen wir arbeiten können, schreiben wir die Kernlogik zum Lesen dieser Dateien und zur Rückgabe einer grundlegenden Zusammenfassung.

Wir werden diese Logik in eine separate Python-Datei unter einem Ordner namens `utils/` legen. Das macht es einfach, sie in verschiedenen Tools wiederzuverwenden, ohne Code zu duplizieren.

### Schritt 1: Das Hilfsprogramm-Modul erstellen
Falls du den `utils/`-Ordner noch nicht erstellt hast, tue es jetzt:

```bash
mkdir utils
```

Erstelle jetzt eine neue Python-Datei darin:

**utils/file_reader.py**

```python
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
```

### Wie das funktioniert
- Wir verwenden pandas zum Lesen von CSV- und Parquet-Dateien. Es ist eine bekannte Datenanalyse-Bibliothek in Python.
- `pathlib.Path` hilft uns, Dateipfade sicher über Betriebssysteme hinweg zu konstruieren.
- Beide Funktionen geben detaillierte Zusammenfassungen zurück, einschließlich Spalteninformationen und einer Vorschau der Daten.
- Wir schließen Fehlerbehandlung ein, um nützliches Feedback zu geben, wenn Dateien nicht existieren oder nicht gelesen werden können.

Das ist die gesamte Logik, die unsere Tools zunächst benötigen. Später, wenn du erweiterte Zusammenfassungen hinzufügen möchtest — wie das Erkennen von Null-Werten oder das Berechnen von Statistiken — kannst du diese Funktionen erweitern.

Mit unseren fertigen Hilfsprogrammen können wir sie jetzt als MCP-Tools verfügbar machen — damit unser lokales LLM sie tatsächlich verwenden kann!

## Datei-Reader als MCP-Tools verpacken
Jetzt, da wir die Logik zum Lesen und Zusammenfassen unserer Datendateien geschrieben haben, ist es Zeit, diese Funktionen unserem lokalen LLM durch MCP-Tools zur Verfügung zu stellen.

### Was ist ein MCP-Tool?
Ein MCP-Tool ist eine Python-Funktion, die du bei deinem MCP-Server registrierst und die die KI aufrufen kann, wenn sie eine Aktion ausführen muss — wie das Lesen einer Datei, das Abfragen einer API oder das Durchführen einer Berechnung.

Um ein Tool zu registrieren, dekorierst du die Funktion mit `@mcp.tool()`. Im Hintergrund generiert MCP eine Definition, die die KI sehen und mit der sie interagieren kann.

Aber bevor wir das tun, folgen wir einer bewährten Praxis: Wir definieren unsere MCP-Server-Instanz an einem zentralen Ort und importieren sie dann in jede Datei, die Tools definiert. Das stellt sicher, dass alles sauber und konsistent bleibt.

### Schritt 1: Die MCP-Server-Instanz definieren
Erstelle deine `server.py`-Datei mit folgendem Inhalt:

**server.py**
```python
# server.py

from mcp.server.fastmcp import FastMCP

# Das ist die geteilte MCP-Server-Instanz
mcp = FastMCP("mix_server")
```

### Schritt 2: Das CSV-Tool erstellen
Lass uns jetzt unser erstes Tool definieren: eines, das eine CSV-Datei zusammenfasst.

Erstelle eine neue Datei namens `csv_tools.py` im `tools/`-Ordner:

**tools/csv_tools.py**
```python
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
```

### Schritt 3: Das Parquet-Tool erstellen
Jetzt machen wir dasselbe für eine Parquet-Datei.

Erstelle eine Datei namens `parquet_tools.py` im `tools/`-Ordner:

**tools/parquet_tools.py**
```python
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
```

### Schritt 4: Den Server-Einstiegspunkt erstellen
Erstelle den Haupteinstiegspunkt für deinen MCP-Server:

**main.py**
```python
# main.py

from server import mcp

# Tools importieren, damit sie über Dekoratoren registriert werden
import tools.csv_tools
import tools.parquet_tools

# Einstiegspunkt zum Ausführen des Servers
if __name__ == "__main__":
    mcp.run()
```

Jetzt, wann immer der Server läuft, registriert er automatisch alle Tools über die `@mcp.tool()`-Dekoratoren.

Dein MCP-Server ist jetzt komplett! Im nächsten Abschnitt bauen wir einen lokalen Client mit LlamaIndex und Ollama, der sich mit deinem Server verbinden und diese Tools verwenden kann.

## Einen lokalen MCP-Client mit LlamaIndex und Ollama bauen

Jetzt kommt der aufregende Teil: einen lokalen Client bauen, der sich mit deinem MCP-Server verbinden und mit ihm über ein lokales LLM durch Ollama interagieren kann.

Dieser Client wird LlamaIndex verwenden, um die Interaktion zwischen dem lokalen LLM und deinen MCP-Tools zu orchestrieren.

### Schritt 1: Den lokalen Client erstellen
Erstelle eine neue Datei namens `client.py` in deinem Projektverzeichnis:

**client.py**
```python
# client.py

import asyncio
import nest_asyncio
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.workflow import Context
from llama_index.core.agent.workflow import ToolCall, ToolCallResult

# nest_asyncio anwenden, um async in Jupyter-ähnlichen Umgebungen zu ermöglichen
nest_asyncio.apply()

class LocalMCPClient:
    def __init__(self, model_name: str = "llama3.2", server_url: str = "http://127.0.0.1:8000/sse"):
        """
        Den lokalen MCP-Client initialisieren.
        
        Args:
            model_name: Name des zu verwendenden Ollama-Modells
            server_url: URL des MCP-Servers
        """
        self.model_name = model_name
        self.server_url = server_url
        self.llm = None
        self.agent = None
        self.agent_context = None
        self.mcp_client = None
        self.tools = None
        
    async def setup(self):
        """Das LLM, den MCP-Client und den Agent einrichten."""
        # Lokales LLM einrichten
        self.llm = Ollama(model=self.model_name, request_timeout=120.0)
        Settings.llm = self.llm
        
        # MCP-Client einrichten
        self.mcp_client = BasicMCPClient(self.server_url)
        mcp_tools = McpToolSpec(client=self.mcp_client)
        self.tools = await mcp_tools.to_tool_list_async()
        
        # Verfügbare Tools anzeigen
        print("Verfügbare MCP-Tools:")
        for tool in self.tools:
            print(f"- {tool.metadata.name}: {tool.metadata.description}")
        
        # Agent einrichten
        system_prompt = """
        Du bist ein KI-Assistent, der mit Datendateien durch spezialisierte Tools arbeiten kann.
        Du hast Zugang zu Tools, die CSV- und Parquet-Dateien lesen und zusammenfassen können.
        
        Wenn ein Benutzer nach Datendateien fragt, verwende die entsprechenden Tools, um die Informationen
        zu bekommen und eine hilfreiche Zusammenfassung dessen zu geben, was du findest.
        
        Sei immer klar darüber, welche Dateien du analysierst und was die Ergebnisse zeigen.
        """
        
        self.agent = FunctionAgent(
            name="DataAgent",
            description="Ein Agent, der mit Datendateien durch MCP-Tools arbeiten kann.",
            tools=self.tools,
            llm=self.llm,
            system_prompt=system_prompt,
        )
        
        # Agent-Kontext für die Aufrechterhaltung der Gesprächshistorie erstellen
        self.agent_context = Context(self.agent)
        
        print(f"✅ Lokaler MCP-Client bereit mit {self.model_name}")
        
    async def chat(self, message: str, verbose: bool = True) -> str:
        """
        Eine Nachricht an den Agent senden und eine Antwort erhalten.
        
        Args:
            message: Benutzernachricht
            verbose: Ob Tool-Aufrufe angezeigt werden sollen
            
        Returns:
            Agent-Antwort
        """
        if not self.agent:
            raise RuntimeError("Client nicht eingerichtet. Rufe zuerst setup() auf.")
            
        print(f"\n👤 Benutzer: {message}")
        
        handler = self.agent.run(message, ctx=self.agent_context)
        
        # Events streamen, um Tool-Aufrufe zu zeigen
        if verbose:
            async for event in handler.stream_events():
                if type(event) == ToolCall:
                    print(f"🔧 Tool {event.tool_name} aufrufen mit Argumenten: {event.tool_kwargs}")
                elif type(event) == ToolCallResult:
                    print(f"📋 Tool {event.tool_name} Ergebnis: {event.tool_output[:100]}...")
        
        response = await handler
        print(f"\n🤖 Agent: {response}")
        return str(response)
    
    async def interactive_chat(self):
        """Eine interaktive Chat-Sitzung starten."""
        print("\n🚀 Starte interaktive Chat-Sitzung...")
        print("Tippe 'exit' zum Beenden, 'help' für Beispiele")
        
        while True:
            try:
                user_input = input("\n💬 Gib deine Nachricht ein: ").strip()
                
                if user_input.lower() == 'exit':
                    print("👋 Auf Wiedersehen!")
                    break
                elif user_input.lower() == 'help':
                    print("\n📚 Beispielbefehle:")
                    print("- Fasse die CSV-Datei namens sample.csv zusammen")
                    print("- Was ist in der sample.parquet-Datei?")
                    print("- Wie viele Zeilen hat sample.csv?")
                    print("- Vergleiche sample.csv und sample.parquet")
                    continue
                elif not user_input:
                    continue
                    
                await self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                print(f"❌ Fehler: {e}")

async def main():
    """Hauptfunktion zum Ausführen des Clients."""
    client = LocalMCPClient()
    
    print("🔧 Richte lokalen MCP-Client ein...")
    await client.setup()
    
    # Interaktiven Chat starten
    await client.interactive_chat()

if __name__ == "__main__":
    asyncio.run(main())
```

### Schritt 2: Server für SSE-Transport aktualisieren
Wir müssen unseren Server aktualisieren, um Server-Sent Events (SSE) zu unterstützen, damit der Client sich mit ihm verbinden kann. Aktualisiere deine `main.py`:

**main.py**
```python
# main.py

from server import mcp

# Tools importieren, damit sie über Dekoratoren registriert werden
import tools.csv_tools
import tools.parquet_tools

# Einstiegspunkt zum Ausführen des Servers
if __name__ == "__main__":
    import asyncio
    
    # Server mit SSE-Transport ausführen
    asyncio.run(mcp.run(transport="sse"))
```

### Wie das funktioniert
1. **LocalMCPClient**: Eine Klasse, die die gesamte Client-Funktionalität kapselt
2. **LLM-Setup**: Verwendet Ollama, um ein lokales LLM auszuführen (standardmäßig Llama 3.2)
3. **MCP-Verbindung**: Verbindet sich über SSE mit deinem lokalen MCP-Server
4. **Tool-Integration**: Verwendet LlamaIndex's McpToolSpec, um MCP-Tools für den Agent zu verpacken
5. **Function Agent**: Erstellt einen Agent, der Tools basierend auf Benutzeranfragen aufrufen kann
6. **Interaktiver Chat**: Bietet eine einfache Kommandozeilen-Schnittstelle zum Chatten

Der Client zeigt Tool-Aufrufe in Echtzeit an, sodass du genau sehen kannst, was passiert, wenn die KI entscheidet, deine Tools zu verwenden.

## Dein komplettes lokales MCP-System ausführen und testen

Jetzt ist es Zeit, alles zusammenzuführen und dein komplettes lokales MCP-System zu testen!

### Schritt 1: Den MCP-Server starten
Lass uns zuerst deinen MCP-Server starten. Öffne ein Terminal in deinem Projektverzeichnis und führe aus:

```bash
uv run main.py
```

Du solltest eine Ausgabe sehen, die anzeigt, dass der Server gestartet wurde. Er wartet auf Verbindungen vom Client.

### Schritt 2: Ollama starten (falls nicht bereits laufend)
Stelle sicher, dass Ollama läuft und das Modell hat, das du verwenden möchtest:

```bash
ollama serve
```

In einem anderen Terminal prüfe, ob dein Modell verfügbar ist:

```bash
ollama list
```

Falls du `llama3.2` nicht siehst, lade es herunter:

```bash
ollama pull llama3.2
```

### Schritt 3: Den lokalen Client ausführen
Öffne ein neues Terminal (lass den Server laufen) und starte den Client:

```bash
uv run client.py
```

Du solltest sehen:
1. Der Client verbindet sich mit dem MCP-Server
2. Eine Liste der verfügbaren Tools
3. Die Nachricht über den Abschluss des Setups
4. Eine Eingabeaufforderung zum Chat-Start

### Schritt 4: Das System testen
Probiere diese Beispiel-Interaktionen:

**Beispiel 1: Grundlegende CSV-Zusammenfassung**
```
💬 Gib deine Nachricht ein: Fasse die CSV-Datei namens sample.csv zusammen
```

Du solltest sehen:
- Der Tool-Aufruf wird gemacht
- Das Tool gibt Daten über die CSV-Datei zurück
- Der Agent liefert eine natürlichsprachliche Zusammenfassung

**Beispiel 2: Dateien vergleichen**
```
💬 Gib deine Nachricht ein: Vergleiche die Daten in sample.csv und sample.parquet - sind sie gleich?
```

**Beispiel 3: Spezifische Fragen**
```
💬 Gib deine Nachricht ein: Wie viele Personen sind in der sample.csv-Datei und was sind ihre Berufe?
```

### Schritt 5: Die Ausgabe verstehen
Wenn du eine Frage stellst, siehst du:

1. **Tool-Aufruf**: `🔧 Tool summarize_csv_file aufrufen mit Argumenten: {'filename': 'sample.csv'}`
2. **Tool-Ergebnis**: `📋 Tool summarize_csv_file Ergebnis: CSV-Datei 'sample.csv' hat 5 Zeilen...`
3. **Agent-Antwort**: Die natürlichsprachliche Interpretation der Tool-Ergebnisse durch das LLM

### Häufige Probleme beheben

**Server-Verbindungsprobleme:**
- Stelle sicher, dass der Server auf dem erwarteten Port läuft
- Prüfe, dass keine Firewall die Verbindung blockiert
- Überprüfe, ob die Server-URL im Client mit der tatsächlichen Adresse des Servers übereinstimmt

**Ollama-Probleme:**
- Stelle sicher, dass Ollama läuft: `ollama serve`
- Prüfe, ob das Modell heruntergeladen ist: `ollama list`
- Probiere ein anderes Modell, falls llama3.2 nicht gut funktioniert

**Tool-nicht-gefunden-Fehler:**
- Überprüfe, ob deine Datendateien im `data/`-Verzeichnis existieren
- Prüfe Dateiberechtigungen
- Stelle sicher, dass die Dateinamen genau übereinstimmen (groß-/kleinschreibungsabhängig)

**Speicher- oder Leistungsprobleme:**
- Probiere ein kleineres Modell wie `llama3.2:1b`, falls dein System ressourcenbeschränkt ist
- Erhöhe das Request-Timeout im Client, falls Antworten langsam sind

### Was unter der Haube passiert
1. Dein lokales LLM erhält deine natürlichsprachliche Frage
2. Es entscheidet, welche MCP-Tools (falls vorhanden) es aufrufen muss
3. Der Client sendet Tool-Anfragen an deinen MCP-Server
4. Der Server führt die Python-Funktionen aus und gibt Ergebnisse zurück
5. Das LLM verarbeitet die Tool-Ergebnisse und generiert eine natürlichsprachliche Antwort
6. All dies passiert lokal auf deinem Rechner - keine Daten verlassen dein System!

Herzlichen Glückwunsch! Du hast jetzt ein komplettes lokales MCP-System laufen. Im letzten Abschnitt fassen wir zusammen, was du gebaut hast, und erkunden Möglichkeiten, es zu erweitern.

## Zusammenfassung und nächste Schritte

Herzlichen Glückwunsch — du hast gerade ein komplettes lokales MCP-System gebaut!

Lass uns einen Moment innehalten und überdenken, was du erreicht hast.

### Was du gebaut hast
Durch das Befolgen dieses Leitfadens hast du jetzt ein vollständig funktionierendes lokales MCP-System, das:

- **Nur lokale Komponenten verwendet**: Ollama für LLM, Python für MCP-Server, LlamaIndex für Orchestrierung
- **Deine Daten privat hält**: Keine Daten verlassen deinen Rechner
- **Echte Daten liest** aus CSV- und Parquet-Dateien
- **Benutzerdefinierte MCP-Tools bereitstellt**, die dein lokales LLM aufrufen kann:
  - `summarize_csv_file`
  - `summarize_parquet_file`
- **Einer sauberen, modularen Struktur folgt**, die einfach zu erweitern ist
- **Natürlichsprachliche Interaktion** mit deinen Daten durch einen intelligenten Agent bietet

### Du hast auch gelernt, wie man:
- Eine lokale LLM-Umgebung mit Ollama einrichtet
- MCP-Tools mit dem `@mcp.tool()`-Decorator erstellt und registriert
- Einen MCP-Client mit LlamaIndex baut, der sich mit deinem Server verbindet
- Eine komplette lokale KI-Toolchain zusammenfügt
- Async-Operationen und Echtzeit-Tool-Aufrufe handhabt

### Architektur-Übersicht
Dein System besteht aus:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Lokales LLM   │◄──►│   MCP-Client     │◄──►│   MCP-Server    │
│   (Ollama)      │    │  (LlamaIndex)    │    │   (FastMCP)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲                        │
                                │                        ▼
                         ┌─────────────────┐    ┌─────────────────┐
                         │   Benutzer-     │    │   Daten-Tools   │
                         │   Chat-Interface│    │  (CSV/Parquet)  │
                         └─────────────────┘    └─────────────────┘
```

### Wohin von hier aus
Dieses Projekt wurde entwickelt, um dir die Grundlagen beizubringen, aber es ist nur der Anfang. Hier sind Ideen zur Erweiterung deines lokalen MCP-Systems:

#### 1. Erweiterte Daten-Tools hinzufügen
Versuche Tools zu bauen, die:
- Daten basierend auf Bedingungen filtern
- Statistiken berechnen (Mittelwert, Median, Modus)
- Visualisierungen generieren (matplotlib/seaborn)
- Datentransformationen durchführen
- Datenbanken abfragen (SQLite, PostgreSQL)

#### 2. Dateiformat-Unterstützung erweitern
Füge Unterstützung hinzu für:
- JSON-Dateien
- Excel-Tabellenkalkulationen
- XML/HTML-Dateien
- Log-Dateien
- Benutzerdefinierte Datenformate

#### 3. Externe API-Tools hinzufügen
Erstelle Tools, die:
- Wetterdaten abrufen
- Das Web durchsuchen
- REST-APIs abfragen
- Aus Message-Queues lesen
- Systemressourcen überwachen

#### 4. Die Client-Erfahrung verbessern
Erweitere den Client mit:
- Web-Interface mit Streamlit oder FastAPI
- Spracheingabe/-ausgabe
- Persistente Gesprächshistorie
- Mehrstufige Planung und Ausführung
- Benutzerdefinierte Prompt-Templates

#### 5. Erweiterte MCP-Features
Erkunde andere MCP-Fähigkeiten:
- **Ressourcen**: Verwende `@mcp.resource()`, um dynamische Datenquellen bereitzustellen
- **Prompts**: Erstelle wiederverwendbare Interaktions-Templates mit `@mcp.prompt()`
- **Async-Tools**: Baue hochleistungsfähige Async-Tools für I/O-Operationen
- **Tool-Verkettung**: Erstelle Workflows, die mehrere Tools kombinieren

#### 6. Verschiedene LLM-Modelle
Experimentiere mit:
- Verschiedenen Ollama-Modellen (CodeLlama, Mistral, etc.)
- Quantisierten Modellen für bessere Leistung
- Feinabgestimmten Modellen für spezifische Domänen
- Mehreren Modellen für verschiedene Aufgaben

#### 7. Produktions-Überlegungen
Für den realen Einsatz:
- Angemessenes Logging und Monitoring hinzufügen
- Authentifizierung und Autorisierung implementieren
- Konfigurationsmanagement erstellen
- Umfassende Fehlerbehandlung hinzufügen
- Automatisierte Tests bauen
- Deployment-Skripte erstellen

### Beispiel-Erweiterung: Ein Datenbank-Tool hinzufügen
Hier ist ein schnelles Beispiel, wie du ein SQLite-Datenbank-Tool hinzufügen könntest:

**tools/database_tools.py**
```python
from server import mcp
import sqlite3
from pathlib import Path

@mcp.tool()
def query_database(query: str, db_name: str = "sample.db") -> str:
    """
    Eine SQL-Abfrage gegen eine SQLite-Datenbank ausführen.
    
    Args:
        query: Auszuführende SQL-Abfrage
        db_name: Name der SQLite-Datenbankdatei
        
    Returns:
        Abfrageergebnisse als formatierter String
    """
    db_path = Path("data") / db_name
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                return f"Abfrage gab {len(results)} Zeilen zurück:\n" + \
                       "\n".join([str(row) for row in results])
            else:
                return "Abfrage erfolgreich ausgeführt, keine Ergebnisse zurückgegeben."
    except Exception as e:
        return f"Datenbankfehler: {str(e)}"
```

### Teilen und Lernen
- **GitHub**: Teile deine Erweiterungen und lerne von anderen
- **Community**: Tritt MCP- und LlamaIndex-Communities bei
- **Dokumentation**: Trage zur Verbesserung der MCP-Dokumentation bei
- **Experimente**: Probiere neue Kombinationen von Tools und Modellen

### Das größere Bild
Du hast mehr als nur eine Demo gebaut — du hast eine Grundlage für lokale KI-Anwendungen geschaffen, die:
- Privatsphäre respektieren, indem sie Daten lokal halten
- Erweiterbar und modular sind
- Open-Source-Tools verwenden
- Für spezifische Domänen angepasst werden können
- Transparente Tool-Ausführung bieten

Das repräsentiert ein mächtiges Paradigma: KI, die **für dich** arbeitet, **zu deinen Bedingungen**, **mit deinen Daten**, **auf deinem Rechner**.

Die Zukunft der KI-Tools ist lokal, privat und unter deiner Kontrolle. Du hast jetzt die Fähigkeiten, Teil des Aufbaus dieser Zukunft zu sein!
