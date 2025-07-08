
0:02
today we are going to build a 100% local
0:05
secure and private MCP client that you
0:07
can connect to any MCP server that is
0:09
out there so here's what we're going to
0:11
cover in this tutorial we'll start with
0:12
some background on MCP understand some
0:15
of the key components and how a client
0:17
server interacts with each other and
0:20
then I'll explain you uh the
0:22
architecture diagram of the app that we
0:24
are going to build today that includes
0:25
our local MCP client and an SQLite
0:28
database over which we are going to
0:30
build a server and connect it to our
0:31
client and finally I'll be giving you a
0:34
detailed walkthrough of the code on how
0:36
you can build this yourself step by step
0:39
so without any further ado let's get
What is MCP
0:41
started all right so let's set the
0:43
context for this video by understanding
0:45
what MCP is and why do we need to learn
0:48
how to build a local client so MCP as we
0:51
all know is a standardized way that you
0:54
can use to connect your LLMs or your AI
0:57
agents to external APIs data sources and
1:01
for that matter any tool that is out
1:03
there right you can think of it as a a
1:05
USBC port for your AI application right
1:08
wherein you have your AI app and then
1:10
you can easily plug and play database
1:13
maybe uh an MCP server that is built
1:15
over GitHub or Gmail or local file
1:18
system and for that matter any API that
1:21
is out there on the internet you can
1:22
easily connect them to your AI agents
1:25
using a standard interface so that's
1:26
about MCP right so there are two major
1:29
components in an MCP setup one is a MCP
1:32
server right so MCP server basically
1:35
wraps up let's say the external APIs
1:38
database or for that matter like any API
1:40
that is present on the internet it can
1:41
also be your local file system it wraps
1:44
them as MCP tools and make them
1:47
available to the client now an MCP
1:49
client is something that is used by our
1:51
AI application and for that matter like
1:53
the agents and LLMs that we're building
1:55
to communicate with the MCP server right
1:58
now we typically see that this MCP
2:00
client is either hosted by cloud desktop
2:02
or cursor ID so there's a bit of problem
2:04
with that the reason being these MCP
2:08
host use an external LLM basically they
2:10
would be calling an API and sending your
2:13
data somewhere else so let's say if
2:15
you're working with some sensitive data
2:17
that is very important to your
2:18
organization and privacy is paramount
2:20
right so in that case you cannot use
2:22
such a client wherein your data would be
2:25
sent to some external server so this is
2:27
the exact problem that we are going to
2:29
solve today we'll be building our own
2:31
local client that you can universally
2:34
connect to any MCP server that is out
2:36
there let's try to understand the
2:38
architecture of the system that we are
2:39
going to build today all right so before
2:42
we jump into the demo it's time to
2:44
understand the key components and the
2:46
architecture of how the system that we
2:49
are building today is working right so
2:51
we are building a local MCP host which
2:54
has uh a llama index agent which is
2:56
powered by locally running LLM using
2:58
Olama and this agent is working together
3:01
with the our custommade client right so
3:04
uh let's try to understand step by step
3:06
how you know the life cycle of uh a user
3:09
interacting with the system would work
3:11
right so user would come up with a query
3:14
right this query is uh going to be you
3:16
know received by our agent and uh then
3:19
the agent would use the client to you
3:22
know connect with the MCP server excuse
3:24
me for this typo so this should be uh
3:27
local MCP server here so uh what what
3:30
the client uh is going to do is it is
3:33
going to connect with this uh MCP server
3:35
get information about all the tools that
3:37
are available right so this is shown in
3:38
the third step and uh based on the user
3:41
query the agent would decide like what
3:43
is the right tool to call right so then
3:46
we'll have an actual tool calling or
3:48
function calling right uh the MCP server
3:51
that we have it has two tools uh so it's
3:53
a server that is built on top of an SQL
3:56
database but as far as you are concerned
3:58
I mean you can replace this with any
4:00
server so our client is uh generic
4:02
universal and it it will easily connect
4:04
to that without any sort of code change
4:06
on the client side right so to to keep
4:10
things simple and dactic we have uh two
4:12
tools uh in this server one is to add
4:14
data to the server and one is to read
4:16
data from the server and uh based on
4:19
whatever tool is being called uh it will
4:21
you know finally generate a context or
4:23
the response and this response is then
4:26
received back by agent and on the basis
4:28
of that it will be able to you know
4:30
provide a final answer to the user query
4:33
so this is how the system work and uh
4:35
the text tech if you look at it we'll be
4:37
using llama index uh to orchestrate all
4:40
these things and then we'll be using uh
4:42
you know to locally serve an LLM which
4:45
is powering our agent and uh the LLM
4:48
that we are going to use would be deep
4:50
carv1 so I hope you got an idea of like
4:53
how uh so I hope you get an idea of like
4:56
how this system is going to work it's
4:58
time to you know build this and uh I'll
5:00
give you a step-by-step guide on how you
5:02
can do it
5:05
yourself so I hope now you understand
5:07
like how this system is going to work
5:08
and it's time to you know jump into the
5:10
code and build it step by
5:14
step all right so now I'm in my cursor
Code
5:16
ID and it's time to understand all the
5:18
code for building this system right so
5:21
uh I'll quickly start by explaining you
5:23
the server that we are going to use for
5:25
this demo uh which is uh a simple SQLite
5:30
server that I built right so it has two
5:32
tools which is uh an add data tool so
5:35
each of these tools are going to expect
5:37
uh you know an SQL query in form of a
5:39
string right uh and I have also provided
5:43
like all the description of like how the
5:44
query should look like what should be
5:46
the schema of it and also gave a few
5:48
examples so that it becomes for our
5:50
agents or the LLM to make the tool call
5:53
since we are using local LLMs right so
5:55
here's the actual uh functionality or
5:58
the code to you know add new data to our
6:01
SQLite server similarly the second tool
6:04
is a read data tool again takes a SQL
6:07
query in form of a string we have tried
6:09
to be as descriptive as possible
6:11
regarding what this tool does and
6:13
examples and uh the argument that is it
6:16
is going to take right again
6:18
uh the functionality is actually
6:20
implemented here so uh the tools are
6:23
fairly simple and as far as you are
6:25
concerned you can replace it with any
6:26
server that is out there that you want
6:28
to connect uh with our client and you do
6:30
not have to you know uh make any sort of
6:33
code changes uh on the client side so
6:34
the client is universal it would
6:36
generically connect to any MCP server
6:38
that is out there right finally uh we
6:41
have some uh code to you know uh how you
6:44
can run this server so I mean you just
6:46
need to run this command ue run server
6:48
py and then specify like the uh
6:51
transport mechanism so we are using uh
6:53
typically like MCP provide two transport
6:56
mechanism like how uh server can send
6:58
data to the client so if you're you know
7:00
doing something exper some sort of
7:02
experimentation and doing things locally
7:04
in that case you can use sddio so
7:06
basically uh everything that your server
7:09
is going to print to your terminal or
7:10
the stdio is going to be used by client
7:12
and uh it will be used as a context by
7:15
the agent that is working with the
7:17
client another thing that we are going
7:19
to use today is SSE which is like more
7:21
sophisticated way so let's say if you
7:23
you are connecting to a remote server
7:24
then the communication would happen or
7:26
you know server send event or just like
7:28
HTTP so do not get confused with the ter
7:31
terminologies like these are just two
7:33
ways on how your server can send data to
7:36
your client so uh that's about the
7:39
server and uh so what we can do is we
7:43
can already get our server
7:48
started right as you can see our server
Client
7:50
is start has started the next step is to
7:53
you know build an MCP client and
7:55
establish a connection with our server
7:57
right so as you can see llama index
7:59
provide these two modules one is uh the
8:01
basic MCP client and MCP tools spec so
8:04
basic MCP client is uh will be used to
8:07
you know uh we'll instantiate or create
8:09
our own client and we'll provide like uh
8:12
where the server is running so our
8:14
server is running at uh locally at 8,000
8:17
and you then also specify the transport
8:20
mechanism or like how the server is
8:22
going to send data to to this client so
8:24
as you know uh since we used SSC when we
8:26
started the server so we are going to
8:28
specify SSC here so this would be
8:31
connecting via server sent
8:32
events so now that our client is ready
8:35
what we're going to do is we'll be using
8:37
the second thing which is uh you know uh
8:40
MCP tool spec so if you look at the
8:43
definition of this class it is built on
8:45
top of the basic tool spec class so I'll
8:48
give shed more light on it or I'll give
8:50
more details about it very soon when we
8:52
are going to build the agent so if you
8:54
read this uh definition MCP toolspec
8:56
will get the tools from MCP client right
9:00
and convert them to llama index function
9:02
tools right so if you see here we have
9:05
already created uh the MCP client and
9:07
using MCP tools spec what we do is we'll
9:10
get all the tools uh that are available
9:13
to this client which is already
9:15
connected to our server right and then
9:17
it will wrap up them in a form so that
9:20
these tools can be used by the agent or
9:23
the function calling agent that we have
9:25
in llama index which we are soon going
9:27
to build right so these two lines are
9:29
doing all the heavy lifting in terms of
9:31
you know creating a client connecting it
9:33
to the server and then wrapping up those
9:35
tools in a way so that it can be as
9:37
easily used by our llama index agent
9:39
that we are going to build right so we
9:43
have it here and uh as you can see we'll
9:45
try to also print like uh what are all
9:47
the tools that are available in our
9:49
server since we already created the
9:50
client and uh it will print all the
9:52
metadata so as you can see uh so it is
9:56
providing uh the tool name so this is
9:58
the tool name right and uh it is also
10:00
giving the metadata description of like
10:03
what exactly is present in this tool
10:04
right so this is the description that we
10:07
provided
10:09
for the two tools that we created right
10:12
so this is fairly simple uh nothing
10:15
confusing about it right so now uh we
10:19
have access to the two tools that are
10:21
present in that MCP server we know like
10:23
the description and what exactly they do
10:25
and this is something that is going to
10:26
be used by the LLM that is powering the
10:29
agent that we are going to build so
10:31
without any further ado it's time to
Agent
10:34
build the agent right so before that
10:36
we'll also define a system prompt so
10:38
this system prompt would you know steer
10:40
the LLM in a way so that it knows that
10:43
what exactly this LLM is supposed to do
10:45
so in this case you know it's an AI
10:48
assistant that is used for tool calling
10:50
so we specify all that information here
10:52
uh but uh on need basis let's say if you
10:55
have a specific application you can use
10:56
this system prompt and uh uh modify it
10:59
according to your needs right so uh this
11:03
step is also done we have defined the
11:05
system
11:06
prompt now comes the important part
11:09
wherein we define our function calling
11:11
agent right and how we provide uh this
11:15
agent access to all the tools that are
11:17
present in the MCP server right so only
11:20
these lines are important right so the
11:23
function calling agent is nothing but a
11:25
simple you know llama index function
11:27
calling agent that has ability to call
11:30
any tools that are provided to it right
11:32
so if we look at the arguments uh it
11:34
takes uh the name of the agent right the
11:36
description like what exactly this agent
11:38
is supposed to do then it takes a list
11:41
of tools right the llm that is powering
11:43
it and the system that system prom that
11:45
we defined now you should carefully look
11:47
at you know uh this a agent does not
11:51
care whether the tools are coming from
11:53
you know a simple python function that
11:55
you have defined and you wrapped it up
11:57
uh using uh the base tool spec of llama
11:59
index right or whether it is coming from
12:01
MCP but here we have make made sure you
12:04
know these tools are the MCP tools uh
12:06
that we have got access to using our
12:08
client right so uh it's fairly simple so
12:11
it's just a typical function calling
12:13
agent but we are using making use of the
12:16
MCP tool spec so that we are able to you
12:18
know wrap up the tools that are present
12:20
in the server that we're connected with
12:22
right and they are wrapped up in a way
12:24
so that the agent can easily use them so
12:27
that simple next uh is uh you know we
12:31
also need to define like how we handle
12:33
the user messages right since uh we are
12:36
going to have uh you know an interactive
12:38
chat session so we need to make sure
12:39
like uh what all messages are there uh
12:42
what agent uh we are using you know for
12:44
all this interaction
12:46
And then we also need to provide context
12:48
so that let's say if I had a
12:51
conversation with the agent so it should
12:53
also store all these messages in the
12:55
context so that I can also ask a
12:57
question which is a followup of my
12:59
previous question right so basically
13:01
maintaining the chat context right so
13:02
all of that this would be done here so
13:05
we have this uh function that would take
13:07
care of you know handling the user
13:08
messages fairly simple you can read
13:11
about it like it takes the me message
13:13
context which is the string the user
13:14
message the agent that uh which is our
13:16
function calling agent we'll also define
13:18
the context very soon so that this
13:20
context would manage or you know take
13:21
care of you know storing all the chat
13:23
history and everything that is happening
13:24
like what tools have been called like
13:26
what what are the description or what
13:28
are the metadata that is involved in the
13:29
tool and uh the responses that we got
13:32
out of our queries right so everything
13:34
would be stored in this context so it's
13:36
just a helper function that we have
13:37
defined here and uh so let's run this as
13:40
So I mean we already initialized the
13:42
client so but let's uh again do that so
13:45
if you see uh these four or five lines
13:48
would completely explain like what
13:50
exactly is going on right so first we
13:52
create an MCP client right using the
13:55
basic MC MCP client functionality that
13:57
is provided by llama index we provide
13:59
the URL to our server uh we also specify
14:03
the transport mechanism right then we
14:05
use MCP tool spec to you know wrap up
14:08
the uh MCP tool in a way so that it can
14:10
be easily used by the agents uh the
14:13
llama index agent that we are going to
14:15
create right so then we call uh get
14:17
agent right so get agent would take uh
14:19
all these tools and it would be using it
14:22
here right
14:24
so that's fairly simple and finally we
14:27
are going to create the agent context
14:28
right so this agent context would make
14:30
sure agent keeps the context of the
14:34
entire chat history or the entire chat
14:35
session so that we can also ask
14:37
follow-up question based on our previous
14:39
conversation tool information what are
14:41
the output the row output that was given
14:44
by the tool and what is the final
14:45
response that is being sent to the LLM
14:47
so this simple line would take care of
14:49
all those things right all right so now
14:51
it's time to interact with this agent uh
14:53
which is running completely locally and
14:55
as we have like set up everything it has
14:57
access to all the tools that are
14:58
available in our MCP server right so as
15:00
you remember the two tools are simple
15:02
one is to you know add data to uh
15:04
database and another one is to you know
15:06
fetch data from it so let's get started
15:09
and uh first we are going to add some
15:11
data to
15:16
it so I'm providing a simple natural
15:19
language query i'm saying Rafael Nadal
15:21
whose age is 39 and is a tennis player
15:24
so as you can see uh this is uh the user
15:28
query and uh we were able to you know
15:30
successfully call the add data tools uh
15:33
with these keyword arguments so
15:34
basically it converts it uh into an SQL
15:36
query and uh the then the agent says
15:39
that the data has been successfully
15:41
added so let's try to fetch this data
15:43
now right we'll
15:49
call okay so now you can see like uh it
15:52
uh is calling the right tool again since
15:54
uh now we are trying to fetch the data
15:56
that we already added and it shows that
15:58
okay against ID1 we have Rafael Nadal
16:00
age 39 profession is tennis player so it
16:03
nicely structures uh and store it in
16:05
form of a table right so let's try to
16:08
add some new data
16:19
So again we are able to you know add new
16:21
data so you can
16:23
do fetch data again just for the sake of
16:26
this demo uh right so now uh it is able
16:29
to you know fetch all the new records as
16:31
well so yeah uh this is a fairly simple
16:34
demo uh and the reason being I just
16:35
wanted to focus on building an uh a
16:38
local MCP client but this client can be
16:41
universally connected to any MCP server
16:43
that is out there so you barely have to
16:45
like make any changes on the client side
16:47
and uh since MP MCP is so powerful like
16:50
it has standardized all this interaction
16:52
so it's a powerful setup so yeah
16:54
definitely try to try it out like let me
16:57
know if you have any feedback what you
16:58
liked about it and uh I think that is
17:01
all for this video and uh if you're
17:02
watching this on Twitter I have also
17:04
given a detailed uh description and a
17:06
step-by-step guide in the thread that
17:08
follows and if you're watching this uh
17:10
on YouTube make sure that uh you know
17:12
you like this video you subscribe to my
17:15
channel so that it gives me a signal
17:17
that I should be creating more content
17:18
like this all right thank you so much uh
17:21
for watching this and thank you so much
17:22
for your time i'll see you in another
17:24
video bye-bye





