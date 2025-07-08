# First Steps with MCP
Hier stehen meine Notizen

## Wichtige Links
https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed
https://github.com/patchy631/ai-engineering-hub/tree/main/llamaindex-mcp


pip install uv

uv init mix_server # installiere uv mix_server
cd mix_server

uv venv # installiere virtuelle Umgebung
.\.venv\Scripts\activate # aktiviere virtuelle Umgebung (Windows)

uv add "mcp[cli]" pandas pyarrow # Add Required Dependencies

