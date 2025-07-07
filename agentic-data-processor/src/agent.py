# src/agent.py

##############################
# # Example usage
# from src.agent import agent_executor, df
# from src.file_loader import load_file

# # Load data
# df = load_file("data/input/my_data.csv")

# # Run agent command
# agent_executor.run("Drop rows where status is null, convert signup_date to datetime, redact email")

# # Agent command with RAG injection
# # Run RAG first:
# from src.rag_loader import run_retrieval_qa

# rag_context = run_retrieval_qa(f"What are the cleaning rules for this table?")

# # Inject into user command prompt:
# augmented_command = f"""
# Use these rules when cleaning:

# {rag_context}

# User command: {user_command}
# """

# result = agent_executor.run(augmented_command)

# # View result
# print(df.head())
##############################

from src.config_loader import load_agent_config
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import pandas as pd
from src.transformations import drop_nulls, convert_to_datetime, filter_by_value, redact_column

# Global df (for simplicity - later wrap in state class)
df = pd.DataFrame()

# Tool wrappers
def drop_nulls_tool(column):
    global df
    df = drop_nulls(df, column)
    return f"Dropped nulls from {column}"

def convert_to_datetime_tool(column):
    global df
    df = convert_to_datetime(df, column)
    return f"Converted {column} to datetime"

def filter_by_value_tool(column, min_value=None, max_value=None):
    global df
    df = filter_by_value(df, column, min_value, max_value)
    return f"Filtered {column} by value"

def redact_column_tool(column):
    global df
    df = redact_column(df, column)
    return f"Redacted {column}"

# Define Tools
tools = [
    Tool.from_function(
        func=drop_nulls_tool,
        name="drop_nulls",
        description="Drop rows with null values in the given column"
    ),
    Tool.from_function(
        func=convert_to_datetime_tool,
        name="convert_to_datetime",
        description="Convert the given column to datetime format"
    ),
    Tool.from_function(
        func=filter_by_value_tool,
        name="filter_by_value",
        description="Filter column by min and/or max value"
    ),
    Tool.from_function(
        func=redact_column_tool,
        name="redact_column",
        description="Redact the given column (replace values with '[REDACTED]')"
    ),
]

# Load config
config = load_agent_config()

# Initialize Agent
# llm = ChatOpenAI(model='gpt-4o')
llm = ChatOpenAI(model=config['agent']['model'], temperature=config['agent']['temperature'])

# Memory
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory = ConversationBufferMemory(k=config['agent']['memory']['k'], return_messages=True)

# # TODO - Define tools dynamically (you can add a registry mapping tool name to function)
# tools = []
# for tool_def in config['tools']:
#     tool_func = ...  # map tool_def['name'] to function, e.g. via a dict
#     tools.append(Tool.from_function(func=tool_func, name=tool_def['name'], description=tool_def['description']))

agent_executor = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=config['agent']['verbose']
)