Building a Local MCP Client with LlamaIndex
This Jupyter notebook walks you through creating a local MCP (Model Context Protocol) client that can chat with a database through tools exposed by an MCP server—completely on your machine. Follow the cells in order for a smooth, self‑contained tutorial.

import nest_asyncio
nest_asyncio.apply()
2  Setup a local LLM
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings

llm = Ollama(model="llama3.2", request_timeout=120.0)
Settings.llm = llm
3  Initialize the MCP client and build the agent
Point the client at your local MCP server’s SSE endpoint (default shown below), and list the available tools.

from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tools = McpToolSpec(client=mcp_client) # you can also pass list of allowed tools
tools = await mcp_tools.to_tool_list_async()
for tool in tools:
    print(tool.metadata.name, tool.metadata.description)
add_data Add new data to the people table using a SQL INSERT query.

    Args:
        query (str): SQL INSERT query following this format:
            INSERT INTO people (name, age, profession)
            VALUES ('John Doe', 30, 'Engineer')
        
    Schema:
        - name: Text field (required)
        - age: Integer field (required)
        - profession: Text field (required)
        Note: 'id' field is auto-generated
    
    Returns:
        bool: True if data was added successfully, False otherwise
    
    Example:
        >>> query = '''
        ... INSERT INTO people (name, age, profession)
        ... VALUES ('Alice Smith', 25, 'Developer')
        ... '''
        >>> add_data(query)
        True
    
