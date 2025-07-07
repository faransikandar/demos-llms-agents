import yaml
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, Tool
from src.config_loader import load_agent_config
from src.tool_registry import TOOL_REGISTRY
from src.rag_loader import run_retrieval_qa
import logging

class AgentManager:
    def __init__(self, config_path='configs/agent_config.yaml'):
        self.config = load_agent_config(config_path)
        self.logger = self._setup_logger()
        self.llm = ChatOpenAI(model=self.config['agent']['model'], temperature=self.config['agent']['temperature'])
        self.memory = ConversationBufferMemory(k=self.config['agent']['memory']['k'], return_messages=True)
        self.tools = self._load_tools()
        self.agent_executor = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=self.config['agent']['verbose']
        )
        self.logger.info("AgentManager initialized.")

    def _load_tools(self):
        tools = []
        for tool_def in self.config['tools']:
            tool_func = TOOL_REGISTRY.get(tool_def['name'])
            if not tool_func:
                self.logger.warning(f"Tool '{tool_def['name']}' not found in TOOL_REGISTRY")
                continue
            tools.append(Tool.from_function(func=tool_func, name=tool_def['name'], description=tool_def['description']))
            self.logger.info(f"Tool loaded: {tool_def['name']}")
        return tools

    def _setup_logger(self):
        logger = logging.getLogger("AgentManager")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("agent.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger

    def run(self, user_command, rag_enabled=True):
        if rag_enabled:
            rag_context = run_retrieval_qa("What are the cleaning rules for this table?")
            augmented_command = f"""
            Use these rules when cleaning:
            
            {rag_context}
            
            User command: {user_command}
            """
            self.logger.info(f"Running agent with RAG context. User command: {user_command}")
            return self.agent_executor.run(augmented_command)
        else:
            self.logger.info(f"Running agent WITHOUT RAG. User command: {user_command}")
            return self.agent_executor.run(user_command)
