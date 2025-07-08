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
