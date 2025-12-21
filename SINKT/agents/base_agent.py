from abc import ABC, abstractmethod
from pydantic import BaseModel
from enum import Enum

from langchain.chat_models import BaseChatModel, init_chat_model

class Models(str, Enum):
    GPT4_o = "openai:gpt-4o"
    GPT5_1 = "openai:gpt-5.1"
    CLAUDE4_5 = "anthropic:claude-opus-4-5"

class AgentContext(BaseModel):
    pass

class AgentResponse(BaseModel):
    pass

class Agent(ABC):
    prompt: str = "Define the prompt"
    llm: BaseChatModel
    agent_name: str

    def __init__(self, llm: Models, agent_name: str):
        super().__init__()
        self.llm = init_chat_model(llm.value)
        self.agent_name = agent_name
        
    @abstractmethod
    def invoke(self, context: AgentContext):
        pass
    