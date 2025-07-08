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
