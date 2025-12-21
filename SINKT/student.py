from .models import StudentProfile
import random
import numpy as np

class StudentFactory:
    """Generates unique students based on archetypes."""
    ARCHETYPES = {
        # 1. Analyst: Careful, logical, slow but accurate
        "analyst": {
            "initial_proficiency": 0.22,
            "slip_rate": 0.07,
            "guess_rate": 0.2,
            "learning_speed": 2, # 2x
            "technological_familiarity": 0.65,
            "logical_ability": 0.9,
            "text_interpretation": 0.8
        },

        # 2. Unstable: Inconsistent, sometimes good, sometimes not
        "unstable": {
            "initial_proficiency": 0.18,
            "slip_rate": 0.25,
            "guess_rate": 0.1,
            "learning_speed": 1,
            "technological_familiarity": 0.5,
            "logical_ability": 0.4,
            "text_interpretation": 0.5
        },

        # 3. Hurry: Fast, careless, guesses a lot
        "hurry": {
            "initial_proficiency": 0.19,
            "slip_rate": 0.28,
            "guess_rate": 0.08,
            "learning_speed": 0.7,
            "technological_familiarity": 0.7,
            "logical_ability": 0.5,
            "text_interpretation": 0.55
        },

        # 4. Expert: High knowledge, low slip, learns fast
        "expert": {
            "initial_proficiency": 0.55,
            "slip_rate": 0.05,
            "guess_rate": 0.3,
            "learning_speed": 2.5,
            "technological_familiarity": 0.85,
            "logical_ability": 0.95,
            "text_interpretation": 0.85
        },

        # 5. Dedicated: Average but persistent, learns steadily
        "dedicated": {
            "initial_proficiency": 0.25,
            "slip_rate": 0.12,
            "guess_rate": 0.18,
            "learning_speed": 1.5,
            "technological_familiarity": 0.6,
            "logical_ability": 0.7,
            "text_interpretation": 0.7
        },

        # 6. Struggler: Low knowledge, slow learning, high slip
        "struggler": {
            "initial_proficiency": 0.09,
            "slip_rate": 0.22,
            "guess_rate": 0.1,
            "learning_speed": 0.8,
            "technological_familiarity": 0.35,
            "logical_ability": 0.25,
            "text_interpretation": 0.3
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