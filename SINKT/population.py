import random 
import numpy as np
import networkx as nx
from typing import Dict, List 
from rich import print

from .models import KnowledgeGraphModel, StudentProfile, QuestionSchema, ErrorAnalyzerSchema
from .utils import normalize_id, get_llm, Models
from .agents import ErrorAnalyzerAgent

class PopulationSimulator:
    def __init__(self, kg_model: KnowledgeGraphModel):
        self.kg_model = kg_model
        self.graph = nx.DiGraph()
        self.question_bank = {}
        self._build_structure()
        
        # SINKT Constants
        self.LOGISTIC_SLOPE = 10
        self.LOGISTIC_CENTER = 0.6

    def _build_structure(self):
        # Graph Construction (Same as fixed version)
        for c in self.kg_model.concepts:
            nid = normalize_id(c.name)
            self.graph.add_node(nid, name=c.name)
            self.question_bank[nid] = []
        for r in self.kg_model.relations:
            if r.relation_type == 'prerequisite':
                self.graph.add_edge(normalize_id(r.source), normalize_id(r.target))
        for q in self.kg_model.questions:
            spec_id = normalize_id(q.specific_concept_id)
            main_id = normalize_id(q.main_concept_id)
            if spec_id in self.question_bank: self.question_bank[spec_id].append(q)
            if main_id in self.question_bank and main_id != spec_id: self.question_bank[main_id].append(q)

    def _initialize_student_knowledge(self, profile: StudentProfile) -> Dict[str, float]:
        """
        Initializes knowledge based on profile stats.
        'Technological Familiarity' boosts initial scores.
        """
        knowledge = {}
        try: order = list(nx.topological_sort(self.graph))
        except: order = list(self.graph.nodes)
        
        for node in order:
            parents = list(self.graph.predecessors(node))
            
            # Base initialization
            if not parents:
                # Roots: Random factor * proficiency * tech_boost
                base_val = np.random.uniform(0.1, 0.5) 
                val = base_val * (1 + profile.initial_proficiency)
            else:
                # Children: Dependent on parents
                parent_vals = [knowledge.get(p, 0.0) for p in parents]
                avg_parents = np.mean(parent_vals)
                val = np.clip(avg_parents * np.random.uniform(0.3, 1.0), 0.0, 1.0)
            
            # Apply Tech Familiarity Boost (assuming all nodes are tech-related)
            # A familiar student starts slightly higher everywhere
            val = min(1.0, val + (profile.technological_familiarity * 0.1))
            
            knowledge[node] = val
        return knowledge

    def _calculate_fi(self, concept_id: str, knowledge_state: Dict[str, float]) -> float:
        parents = list(self.graph.predecessors(concept_id))
        if not parents: return 1.0
        avg_parents = np.mean([knowledge_state[p] for p in parents])
        return 1 / (1 + np.exp(-self.LOGISTIC_SLOPE * (avg_parents - self.LOGISTIC_CENTER)))

    def run_student_session(self, profile: StudentProfile, n_attempts: int, explain_error: False) -> List[Dict]:
        knowledge = self._initialize_student_knowledge(profile)
        history = []
        
        for t in range(n_attempts):
            # 1. Unlock Logic
            unlockable = []
            for node in self.graph.nodes:
                if not self.question_bank.get(node): continue
                parents = list(self.graph.predecessors(node))
                if not parents or all(knowledge[p] > 0.5 for p in parents):
                    unlockable.append(node)
            
            if not unlockable: break
            
            # 2. Selection (Weighted by ignorance)
            weights = [1.0 - knowledge[c] for c in unlockable]
            selected_node = random.choices(unlockable, weights=weights, k=1)[0]
            question: QuestionSchema = random.choice(self.question_bank[selected_node])
            
            # if explain_error:
            #     agent = ErrorAnalyzerAgent(get_llm(Models.GPT5_1))
            #     agent.invoke(profile, )
            
            q_spec_id = normalize_id(question.specific_concept_id)
            q_main_id = normalize_id(question.main_concept_id)
                
            # 3. Probability (SINKT + Slip/Guess)
            ki = knowledge[selected_node]
            fi = self._calculate_fi(selected_node, knowledge)
            
            # Raw probability of knowing
            p_know = ki * fi
            
            # Apply Slip and Guess (IRT/BKT Logic)
            # P(Correct) = P(Know)*(1-Slip) + (1-P(Know))*Guess
            # Logical ability reduces slip slightly? Let's keep it simple for now.
            p_correct = p_know * (1 - profile.slip_rate) + (1 - p_know) * profile.guess_rate
            
            outcome = 1 if random.random() < p_correct else 0

            # CALLING AGENT TO EXPLAIN ERROR            
            if explain_error and outcome == 0:
                print(100*'=')
                print(question)
                mastery_main = knowledge[q_main_id]
                mastery_spec = knowledge[q_spec_id]
                print(f'MAIN MASTERY ({q_main_id}): {knowledge[q_main_id]}\nSPECIFIC MASTERY ({q_spec_id}): {knowledge[q_spec_id]}')
                agent = ErrorAnalyzerAgent(get_llm(Models.GPT5_1))
                result: ErrorAnalyzerSchema = agent.invoke(profile, (mastery_main, mastery_spec), question)
                print(100*'=')
                print(f'EXPLANATION: {result.explanation}\nERROR_TYPE: {result.error_type}')

            # 4. Learning Update
            # Base Learning Rate
            base_lr = 0.15 if outcome == 1 else 0.05
            
            # Apply Profile Speed
            real_lr = base_lr * profile.learning_speed
            
            # Update Helper
            def update_node(nid, rate):
                curr = knowledge[nid]
                new_v = curr + rate * (1.0 - curr)
                
                # Clamping
                parents = list(self.graph.predecessors(nid))
                if parents:
                    avg_par = np.mean([knowledge[p] for p in parents])
                    new_v = min(new_v, avg_par + 0.15)
                knowledge[nid] = new_v

            # Update Specific
            update_node(q_spec_id, real_lr)
            
            # Update Main (Proportional)
            if outcome == 1 and q_main_id in knowledge:
                degree = max(1, self.graph.degree[q_main_id])
                update_node(q_main_id, real_lr / degree)
            
            # 5. Log
            row = {
                "student_id": profile.id,
                "archetype": profile.archetype,
                "step": t + 1,
                "question_id": selected_node, # Tracking the node selected for practice
                "outcome": outcome,
                "p_know_latent": round(p_know, 3),
                "p_correct_observed": round(p_correct, 3)
            }
            # Log cognitive stats for analysis
            row.update({k: getattr(profile, k) for k in profile.__annotations__ if k not in ['id', 'archetype']})
            # Log knowledge state
            row.update(knowledge)
            
            history.append(row)
            
        return history