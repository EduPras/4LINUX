import os
import sys
from pathlib import Path
# current_dir = Path(os.path.dirname(os.path.abspath('.')))
# sys.path.append(current_dir / 'SINKT')
# sys.path.append(current_dir)

import pandas as pd
from pathlib import Path
import random
from dotenv import load_dotenv
from langsmith.wrappers import wrap_openai
from openai import OpenAI

from SINKT.agents.question import QuestionAgent, QuestionResponse, QuestionContext
from SINKT.agents.error_analyzer import ErrorAnalyzerAgent, ErrorAnalyzerResponse, ErrorAnalyzerContext
from SINKT.models import (
    KnowledgeGraphModel, 
    Concept,
    Relation,
)
from SINKT.utils import get_llm, Models, normalize_id
from SINKT.graph.builder import GraphXMLBuilder
from SINKT.graph.selector import GraphSelector

from SINKT.student import StudentFactory
from SINKT.population import PopulationSimulator

load_dotenv('.env')

assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY not found"
assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY not found"
assert os.getenv("LANGSMITH_API_KEY"), "ANTHROPIC_API_KEY not found"
client = wrap_openai(OpenAI())

print('Loaded')


def generate_synthetic_dataset(n_students=10):
    xml_builder = GraphXMLBuilder()
    input_path = Path(".")
    
    if not input_path.exists():
        print("Data path not found.")
        return None

    kg_model = xml_builder.load(input_path)
    sim = PopulationSimulator(kg_model)
    
    all_data = []
    print(f"Generating data for {n_students} students...")
    
    for i in range(1, n_students + 1):
        # Create unique profile
        profile = StudentFactory.create_student(i)
        
        # Random sequence length (30-60 interactions)
        n_steps = random.randint(1000, 1001)
        
        # Run Session
        student_history = sim.run_student_session(profile, n_steps, explain_error=False)
        all_data.extend(student_history)
        
        if i % 10 == 0:
            print(f"Processed {i} students...")
            
    df = pd.DataFrame(all_data)
    return df, kg_model

df_population, kg_model = generate_synthetic_dataset(n_students=1)

if df_population is not None:
    print("\n--- Dataset Generation Complete ---")
    print(f"Total Interactions: {len(df_population)}")
    print("\nSample Data:")
    # display(df_population[['student_id', 'archetype', 'step', 'question_id', 'outcome', 'global_mastery']].head())
    
    # Save to CSV
    df_population.to_csv("synthetic_student_population.csv", index=False)
    print("Saved to synthetic_student_population.csv")