read_data Read data from the people table using a SQL SELECT query.

    Args:
        query (str, optional): SQL SELECT query. Defaults to "SELECT * FROM people".
            Examples:
            - "SELECT * FROM people"
            - "SELECT name, age FROM people WHERE age > 25"
            - "SELECT * FROM people ORDER BY age DESC"
    
    Returns:
        list: List of tuples containing the query results.
              For default query, tuple format is (id, name, age, profession)
    
    Example:
        >>> # Read all records
        >>> read_data()
        [(1, 'John Doe', 30, 'Engineer'), (2, 'Alice Smith', 25, 'Developer')]
        
        >>> # Read with custom query
        >>> read_data("SELECT name, profession FROM people WHERE age < 30")
        [('Alice Smith', 'Developer')]
    
3  Define the system prompt
This prompt steers the LLM when it needs to decide how and when to call tools.

SYSTEM_PROMPT = """\
You are an AI assistant for Tool Calling.

Before you help a user, you need to work with tools to interact with Our Database
"""
4  Helper function: get_agent()
Creates a FunctionAgent wired up with the MCP tool list and your chosen LLM.

from llama_index.tools.mcp import McpToolSpec
from llama_index.core.agent.workflow import FunctionAgent

async def get_agent(tools: McpToolSpec):
    tools = await tools.to_tool_list_async()
    agent = FunctionAgent(
        name="Agent",
        description="An agent that can work with Our Database software.",
        tools=tools,
        llm=OpenAI(model="gpt-4"),
        system_prompt=SYSTEM_PROMPT,
    )
    return agent
