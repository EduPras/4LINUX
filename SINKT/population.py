import random
import numpy as np
import networkx as nx
from typing import Dict, List
import logging

from SINKT.agents.question import QuestionResponse
from SINKT.agents.error_analyzer import ErrorAnalyzerResponse, ErrorAnalyzerAgent
from SINKT.graph.model import KnowledgeGraphModel

from .models import StudentProfile
from .utils import normalize_id, get_llm, Models

class PopulationSimulator:
    """
    Apply the concepts described in [SINKT_Base_Individual](https://github.com/EduPras/4LINUX/blob/master/notebooks/SINKT_Base_Individual.ipynb)
    to create a synthetic dataset.
    """
    
    def __init__(self, kg_model: KnowledgeGraphModel):
        self.kg_model = kg_model
        self.graph = nx.DiGraph()
        self.question_bank = {}
        self._build_structure()
        
        # SINKT Constants
        self.LOGISTIC_SLOPE = 10
        self.LOGISTIC_CENTER = 0.6

    def _build_structure(self):
        # Graph Construction 
        for c in self.kg_model.concepts:
            nid = normalize_id(c.name)
            self.graph.add_node(nid, name=c.name)
            self.question_bank[nid] = []
        for r in self.kg_model.relations:
            self.graph.add_edge(normalize_id(r.source), normalize_id(r.target), attr=r.relation_type)
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
        
        min_val = 0.05
        for node in order:
            parents = list(self.graph.predecessors(node))
            # Base initialization
            if not parents:
                # Roots: Use initial proficiency directly, plus some noise
                val = np.random.normal(profile.initial_proficiency, np.clip(np.random.normal(0.4, 0.2), min_val, 1))
                val = np.clip(val, min_val, 1)
            else:
                # Children: Dependent on parents, but never below min_val
                parent_vals = [knowledge.get(p, min_val) for p in parents]
                avg_parents = np.mean(parent_vals)
                val = np.clip(avg_parents * np.random.uniform(0.7, 1.0), min_val, 1.0)

            # Apply Tech Familiarity Boost (assuming all nodes are tech-related)
            val = min(1.0, val + (profile.technological_familiarity * 0.6))
            knowledge[node] = val

            # After initializing this node, update all its parents if not set, based on their children's values
            for parent in parents:
                if parent not in knowledge:
                    # Get all children of this parent that have been initialized
                    children = list(self.graph.successors(parent))
                    child_vals = [knowledge[c] for c in children if c in knowledge]
                    if child_vals:
                        # Set parent as the average of its initialized children's values
                        knowledge[parent] = np.clip(np.mean(child_vals), min_val, 1.0)
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
                if not parents or all(knowledge[p] > 0.75 for p in parents):
                    unlockable.append(node)
            if not unlockable:
                break

            # 2. Selection (Weighted by ignorance)
            weights = [1.0 - knowledge[c] for c in unlockable]
            selected_node = random.choices(unlockable, weights=weights, k=1)[0]
            question: QuestionResponse = random.choice(self.question_bank[selected_node])

            q_spec_id = normalize_id(question.specific_concept_id)
            q_main_id = normalize_id(question.main_concept_id)

            # 3. Probability (ki + noise)
            ki = knowledge[selected_node]
            noise = np.random.normal(0, 0.05)
            p_know = min(max(ki + noise, 0.0), 1.0)

            # 4. Apply Slip and Guess (IRT/BKT Logic)
            p_correct = p_know * (1 - profile.slip_rate) + (1 - p_know) * (profile.guess_rate)

            outcome = 1 if random.random() < p_correct else 0

            # CALLING AGENT TO EXPLAIN ERROR            
            if explain_error and outcome == 0:
                mastery_main = knowledge[q_main_id]
                mastery_spec = knowledge[q_spec_id]
                agent = ErrorAnalyzerAgent(get_llm(Models.GPT5_1))
                result: ErrorAnalyzerResponse = agent.invoke(profile, (mastery_main, mastery_spec), question)
                print(result.text)

            # 4. Learning Update
            base_lr = 0.15 if outcome == 1 else 0.05
            real_lr = base_lr * profile.learning_speed

            def update_node(nid, rate):
                curr = knowledge[nid]
                new_v = curr + rate * (1.0 - curr)
                knowledge[nid] = new_v

            update_node(q_spec_id, real_lr)
            if outcome == 1 and q_main_id in knowledge:
                degree = max(1, self.graph.degree[q_main_id])
                update_node(q_main_id, real_lr / degree)

            # 5. Update child concepts (those for which selected_node is a prerequisite)
            children = list(self.graph.successors(selected_node))
            n_prereq = [len(list(self.graph.predecessors(child))) for child in children]
            for child, n_pre in zip(children, n_prereq):
                if n_pre > 0:
                    update_val = knowledge[selected_node] / n_pre
                    knowledge[child] = min(1.0, knowledge[child] + update_val)

            row = {
                "student_id": profile.id,
                "archetype": profile.archetype,
                "step": t + 1,
                "question_id": selected_node, # Tracking the node selected for practice
                "outcome": outcome,
                "p_know_latent": round(p_know, 3),
                "p_correct_observed": round(p_correct, 3)
            }
            row.update({k: getattr(profile, k) for k in profile.__annotations__ if k not in ['id', 'archetype']})
            row.update(knowledge)
            history.append(row)
            # break
        return history