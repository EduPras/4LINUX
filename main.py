from langsmith.wrappers import wrap_openai
from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path

from SINKT.agents import QuestionAgent
from SINKT.models import (
    KnowledgeGraphModel, 
    Concept,
    Relation,
)
from SINKT.utils import (get_llm, Models)
from SINKT.knowledge_graph import GraphSelector, GraphXMLBuilder

from langsmith import traceable
from tqdm import tqdm

load_dotenv('.env')

assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found"
assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not found"
assert os.getenv("LANGSMITH_API_KEY"), "ANTHROPIC_API_KEY not found"

ROOT = Path('notebooks/ebooks/LinuxFundamentals')
n = ROOT / 'nodes.xml'
r = ROOT / 'relations.xml'
q = ROOT / 'questions.xml' 

client = wrap_openai(OpenAI())

# @traceable(run_type="chain", name="QuestionCreator")
# def run():
#     kgb = GraphXMLBuilder()
#     kg: KnowledgeGraphModel = kgb.load(n, r)

#     gs = GraphSelector(kg)
#     pairs = gs.get_concept_pairs()

#     llm = get_llm(Models.GPT5_1)
#     question_agent = QuestionAgent(llm)

#     for p in tqdm(pairs):
#         q  = question_agent.invoke(p, langsmith_extra={"name": f'QUESTION({p[0]} / {p[1]})'})
#         kg.questions.append(q)
        
#     kgb.save(kg, Path('.'))
    
# # run()

# kgb = GraphXMLBuilder()
# kg: KnowledgeGraphModel = kgb.load(Path('.'))
# kgb.save(kg, Path('.'))
# print(kg.questions)

import pandas as pd
from SINKT.simulator import AdaptiveLearningSimulator

# 1. Load Data
xml_builder = GraphXMLBuilder()
# Update this path to where your XML files are located
input_path = Path(".") 

# Check if path exists to prevent error in example
if not input_path.exists():
    print(f"Please create directory {input_path} and place nodes.xml, relations.xml, questions.xml there.")
else:
    kg_model = xml_builder.load(input_path)

    # 2. Initialize Simulator
    # mastery_threshold=0.8 means student needs ~3 correct answers to master a concept and unlock the next
    sim = AdaptiveLearningSimulator(kg_model, mastery_threshold=0.75)

    # 3. Run Simulation
    # We simulate a "Good" student (85% success rate)
    history_data = sim.simulate_student_session(steps=400, success_rate=0.85)

    # 4. View Results as DataFrame (Synthetic Dataset)
    df = pd.DataFrame(history_data)
    
    # Display the learning path
    print("\n--- Synthetic Dataset Generated ---")
    print(df)

    # Optional: Analyze Progression
    mastered_count = df[df['status'] == 'MASTERED']['concept_id'].nunique()
    print(f"\nTotal Concepts Mastered: {mastered_count}")