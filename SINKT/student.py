from .models import StudentProfile
import random
import numpy as np

class StudentFactory:
    """Generates unique students based on archetypes."""
    ARCHETYPES = {
        # 1. The Ideal Learner (The Canonical Curve)
        # Starts low, learns fast, low noise. The "perfect" student data.
        "The Ideal Learner": {
            "initial_proficiency": 0.1,  
            "slip_rate": 0.05,           # Very careful
            "guess_rate": 0.1,           # Doesn't guess, tries to solve
            "learning_speed": 1.8,       # High P(T) - masters quickly
            "technological_familiarity": 0.7,
            "logical_ability": 0.9,
            "text_interpretation": 0.9
        },

        # 2. The System Gamer (Gaming the System)
        # High guess rate, high tech (knows how to exploit UI), zero learning.
        "The System Gamer": {
            "initial_proficiency": 0.1,
            "slip_rate": 0.1,
            "guess_rate": 0.75,          # Extremely high P(G) - clicking through
            "learning_speed": 0.1,       # Learning is effectively zero
            "technological_familiarity": 0.95, # Knows the UI better than the math
            "logical_ability": 0.4,
            "text_interpretation": 0.2
        },

        # 3. The Wheel-Spinner (Persistent Struggler)
        # Low knowledge, very low learning speed, but distinct from "Gamer" because they TRY (low guess).
        "The Wheel-Spinner": {
            "initial_proficiency": 0.05,
            "slip_rate": 0.1,
            "guess_rate": 0.15,          # Low guess (they are trying honestly)
            "learning_speed": 0.2,       # Stuck: P(T) is very low
            "technological_familiarity": 0.4,
            "logical_ability": 0.3,
            "text_interpretation": 0.3
        },

        # 4. The Careless (High Knowledge/High Slip)
        # Knows the answers but makes sloppy mistakes. High initial knowledge, high slip.
        "The Careless": {
            "initial_proficiency": 0.85, # They actually know the material
            "slip_rate": 0.35,           # High P(S) - error prone despite knowledge
            "guess_rate": 0.05,
            "learning_speed": 1.0,
            "technological_familiarity": 0.8,
            "logical_ability": 0.85,
            "text_interpretation": 0.5   # Often misreads the question
        },

        # 5. The Stop-Out (The Potential Dropout)
        # Moderate start, but frustration leads to disengagement.
        # Modeled here as low text/logic ability leading to a "wall".
        "The Stop-Out": {
            "initial_proficiency": 0.3,
            "slip_rate": 0.15,
            "guess_rate": 0.2,
            "learning_speed": 0.6,       # Slow progress leads to quitting
            "technological_familiarity": 0.3, # UX friction often causes dropouts
            "logical_ability": 0.4,
            "text_interpretation": 0.4
        },

        # 6. The Forgetful Learner (Swiss Cheese Memory)
        # Learns reasonable well, but "slips" frequently on things they should know.
        # *Note: Since your schema lacks a 'forget_rate', we simulate this with higher slip + variable logic.*
        "The Forgetful Learner": {
            "initial_proficiency": 0.2,
            "slip_rate": 0.25,           # Simulates forgetting previously known items
            "guess_rate": 0.15,
            "learning_speed": 1.3,       # They learn fast...
            "technological_familiarity": 0.6,
            "logical_ability": 0.5,      # ...but retention is spotty
            "text_interpretation": 0.6
        }
    }
    
    @staticmethod
    def create_student(student_id: int) -> StudentProfile:
        # Pick random archetype
        arch_name = random.choice(list(StudentFactory.ARCHETYPES.keys()))
        base = StudentFactory.ARCHETYPES[arch_name]
        
        # Add noise to make unique (PERTURBATION)
        def perturb(val, scale=0.05, min_v=0.01, max_v=0.99):
            return max(min_v, min(max_v, val + np.random.normal(0, scale)))

        return StudentProfile(
            id=f"S{student_id:03d}",
            archetype=arch_name,    
            initial_proficiency=perturb(base["initial_proficiency"], 0.1),
            slip_rate=perturb(base["slip_rate"], 0.02),
            guess_rate=perturb(base["guess_rate"], 0.05),
            learning_speed=perturb(base["learning_speed"], 0.1, 0.5, 2.0),
            technological_familiarity=perturb(base["technological_familiarity"], 0.1),
            logical_ability=perturb(base["logical_ability"], 0.1),
            text_interpretation=perturb(base["text_interpretation"], 0.1)
        )