5  Helper function: handle_user_message()
Streams intermediate tool calls (for transparency) and returns the final response.

from llama_index.core.agent.workflow import (
    FunctionAgent, 
    ToolCallResult, 
    ToolCall)

from llama_index.core.workflow import Context

async def handle_user_message(
    message_content: str,
    agent: FunctionAgent,
    agent_context: Context,
    verbose: bool = False,
):
    handler = agent.run(message_content, ctx=agent_context)
    async for event in handler.stream_events():
        if verbose and type(event) == ToolCall:
            print(f"Calling tool {event.tool_name} with kwargs {event.tool_kwargs}")
        elif verbose and type(event) == ToolCallResult:
            print(f"Tool {event.tool_name} returned {event.tool_output}")

    response = await handler
    return str(response)
6  Initialize the MCP client and build the agent
Point the client at your local MCP server’s SSE endpoint (default shown below), build the agent, and setup agent context.

from llama_index.tools.mcp import BasicMCPClient, McpToolSpec


mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")
mcp_tool = McpToolSpec(client=mcp_client)

# get the agent
agent = await get_agent(mcp_tool)

# create the agent context
agent_context = Context(agent)
# Run the agent!
while True:
    user_input = input("Enter your message: ")
    if user_input == "exit":
        break
    print("User: ", user_input)
    response = await handle_user_message(user_input, agent, agent_context, verbose=True)
    print("Agent: ", response)
