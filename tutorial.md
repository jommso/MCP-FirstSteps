# Building Your First Local MCP System: Server + Client mit Ollama
Here's what we'll build:

A small MCP server using Python and the MCP SDK with two useful tools that read data from:
A CSV file (great for spreadsheets and tabular data)
A Parquet file (a format often used in data engineering and analytics)
A local MCP client using LlamaIndex and Ollama that connects to your server
A completely local AI system that runs on your machine without sending data to external services
A clean folder structure that makes it easy to add new tools or features later

You'll be able to ask your local AI things like: 
> "Summarize the contents of my data file" 
> "How many rows and columns are in this CSV?"

Why Start Here?
This tutorial is perfect for you if:

You want to build AI tools that work completely offline and keep your data private
You're curious about MCP and want to see how it works in practice with local LLMs
You'd like a solid starting point for building more advanced tool servers and clients laterr First MCP Server: A Step-by-Step Guide
Here’s what we’ll build:

A small server using Python and the MCP SDK
Two useful tools that read data from:
A CSV file (great for spreadsheets and tabular data)
A Parquet file (a format often used in data engineering and analytics)
A clean folder structure that makes it easy to add new tools or features later
A working connection to Claude for Desktop, so you can ask things like: > “Summarize the contents of my data file” > “How many rows and columns are in this CSV?”
Why Start Here?
This blog is perfect for you if:

You’ve heard about Claude and want to connect it to your own tools or data
You’re curious about MCP and want to see how it works in practice
You’d like a solid starting point for building more advanced tool servers later
We’ll use plain Python and some common libraries like pandas, with no web frameworks or deployment complexity. Everything will run locally on your machine.

By the end, you’ll have a fully working local MCP server and a better understanding of how to make AI tools that go beyond text prediction — and actually do useful work.

Let’s get started!

What Is MCP (and Why Should You Care)?
Let’s break this down before we start writing code.

MCP stands for Model Context Protocol. It’s a way to let apps like Claude for Desktop securely interact with external data and custom tools that you define.

Think of it like building your own mini API — but instead of exposing it to the whole internet, you’re exposing it to an AI assistant on your machine.

With MCP, you can:

Let Claude read a file or query a database
Create tools that do useful things (like summarize a dataset or fetch an API)
Add reusable prompts to guide how Claude behaves in certain tasks
For this project, we’re focusing on tools — the part of MCP that lets you write small Python functions the AI can call.

What We’re Building
Here’s a quick preview of what you’ll end up with:

A local MCP server called mix_server
Two tools: one that reads a CSV file, and one that reads a Parquet file
A clean, modular folder layout so you can keep adding more tools later
A working connection to Claude for Desktop so you can talk to your tools through natural language
Let’s start by setting up your project.

Project Setup (Step-by-Step)
We’ll use uv — a fast, modern Python project manager — to create and manage our environment. It handles dependencies, virtual environments, and script execution, all in one place.

If you’ve used pip or virtualenv before, uv is like both of those combined—but much faster and more ergonomic.

Step 1: Install uv
To install uv, run this in your terminal:

curl -LsSf https://astral.sh/uv/install.sh | sh
Then restart your terminal so the uv command is available.

You can check that it’s working with:

uv --version
Step 2: Create the Project
Let’s make a new folder for our MCP server:

uv init mix_server
cd mix_server
This creates a basic Python project with a pyproject.toml file to manage dependencies.

Step 3: Set Up a Virtual Environment
We’ll now create a virtual environment for our project and activate it:

uv venv
source .venv/bin/activate
This keeps your dependencies isolated from the rest of your system.

Step 4: Add Required Dependencies
We’re going to install three key packages:

mcp[cli]: The official MCP SDK and command-line tools
pandas: For reading CSV and Parquet files
pyarrow: Adds support for reading Parquet files via Pandas
Install them using:

uv add "mcp[cli]" pandas pyarrow
This updates your pyproject.toml and installs the packages into your environment.

Step 5: Create a Clean Folder Structure
We’ll use the following layout to stay organized:

mix_server/
│
├── data/                 # Sample CSV and Parquet files
│
├── tools/                # MCP tool definitions
│
├── utils/                # Reusable file reading logic
│
├── server.py             # Creates the Server
├── main.py             # Entry point for the MCP server
└── README.md             # Optional documentation
Create the folders:

mkdir data tools utils
touch server.py
Your environment is now ready. In the next section, we’ll create a couple of small data files to work with — a CSV and a Parquet file — and use them to power our tools.

Creating Sample Data Files
To build our first tools, we need something for them to work with. In this section, we’ll create two simple files:

A CSV file (great for spreadsheets and tabular data)
A Parquet file (a more efficient format used in data engineering)
Both files will contain the same mock dataset — a short list of users. You’ll use these files later when building tools that summarize their contents.

Step 1: Create the data/ Folder
If you haven’t already created the folder for our data, do it now from your project root:

mkdir data
Step 2: Create a Sample CSV File
Now let’s add a sample CSV file with some fake user data.

