# Building Your First Local MCP System: Server + Client mit Ollama

Here's what we'll build:

- A small MCP server using Python and the MCP SDK with two useful tools that read data from:
  - A CSV file (great for spreadsheets and tabular data)
  - A Parquet file (a format often used in data engineering and analytics)
- A local MCP client using LlamaIndex and Ollama that connects to your server
- A completely local AI system that runs on your machine without sending data to external services
- A clean folder structure that makes it easy to add new tools or features later

You'll be able to ask your local AI things like: 
> "Summarize the contents of my data file" 
> "How many rows and columns are in this CSV?"

## Why Start Here?
This tutorial is perfect for you if:

- You want to build AI tools that work completely offline and keep your data private
- You're curious about MCP and want to see how it works in practice with local LLMs
- You'd like a solid starting point for building more advanced tool servers and clients later

We'll use plain Python, pandas, and local LLM tools like Ollama and LlamaIndex, with no web frameworks or cloud services. Everything will run locally on your machine.

By the end, you'll have a fully working local MCP server and client, plus a better understanding of how to make AI tools that go beyond text prediction — and actually do useful work while keeping your data completely private.

Let's get started!

## What Is MCP (and Why Should You Care)?
Let's break this down before we start writing code.

MCP stands for Model Context Protocol. It's a way to let AI applications securely interact with external data and custom tools that you define.

Think of it like building your own mini API — but instead of exposing it to the whole internet, you're exposing it to a local AI assistant running on your machine.

With MCP, you can:

- Let your local LLM read a file or query a database
- Create tools that do useful things (like summarize a dataset or fetch an API)
- Add reusable prompts to guide how your AI behaves in certain tasks

For this project, we're focusing on tools — the part of MCP that lets you write small Python functions that a local LLM can call.

## What We're Building
Here's a quick preview of what you'll end up with:

- A local MCP server called `mix_server`
- Two tools: one that reads a CSV file, and one that reads a Parquet file
- A local MCP client using LlamaIndex that connects to your server
- Ollama running a local LLM (like Llama 3.2) to power the client
- A clean, modular folder layout so you can keep adding more tools later
- A completely local system where you can chat with your data using natural language

Let's start by setting up your project.

## Project Setup (Step-by-Step)
We'll use uv — a fast, modern Python project manager — to create and manage our environment. It handles dependencies, virtual environments, and script execution, all in one place.

If you've used pip or virtualenv before, uv is like both of those combined—but much faster and more ergonomic.

