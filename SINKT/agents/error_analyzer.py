from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langsmith import traceable

from typing import Tuple, List, Literal
import random

from .base_agent import Agent, AgentContext, AgentResponse, Models
from .question import QuestionResponse
from ..models import StudentProfile

class ErrorAnalyzerResponse(AgentResponse):
    error_type: Literal['lack_of_concept_knowledge', 'slip', 'misinterpretation', 'lack_of_attention']
    text: str
    
class ErrorAnalyzerContext(AgentContext):
    std_chars: StudentProfile
    mastery: Tuple[float, float]
    question: QuestionResponse

class ErrorAnalyzerAgent(Agent):
    prompt = SystemMessage("""
        You are an Error Explainer Agent, you are analyzing an error a student's mistake on a question of given concepts.
        
        Your Goal: Based on the student <CHARACTERISTICS>, <CONCEPTS AND MASTERY>, <ANSWER_ID>
        and the question's <QUESTION TEXT>, <OPTIONS> and <CORRECT_ANSWER ID>,
        classify the error type in one of these: 
            - **slip**
            - **misinterpretation**
            - **lack_of_concept_knowledge**
            - **lack_of_attention**
    """)
    def __init__(self, llm: str):
        super().__init__(llm, f"ErrorAnalyzerAgent")

        print(self.agent_name, f"ErrorAnalyzerAgent")

        self.agent = create_agent(
            name=self.agent_name,
            model=self.llm,
            middleware=[],
            tools=[],
            system_prompt=ErrorAnalyzerAgent.prompt,
            response_format=ErrorAnalyzerResponse
        )
    
    @traceable(run_type="chain", name="ErrorAnalyzerAgent")
    def invoke(self, context: ErrorAnalyzerContext) -> ErrorAnalyzerResponse:
        try:
            options = context.question.option
            error_options = [opt for idx, opt in enumerate(options) if idx != int(context.question.correct_answer)]
            error_selected = random.choice(error_options)
            
            prompt =f"""
            <CHARACTERISTICS>
            
            {context.std_chars.to_plain_string()}

            <CONCEPTS AND MASTERY>
            - {context.question.main_concept_id} (Field area): {context.mastery[0]}
            - {context.question.specific_concept_id} (Specific): {context.mastery[1]}
            
            <QUESTION TEXT>
            {context.question.text}
            
            <OPTIONS>
            {options}
            
            <ANSWER ID>: {error_selected}
            <CORRECT ANSWER ID>: {context.question.correct_answer}
            """
            

            result: ErrorAnalyzerResponse = self.agent.invoke(input={"messages": [HumanMessage(content=prompt)]})

            return result['structured_response']
        except Exception as e:
            print(f'Error: {e}')
            return None
        
        
# if __name__ == '__main__':
#     from rich import print
#     from dotenv import load_dotenv
    
#     load_dotenv('../.env')
#     agent = ErrorAnalyzerAgent(Models.GPT5_1) 
#     question = QuestionResponse(
#         context="Linus is the man who created the linux kernel",
#         main_concept_id="Linux",
#         specific_concept_id="Kernel linux",
#         option=["Didi", "Zezé de Camargo & Luciano", "Linus Torvalds", "Sandy"],
#         correct_answer=2,
#         text="Who created the linux kernel?"
#     )
    
#     mastery = [random.random(), random.random()]
    
#     profile = StudentProfile(
#         id="Student test",
#         archetype="Mad",
#         initial_proficiency=random.random(),
#         slip_rate=random.random(),
#         guess_rate=random.random(),
#         learning_speed=random.random(),
#         logical_ability=random.random(),
#         text_interpretation=random.random(),
#         technological_familiarity=random.random()
#     )
#     ctx = ErrorAnalyzerContext(mastery=mastery, question=question, std_chars=profile)
#     print(agent.invoke(ctx))