Create a new file called sample.csv inside the data/ folder:

data/sample.csv
And paste the following into it:

id,name,email,signup_date
1,Alice Johnson,alice@example.com,2023-01-15
2,Bob Smith,bob@example.com,2023-02-22
3,Carol Lee,carol@example.com,2023-03-10
4,David Wu,david@example.com,2023-04-18
5,Eva Brown,eva@example.com,2023-05-30
This file gives us structured, readable data — perfect for a tool to analyze.

Step 3: Convert the CSV to Parquet
We’ll now create a Parquet version of the same data using Python. This shows how easily you can support both file types in your tools.

Create a short script in the root of your project called generate_parquet.py:

# generate_parquet.py

import pandas as pd
# Read the CSV
df = pd.read_csv("data/sample.csv")
# Save as Parquet
df.to_parquet("data/sample.parquet", index=False)
Run the script:

uv run generate_parquet.py
After this, your data/ folder should look like:

data/
├── sample.csv
└── sample.parquet
What’s the Difference Between CSV and Parquet?
CSV: Simple, human-readable text file. Great for small datasets and quick inspection.
Parquet: A binary, column-based format. Much faster for large datasets and common in analytics pipelines (e.g. with Apache Spark or Dremio).
Supporting both formats makes your tools more flexible, and this example shows how little extra effort it takes.

Next, we’ll write some reusable utility functions that can read these files and return a quick summary of their contents — ready to be wrapped as MCP tools.

Writing Utility Functions to Read CSV and Parquet Files
Now that we have some data to work with, let’s write the core logic to read those files and return a basic summary.

We’re going to put this logic in a separate Python file under a folder called utils/. This makes it easy to reuse across different tools without duplicating code.

Step 1: Create the Utility Module
If you haven’t already created the utils/ folder, do it now:

mkdir utils
Now create a new Python file inside it:

touch utils/file_reader.py
Step 2: Add File Reading Functions
Open utils/file_reader.py and paste in the following code:

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
    df = pd.read_csv(file_path)
    return f"CSV file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
def read_parquet_summary(filename: str) -> str:
    """
    Read a Parquet file and return a simple summary.
    Args:
        filename: Name of the Parquet file (e.g. 'sample.parquet')
    Returns:
        A string describing the file's contents.
    """
    file_path = DATA_DIR / filename
    df = pd.read_parquet(file_path)
    return f"Parquet file '{filename}' has {len(df)} rows and {len(df.columns)} columns."
How This Works
We’re using pandas to read both CSV and Parquet files. It’s a well-known data analysis library in Python.
pathlib.Path helps us safely construct file paths across operating systems.
Both functions return a simple string like:

CSV file 'sample.csv' has 5 rows and 4 columns.
This is all the logic our tools will need to start with. Later, if you want to add more advanced summaries — like listing column names or detecting null values — you can expand these functions.

With our utilities ready, we can now expose them as MCP tools — so Claude can actually use them!

Wrapping File Readers as MCP Tools
Now that we’ve written the logic to read and summarize our data files, it’s time to make those functions available to Claude through MCP tools.

What’s an MCP Tool?
An MCP tool is a Python function you register with your MCP server that the AI can call when it needs to take action — like reading a file, querying an API, or performing a calculation.

To register a tool, you decorate the function with @mcp.tool(). Behind the scenes, MCP generates a definition that the AI can see and interact with.

But before we do that, let’s follow a best practice: we’ll define our MCP server instance in one central place, then import it into each file that defines tools. This ensures everything stays clean and consistent.

Step 1: Define the MCP Server Instance
Open your server.py and main.pyfiles (or create it if you haven’t already), and add the following:

# server.py

from mcp.server.fastmcp import FastMCP
# This is the shared MCP server instance
mcp = FastMCP("mix_server")
# main.py
from server import mcp

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()
This creates a named server called “mix_server” and exposes a simple run command.

Step 2: Create the CSV Tool
Let’s now define our first tool: one that summarizes a CSV file.

Create a new file called csv_tools.py inside the tools/ folder:

touch tools/csv_tools.py
Then add the following:

# tools/csv_tools.py

from server import mcp
from utils.file_reader import read_csv_summary
@mcp.tool()
def summarize_csv_file(filename: str) -> str:
    """
    Summarize a CSV file by reporting its number of rows and columns.
    Args:
        filename: Name of the CSV file in the /data directory (e.g., 'sample.csv')
    Returns:
        A string describing the file's dimensions.
    """
    return read_csv_summary(filename)
Step 3: Create the Parquet Tool
Now let’s do the same for a Parquet file.

Create a file called parquet_tools.py inside the tools/ folder:

touch tools/parquet_tools.py
And add:

# tools/parquet_tools.py

from server import mcp
from utils.file_reader import read_parquet_summary
@mcp.tool()
def summarize_parquet_file(filename: str) -> str:
    """
    Summarize a Parquet file by reporting its number of rows and columns.
    Args:
        filename: Name of the Parquet file in the /data directory (e.g., 'sample.parquet')
    Returns:
        A string describing the file's dimensions.
    """
    return read_parquet_summary(filename)
