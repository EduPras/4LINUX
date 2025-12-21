from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable

from typing import Tuple, List
from pydantic import BaseModel, Field

from .base_agent import Agent, AgentContext, AgentResponse, Models

class QuestionResponse(AgentResponse):
    text: str
    option: List[str] = Field(..., min_length=2, max_length=5)
    correct_answer: int
    context: str
    main_concept_id: str
    specific_concept_id: str
    
class QuestionContext(AgentContext):
    topics: Tuple[str, str]

class QuestionAgent(Agent):
    prompt = SystemMessage("""
        You are a Question creator Agent for an Educational Knowledge Graph.
        
        Your Goal: You have a <GENERAL CONCEPT> and a <SPECIFIC CONCEPT> within the general concept.
        Create a question based on those and provide me options as result.
        """)
    
    def __init__(self, llm: str):
        super().__init__(llm)

        self.agent_name = f"QuestionAgent"
        print(self.agent_name)

        self.agent = create_agent(
            name=self.agent_name,
            model=self.llm,
            middleware=[],
            tools=[],
            system_prompt=QuestionAgent.prompt,
            response_format=QuestionResponse
        )
    
     
    @traceable(run_type="chain", name="QuestionAgent")
    def invoke(self, context: QuestionContext) -> QuestionResponse:
        try:
            general_concept = context.topics[0]
            specific_concept = context.topics[1]

            result: QuestionResponse = self.agent.invoke(input={
                "messages": [
                    HumanMessage(content=f"<GENERAL CONCEPT>:\n{general_concept}\n\n<SPECIFIC CONCEPT>:\n{specific_concept}")]
            })
            return result['structured_response']
        except Exception as e:
            print(f'Error: {e}')
            return None
        
        
# if __name__ == '__main__':
#     from rich import print
#     from dotenv import load_dotenv
    
#     load_dotenv('../../.env')
#     agent = QuestionAgent(Models.GPT5_1) 
#     ctx = QuestionContext(topics=('Linux', 'Linus Torvalds'))
#     print(agent.invoke(ctx))