User:  Add to the db: Rafael Nadal whose age is 39 and is a tennis player
Calling tool add_data with kwargs {'query': "INSERT INTO people (name, age, profession) VALUES ('Rafael Nadal', 39, 'Tennis Player')"}
Tool add_data returned meta=None content=[TextContent(type='text', text='true', annotations=None)] isError=False
Agent:  The data has been added successfully.
User:  fetch data
Calling tool read_data with kwargs {'query': 'SELECT * FROM people'}
Tool read_data returned meta=None content=[TextContent(type='text', text='1', annotations=None), TextContent(type='text', text='Rafael Nadal', annotations=None), TextContent(type='text', text='39', annotations=None), TextContent(type='text', text='Tennis Player', annotations=None)] isError=False
Agent:  Here is the data from the database:

1. ID: 1
   Name: Rafael Nadal
   Age: 39
   Profession: Tennis Player
User:  add to the db: Roger federer whose age is 42 and is a tennis player
Calling tool add_data with kwargs {'query': "INSERT INTO people (name, age, profession) VALUES ('Roger Federer', 42, 'Tennis Player')"}
Tool add_data returned meta=None content=[TextContent(type='text', text='true', annotations=None)] isError=False
Agent:  The data has been added successfully.
User:  fetch data
Calling tool read_data with kwargs {'query': 'SELECT * FROM people'}
Tool read_data returned meta=None content=[TextContent(type='text', text='1', annotations=None), TextContent(type='text', text='Rafael Nadal', annotations=None), TextContent(type='text', text='39', annotations=None), TextContent(type='text', text='Tennis Player', annotations=None), TextContent(type='text', text='2', annotations=None), TextContent(type='text', text='Roger Federer', annotations=None), TextContent(type='text', text='42', annotations=None), TextContent(type='text', text='Tennis Player', annotations=None)] isError=False
Agent:  Here is the data from the database:

1. ID: 1
   Name: Rafael Nadal
   Age: 39
   Profession: Tennis Player

2. ID: 2
   Name: Roger Federer
   Age: 42
   Profession: Tennis Player