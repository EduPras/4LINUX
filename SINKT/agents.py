import os
import random

from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import BaseChatModel
from langsmith import traceable

from .models import QuestionSchema, ErrorAnalyzerSchema, StudentProfile
from typing import Tuple, List
from dotenv import load_dotenv

load_dotenv('../.')

class QuestionAgent():
    prompt = SystemMessage("""
        You are a Question creator Agent for an Educational Knowledge Graph.
        
        Your Goal: You have a <GENERAL CONCEPT> and a <SPECIFIC CONCEPT> within the general concept.
        Create a question based on those and provide me options as result.
        """)
    
    def __init__(self, llm: BaseChatModel):

        self.agent_name = f"QuestionAgent"

        self.agent = create_agent(
            name=self.agent_name,
            model=llm,
            middleware=[],
            tools=[],
            system_prompt=QuestionAgent.prompt,
            response_format=QuestionSchema
        )
    
     
    @traceable(run_type="chain", name="QuestionAgent")
    def invoke(self, topics: Tuple[str, str]) -> QuestionSchema:
        try:
            general_concept = topics[0]
            specific_concept = topics[1]

            result: QuestionSchema = self.agent.invoke(input={
                "messages": [
                    HumanMessage(content=f"<GENERAL CONCEPT>:\n{general_concept}\n\n<SPECIFIC CONCEPT>:\n{specific_concept}")]
            })
            return result['structured_response']
        except Exception as e:
            print(f'Error: {e}')
            return None
        
        
class ErrorAnalyzerAgent():
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
    
    def __init__(self, llm: BaseChatModel):

        self.agent_name = f"ErrorAnalyzerAgent"

        self.agent = create_agent(
            name=self.agent_name,
            model=llm,
            middleware=[],
            tools=[],
            system_prompt=ErrorAnalyzerAgent.prompt,
            response_format=ErrorAnalyzerSchema
        )
    
     
    @traceable(run_type="chain", name="ErrorAnalyzerAgent")
    def invoke(self, std_chars: StudentProfile, mastery: Tuple[float, float], question: QuestionSchema) -> ErrorAnalyzerSchema:
        try:
            options = question.option
            error_options = [opt for idx, opt in enumerate(options) if idx != int(question.correct_answer)]
            error_selected = random.choice(error_options)
            
            prompt =f"""
            <CHARACTERISTICS>
            
            {std_chars.to_plain_string()}

            <CONCEPTS AND MASTERY>
            - {question.main_concept_id} (Field area): {mastery[0]}
            - {question.specific_concept_id} (Specific): {mastery[1]}
            
            <QUESTION TEXT>
            {question.text}
            
            <OPTIONS>
            {options}
            
            <ANSWER ID>: {error_selected}
            <CORRECT ANSWER ID>: {question.correct_answer}
            """
            

            result: ErrorAnalyzerSchema = self.agent.invoke(input={"messages": [HumanMessage(content=prompt)]})

            return result['structured_response']
        except Exception as e:
            print(f'Error: {e}')
            return None