### Step 1: Install Ollama
First, we need to install Ollama to run local LLMs. Go to [ollama.ai](https://ollama.ai) and follow the installation instructions for your operating system.

After installation, pull a suitable model:

```bash
ollama pull llama3.2
```

This downloads the Llama 3.2 model which works well for tool calling tasks.

### Step 2: Install uv
To install uv, run this in your terminal:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For Windows (PowerShell):
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then restart your terminal so the uv command is available.

You can check that it's working with:

```bash
uv --version
```

### Step 3: Create the Project
Let's make a new folder for our MCP system:

```bash
uv init mix_server
cd mix_server
```

This creates a basic Python project with a pyproject.toml file to manage dependencies.

### Step 4: Set Up a Virtual Environment
We'll now create a virtual environment for our project:

```bash
uv venv
```

On Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

On Mac/Linux:
```bash
source .venv/bin/activate
```

This keeps your dependencies isolated from the rest of your system.

### Step 5: Add Required Dependencies
We're going to install the necessary packages:

- `mcp[cli]`: The official MCP SDK and command-line tools
- `pandas`: For reading CSV and Parquet files
- `pyarrow`: Adds support for reading Parquet files via Pandas
- `llama-index`: For building the MCP client
- `llama-index-llms-ollama`: Ollama integration for LlamaIndex
- `llama-index-tools-mcp`: MCP tools integration for LlamaIndex
- `nest-asyncio`: For running async code in Jupyter-like environments

Install them using:

```bash
uv add "mcp[cli]" pandas pyarrow llama-index llama-index-llms-ollama llama-index-tools-mcp nest-asyncio
```

This updates your pyproject.toml and installs the packages into your environment.

### Step 6: Create a Clean Folder Structure
We'll use the following layout to stay organized:

```
mix_server/
│
├── data/                 # Sample CSV and Parquet files
│
├── tools/                # MCP tool definitions
│
├── utils/                # Reusable file reading logic
│
├── server.py             # Creates the MCP Server
├── main.py               # Entry point for the MCP server
├── client.py             # Local MCP client with LlamaIndex
└── README.md             # Optional documentation
```

Create the folders:

```bash
mkdir data tools utils
```

Your environment is now ready. In the next section, we'll create a couple of small data files to work with — a CSV and a Parquet file — and use them to power our tools.

## Creating Sample Data Files
To build our first tools, we need something for them to work with. In this section, we'll create two simple files:

- A CSV file (great for spreadsheets and tabular data)
- A Parquet file (a more efficient format used in data engineering)

Both files will contain the same mock dataset — a short list of users. You'll use these files later when building tools that summarize their contents.

### Step 1: Create the data/ Folder
If you haven't already created the folder for our data, do it now from your project root:

```bash
mkdir data
```

### Step 2: Create a Sample CSV File
Now let's add a sample CSV file with some fake user data.

Create a new file called `sample.csv` inside the `data/` folder:

**data/sample.csv**
```csv
id,name,email,signup_date
1,Alice Johnson,alice@example.com,2023-01-15
2,Bob Smith,bob@example.com,2023-02-22
3,Carol Lee,carol@example.com,2023-03-10
4,David Wu,david@example.com,2023-04-18
5,Eva Brown,eva@example.com,2023-05-30
```

This file gives us structured, readable data — perfect for a tool to analyze.

### Step 3: Convert the CSV to Parquet
We'll now create a Parquet version of the same data using Python. This shows how easily you can support both file types in your tools.

Create a short script in the root of your project called `generate_parquet.py`:

```python
# generate_parquet.py

import pandas as pd

# Read the CSV
df = pd.read_csv("data/sample.csv")

# Save as Parquet
df.to_parquet("data/sample.parquet", index=False)

print("Parquet file created successfully!")
```

Run the script:

```bash
uv run generate_parquet.py
```

After this, your `data/` folder should look like:

```
data/
├── sample.csv
└── sample.parquet
```

### What's the Difference Between CSV and Parquet?
- **CSV**: Simple, human-readable text file. Great for small datasets and quick inspection.
- **Parquet**: A binary, column-based format. Much faster for large datasets and common in analytics pipelines (e.g. with Apache Spark or Dremio).

Supporting both formats makes your tools more flexible, and this example shows how little extra effort it takes.

Next, we'll write some reusable utility functions that can read these files and return a quick summary of their contents — ready to be wrapped as MCP tools.

## Writing Utility Functions to Read CSV and Parquet Files
Now that we have some data to work with, let's write the core logic to read those files and return a basic summary.

We're going to put this logic in a separate Python file under a folder called `utils/`. This makes it easy to reuse across different tools without duplicating code.

### Step 1: Create the Utility Module
If you haven't already created the `utils/` folder, do it now:

```bash
mkdir utils
```

Now create a new Python file inside it:

**utils/file_reader.py**

```python
# utils/file_reader.py

import pandas as pd
from pathlib import Path

# Base directory where our data lives
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

def read_csv_summary(filename: str) -> str:
    """
    Read a CSV file and return a simple summary.
    
    Args:
        filename: Name of the CSV file (e.g. 'sample.csv')
        
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"File '{filename}' not found in data directory."
    
    try:
        df = pd.read_csv(file_path)
        summary = f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns.\n"
        summary += f"Columns: {', '.join(df.columns.tolist())}\n"
        summary += f"First few rows:\n{df.head().to_string()}"
        return summary
    except Exception as e:
        return f"Error reading CSV file '{filename}': {str(e)}"

def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a simple summary.
    
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
        
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    if not file_path.exists():
        return f"File '{filename}' not found in data directory."
    
    try:
        df = pd.read_parquet(file_path)
        summary = f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns.\n"
        summary += f"Columns: {', '.join(df.columns.tolist())}\n"
        summary += f"First few rows:\n{df.head().to_string()}"
        return summary
    except Exception as e:
        return f"Error reading Parquet file '{filename}': {str(e)}"
```

### How This Works
- We're using pandas to read both CSV and Parquet files. It's a well-known data analysis library in Python.
- `pathlib.Path` helps us safely construct file paths across operating systems.
- Both functions return detailed summaries including column information and a preview of the data.
- We include error handling to provide useful feedback if files don't exist or can't be read.

This is all the logic our tools will need to start with. Later, if you want to add more advanced summaries — like detecting null values or calculating statistics — you can expand these functions.

With our utilities ready, we can now expose them as MCP tools — so our local LLM can actually use them!

## Wrapping File Readers as MCP Tools
Now that we've written the logic to read and summarize our data files, it's time to make those functions available to our local LLM through MCP tools.

### What's an MCP Tool?
An MCP tool is a Python function you register with your MCP server that the AI can call when it needs to take action — like reading a file, querying an API, or performing a calculation.

To register a tool, you decorate the function with `@mcp.tool()`. Behind the scenes, MCP generates a definition that the AI can see and interact with.

But before we do that, let's follow a best practice: we'll define our MCP server instance in one central place, then import it into each file that defines tools. This ensures everything stays clean and consistent.

### Step 1: Define the MCP Server Instance
Create your `server.py` file with the following content:

**server.py**
```python
# server.py

from mcp.server.fastmcp import FastMCP

# This is the shared MCP server instance
mcp = FastMCP("mix_server")
```

### Step 2: Create the CSV Tool
Let's now define our first tool: one that summarizes a CSV file.

Create a new file called `csv_tools.py` inside the `tools/` folder:

**tools/csv_tools.py**
```python
# tools/csv_tools.py

from server import mcp
from utils.file_reader import read_csv_summary

@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows, columns, and showing a preview.
    
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
        
    Returns:
        A string describing the file's contents and structure.
    """
    return read_csv_summary(filename)
```

### Step 3: Create the Parquet Tool
Now let's do the same for a Parquet file.

Create a file called `parquet_tools.py` inside the `tools/` folder:

**tools/parquet_tools.py**
```python
# tools/parquet_tools.py

from server import mcp
from utils.file_reader import read_parquet_summary

@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows, columns, and showing a preview.
    
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
        
    Returns:
        A string describing the file's contents and structure.
    """
    return read_parquet_summary(filename)
```

### Step 4: Create the Server Entry Point
Create the main entry point for your MCP server:

**main.py**
```python
# main.py

from server import mcp

# Import tools so they get registered via decorators
import tools.csv_tools
import tools.parquet_tools

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()
```

Now, whenever the server runs, it automatically registers all tools via the `@mcp.tool()` decorators.

Your MCP server is now complete! In the next section, we'll build a local client using LlamaIndex and Ollama that can connect to your server and use these tools.

## Building a Local MCP Client with LlamaIndex and Ollama

Now comes the exciting part: building a local client that can connect to your MCP server and interact with it using a local LLM through Ollama.

This client will use LlamaIndex to orchestrate the interaction between the local LLM and your MCP tools.

### Step 1: Create the Local Client
Create a new file called `client.py` in your project root:

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

# Apply nest_asyncio to allow async in Jupyter-like environments
nest_asyncio.apply()

class LocalMCPClient:
    def __init__(self, model_name: str = "llama3.2", server_url: str = "http://127.0.0.1:8000/sse"):
        """
        Initialize the local MCP client.
        
        Args:
            model_name: Name of the Ollama model to use
            server_url: URL of the MCP server
        """
        self.model_name = model_name
        self.server_url = server_url
        self.llm = None
        self.agent = None
        self.agent_context = None
        self.mcp_client = None
        self.tools = None
        
    async def setup(self):
        """Set up the LLM, MCP client, and agent."""
        # Setup local LLM
        self.llm = Ollama(model=self.model_name, request_timeout=120.0)
        Settings.llm = self.llm
        
        # Setup MCP client
        self.mcp_client = BasicMCPClient(self.server_url)
        mcp_tools = McpToolSpec(client=self.mcp_client)
        self.tools = await mcp_tools.to_tool_list_async()
        
        # Display available tools
        print("Available MCP tools:")
        for tool in self.tools:
            print(f"- {tool.metadata.name}: {tool.metadata.description}")
        
        # Setup agent
        system_prompt = """
        You are an AI assistant that can work with data files through specialized tools.
        You have access to tools that can read and summarize CSV and Parquet files.
        
        When a user asks about data files, use the appropriate tools to get the information
        and provide a helpful summary of what you find.
        
        Always be clear about what files you're analyzing and what the results show.
        """
        
        self.agent = FunctionAgent(
            name="DataAgent",
            description="An agent that can work with data files through MCP tools.",
            tools=self.tools,
            llm=self.llm,
            system_prompt=system_prompt,
        )
        
        # Create agent context for maintaining conversation history
        self.agent_context = Context(self.agent)
        
        print(f"✅ Local MCP client ready with {self.model_name}")
        
    async def chat(self, message: str, verbose: bool = True) -> str:
        """
        Send a message to the agent and get a response.
        
        Args:
            message: User message
            verbose: Whether to show tool calls
            
        Returns:
            Agent response
        """
        if not self.agent:
            raise RuntimeError("Client not set up. Call setup() first.")
            
        print(f"\n👤 User: {message}")
        
        handler = self.agent.run(message, ctx=self.agent_context)
        
        # Stream events to show tool calls
        if verbose:
            async for event in handler.stream_events():
                if type(event) == ToolCall:
                    print(f"🔧 Calling tool {event.tool_name} with args: {event.tool_kwargs}")
                elif type(event) == ToolCallResult:
                    print(f"📋 Tool {event.tool_name} result: {event.tool_output[:100]}...")
        
        response = await handler
        print(f"\n🤖 Agent: {response}")
        return str(response)
    
    async def interactive_chat(self):
        """Start an interactive chat session."""
        print("\n🚀 Starting interactive chat session...")
        print("Type 'exit' to quit, 'help' for examples")
        
        while True:
            try:
                user_input = input("\n💬 Enter your message: ").strip()
                
                if user_input.lower() == 'exit':
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    print("\n📚 Example commands:")
                    print("- Summarize the CSV file named sample.csv")
                    print("- What's in the sample.parquet file?")
                    print("- How many rows are in sample.csv?")
                    print("- Compare sample.csv and sample.parquet")
                    continue
                elif not user_input:
                    continue
                    
                await self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    """Main function to run the client."""
    client = LocalMCPClient()
    
    print("🔧 Setting up local MCP client...")
    await client.setup()
    
    # Start interactive chat
    await client.interactive_chat()

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Update Server to Use SSE Transport
We need to update our server to support Server-Sent Events (SSE) so the client can connect to it. Update your `main.py`:

**main.py**
```python
# main.py

from server import mcp

# Import tools so they get registered via decorators
import tools.csv_tools
import tools.parquet_tools

# Entry point to run the server
if __name__ == "__main__":
    import asyncio
    
    # Run server with SSE transport
    asyncio.run(mcp.run(transport="sse"))
```

### How This Works
1. **LocalMCPClient**: A class that encapsulates all the client functionality
2. **LLM Setup**: Uses Ollama to run a local LLM (Llama 3.2 by default)
3. **MCP Connection**: Connects to your local MCP server via SSE
4. **Tool Integration**: Uses LlamaIndex's McpToolSpec to wrap MCP tools for the agent
5. **Function Agent**: Creates an agent that can call tools based on user requests
6. **Interactive Chat**: Provides a simple command-line interface for chatting

The client shows tool calls in real-time so you can see exactly what's happening when the AI decides to use your tools.

## Running and Testing Your Complete Local MCP System

Now it's time to bring everything together and test your complete local MCP system!

### Step 1: Start the MCP Server
First, let's start your MCP server. Open a terminal in your project directory and run:

```bash
uv run main.py
```

You should see output indicating that the server has started. It will be waiting for connections from the client.

### Step 2: Start Ollama (if not already running)
Make sure Ollama is running and has the model you want to use:

```bash
ollama serve
```

In another terminal, check that your model is available:

```bash
ollama list
```

If you don't see `llama3.2`, pull it:

```bash
ollama pull llama3.2
```

### Step 3: Run the Local Client
Open a new terminal (keeping the server running) and start the client:

```bash
uv run client.py
```

You should see:
1. The client connecting to the MCP server
2. A list of available tools
3. The setup completion message
4. A prompt to start chatting

### Step 4: Test the System
Try these example interactions:

**Example 1: Basic CSV Summary**
```
💬 Enter your message: Summarize the CSV file named sample.csv
```

You should see:
- The tool call being made
- The tool returning data about the CSV file
- The agent providing a natural language summary

**Example 2: Compare Files**
```
💬 Enter your message: Compare the data in sample.csv and sample.parquet - are they the same?
```

**Example 3: Specific Questions**
```
💬 Enter your message: How many people are in the sample.csv file and what are their professions?
```

### Step 5: Understanding the Output
When you ask a question, you'll see:

1. **Tool Call**: `🔧 Calling tool summarize_csv_file with args: {'filename': 'sample.csv'}`
2. **Tool Result**: `📋 Tool summarize_csv_file result: CSV file 'sample.csv' has 5 rows...`
3. **Agent Response**: The LLM's natural language interpretation of the tool results

### Troubleshooting Common Issues

**Server Connection Issues:**
- Make sure the server is running on the expected port
- Check that no firewall is blocking the connection
- Verify the server URL in the client matches the server's actual address

**Ollama Issues:**
- Ensure Ollama is running: `ollama serve`
- Check the model is downloaded: `ollama list`
- Try a different model if llama3.2 isn't working well

**Tool Not Found Errors:**
- Verify your data files exist in the `data/` directory
- Check file permissions
- Make sure the file names match exactly (case-sensitive)

**Memory or Performance Issues:**
- Try a smaller model like `llama3.2:1b` if your system is resource-constrained
- Increase the request timeout in the client if responses are slow

### What's Happening Under the Hood
1. Your local LLM receives your natural language question
2. It decides which MCP tools (if any) it needs to call
3. The client sends tool requests to your MCP server
4. The server executes the Python functions and returns results
5. The LLM processes the tool results and generates a natural language response
6. All of this happens locally on your machine - no data leaves your system!

Congratulations! You now have a complete local MCP system running. In the final section, we'll recap what you've built and explore ways to extend it.

## Recap and Next Steps

Congratulations — you just built a complete local MCP system!

Let's take a moment to review what you've accomplished.

### What You Built
By following this guide, you now have a fully working local MCP system that:

- **Uses only local components**: Ollama for LLM, Python for MCP server, LlamaIndex for orchestration
- **Keeps your data private**: No data leaves your machine
- **Reads real data** from both CSV and Parquet files
- **Exposes custom MCP tools** that your local LLM can call:
  - `summarize_csv_file`
  - `summarize_parquet_file`
- **Follows a clean, modular structure** that's easy to extend
- **Provides natural language interaction** with your data through an intelligent agent

### You also learned how to:
- Set up a local LLM environment with Ollama
- Create and register MCP tools using the `@mcp.tool()` decorator
- Build an MCP client using LlamaIndex that connects to your server
- Wire together a complete local AI toolchain
- Handle async operations and real-time tool calling

### Architecture Overview
Your system consists of:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local LLM     │◄──►│   MCP Client     │◄──►│   MCP Server    │
│   (Ollama)      │    │  (LlamaIndex)    │    │   (FastMCP)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲                        │
                                │                        ▼
                         ┌─────────────────┐    ┌─────────────────┐
                         │   User Chat     │    │   Data Tools    │
                         │   Interface     │    │  (CSV/Parquet)  │
                         └─────────────────┘    └─────────────────┘
```

### Where to Go From Here
This project was designed to teach you the fundamentals, but it's just the beginning. Here are ideas for extending your local MCP system:

#### 1. Add More Advanced Data Tools
Try building tools that:
- Filter data based on conditions
- Calculate statistics (mean, median, mode)
- Generate visualizations (matplotlib/seaborn)
- Perform data transformations
- Query databases (SQLite, PostgreSQL)

#### 2. Expand File Format Support
Add support for:
- JSON files
- Excel spreadsheets
- XML/HTML files
- Log files
- Custom data formats

#### 3. Add External API Tools
Create tools that:
- Fetch weather data
- Search the web
- Query REST APIs
- Read from message queues
- Monitor system resources

#### 4. Improve the Client Experience
Enhance the client with:
- Web interface using Streamlit or FastAPI
- Voice input/output
- Persistent conversation history
- Multi-turn planning and execution
- Custom prompt templates

#### 5. Advanced MCP Features
Explore other MCP capabilities:
- **Resources**: Use `@mcp.resource()` to expose dynamic data sources
- **Prompts**: Create reusable interaction templates with `@mcp.prompt()`
- **Async Tools**: Build high-performance async tools for I/O operations
- **Tool Chaining**: Create workflows that combine multiple tools

#### 6. Different LLM Models
Experiment with:
- Different Ollama models (CodeLlama, Mistral, etc.)
- Quantized models for better performance
- Fine-tuned models for specific domains
- Multiple models for different tasks

#### 7. Production Considerations
For real-world use:
- Add proper logging and monitoring
- Implement authentication and authorization
- Create configuration management
- Add comprehensive error handling
- Build automated testing
- Create deployment scripts

### Sample Extension: Adding a Database Tool
Here's a quick example of how you could add a SQLite database tool:

**tools/database_tools.py**
```python
from server import mcp
import sqlite3
from pathlib import Path

@mcp.tool()
def query_database(query: str, db_name: str = "sample.db") -> str:
    """
    Execute a SQL query against a SQLite database.
    
    Args:
        query: SQL query to execute
        db_name: Name of the SQLite database file
        
    Returns:
        Query results as a formatted string
    """
    db_path = Path("data") / db_name
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                return f"Query returned {len(results)} rows:\n" + \
                       "\n".join([str(row) for row in results])
            else:
                return "Query executed successfully, no results returned."
    except Exception as e:
        return f"Database error: {str(e)}"
```

### Share and Learn
- **GitHub**: Share your extensions and learn from others
- **Community**: Join MCP and LlamaIndex communities
- **Documentation**: Contribute to improving MCP documentation
- **Experiments**: Try new combinations of tools and models

### The Bigger Picture
You've built more than just a demo — you've created a foundation for local AI applications that:
- Respect privacy by keeping data local
- Are extensible and modular
- Use open-source tools
- Can be customized for specific domains
- Provide transparent tool execution

This represents a powerful paradigm: AI that works **for you**, **on your terms**, **with your data**, **on your machine**.

The future of AI tooling is local, private, and in your control. You now have the skills to be part of building that future!