Step 4: Register the Tools
Since the tools are registered via decorators at import time, we just need to make sure the main.py file imports the tool modules. Add these lines at the top of server.py:

from server import mcp

# Import tools so they get registered via decorators
import tools.csv_tools
import tools.parquet_tools

# Entry point to run the server
if __name__ == "__main__":
    mcp.run()
Now, whenever the server runs, it automatically registers all tools via the @mcp.tool() decorators.

Your tools are now live! In the next section, we’ll walk through how to run the server and connect it to Claude for Desktop so you can test them out in natural language.

Running and Testing Your MCP Server with Claude for Desktop
At this point, you’ve built a functional MCP server with two tools: one for reading CSV files and another for Parquet. Now it’s time to bring it to life and connect it to Claude for Desktop, so you can start running your tools using plain English.

Step 1: Run the Server
Let’s start your server locally.

In your project root (where main.py lives), run:

uv run main.py
This starts your MCP server using the tools you defined. You won’t see much output in the terminal just yet — that’s normal. Your server is now waiting for a connection from a client like Claude.

Step 2: Install Claude for Desktop (If You Haven’t Already)
You’ll need Claude for Desktop installed to connect to your server.

Download it here: https://www.anthropic.com/claude

Follow the installation instructions for your operating system

Note: As of now, Claude for Desktop is not available on Linux. If you’re on Linux, skip ahead to the section on building your own MCP client.

Step 3: Configure Claude to Use Your Server
Claude needs to know where to find your MCP server. You’ll do this by editing a small config file on your system.

MacOS / Linux:
Open this file in your code editor (create it if it doesn’t exist):

code ~/Library/Application\ Support/Claude/claude_desktop_config.json
Windows:
The config file is located here:

%APPDATA%\Claude\claude_desktop_config.json
Step 4: Add Your Server to the Config
Paste the following JSON into the file, replacing the “/ABSOLUTE/PATH/…” with the actual full path to your mix_server project folder:

{
  "mcpServers": {
    "mix_server": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/mix_server",
        "run",
        "main.py"
      ]
    }
  }
Tip: To find the absolute path:

On Mac/Linux: Run pwd in your terminal

On Windows: Use cd and copy the full path from File Explorer

Make sure uv is in your system PATH, or replace “command”: “uv” with the full path to the uv executable.

Step 5: Restart Claude for Desktop
Restart the app, and you should see a new tool icon (hammer) appear in the interface. Click it, and you’ll see your registered tools:

summarize_csv_file
summarize_parquet_file
These can now be called directly by the AI!

Step 6: Try It Out
Now try asking Claude something like:

“Summarize the CSV file named sample.csv.”
“How many rows are in sample.parquet?”
Claude will detect the appropriate tool, call your server, and respond with the results — powered by the very Python code you wrote.

Troubleshooting Tips
If things don’t work right away, here are a few things to check:

Make sure your uv run server.py process is running and hasn't crashed
Ensure the file paths in your config JSON are correct
Confirm that your data files (sample.csv, sample.parquet) exist in the /data directory
Check the Claude UI for error messages or tool-loading indicators
You now have a working local AI toolchain powered by MCP! In the final section, we’ll do a quick recap and show how you can build on this template for more powerful tools.

Recap and Next Steps
Congratulations — you just built your first MCP server!

Let’s take a moment to review what you’ve accomplished.

What You Built
By following this guide, you now have a fully working MCP server that:

Uses Python and the official mcp SDK
Reads real data from both CSV and Parquet files
Exposes two custom MCP tools that Claude for Desktop can call:
summarize_csv_file
summarize_parquet_file
Follows a clean, modular folder structure
Runs locally using uv and connects seamlessly to Claude for natural language interaction
You also learned how to:
Set up your Python project with uv
Manage dependencies cleanly
Register and expose tools using the @mcp.tool() decorator
Wire everything together with Claude through a simple config file
Where to Go From Here
This project was intentionally simple so you could focus on learning the structure and flow of an MCP server. But this is just the beginning.

Here are a few ideas for extending this template:

1. Add More Advanced Tools
Try building tools that:

Filter rows based on a column value
Return column names or data types
Calculate statistics (mean, median, etc.)
2. Use Resources
Use @mcp.resource() to expose static or dynamic data that Claude can pull into its context before making a decision.

3. Explore Prompts
Create reusable interaction templates with @mcp.prompt() to guide how Claude asks or responds.

4. Add Async Logic
If you’re pulling data from APIs or databases, consider making your tools async using async def—fully supported by FastMCP.

5. Build Your Own Client
Not using Claude? You can write your own MCP-compatible client using the SDK’s ClientSession interface.

Share and Reuse
You now have a template you can reuse for future projects. If you publish it on GitHub, others can fork it, extend it, and learn from it too.

This isn’t just a demo — it’s the foundation of a toolchain where you can define your own AI-powered workflows and expose them to LLMs in a controlled, modular way.
