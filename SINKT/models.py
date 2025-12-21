from pydantic import BaseModel, Field
from typing import List, Dict, Set, Literal, Optional
from SINKT.agents.question import QuestionResponse

class Concept(BaseModel):
    name: str = Field(description="The formal name of the concept.")
    description: str = Field(description="Brief definition.")
    def __eq__(self, other):
        return isinstance(other, Concept) and self.name.lower() == other.name.lower()
    def __hash__(self):
        return hash(self.name.lower())
    model_config = {"frozen": True}
    
class Relation(BaseModel):
    source: str
    target: str
    relation_type: Literal['prerequisite']
    context: Optional[str]
    
    def __eq__(self, other):
        return (isinstance(other, Relation) and 
                self.source.lower() == other.source.lower() and 
                self.target.lower() == other.target.lower())
    
    def __hash__(self):
        return hash(f'{self.target.lower()}-{self.source.lower()}')
    
    model_config = {"frozen": True}
   
class KnowledgeGraphModel(BaseModel):
    concepts: List[Concept]   
    relations: List[Relation]
    questions: Optional[List[QuestionResponse]]
    

class StudentProfile(BaseModel):
    id: str
    archetype: str
    # Cognitive Attributes (0.0 to 1.0)
    initial_proficiency: float    # Base starting knowledge
    slip_rate: float              # Chance to mistake even if known
    guess_rate: float             # Chance to guess right if unknown
    learning_speed: float         # Multiplier for learning rate
    technological_familiarity: float # Boosts initial tech concepts
    logical_ability: float        # Slight boost to consistency
    text_interpretation: float    # Not explicitly used in calculation yet, but stored for metadata
    
    def to_plain_string(self) -> str:
        """Return all variables as a plain string."""
        attrs = [
            f"- id: {self.id}",
            f"- archetype: {self.archetype}",
            f"- initial_proficiency: {self.initial_proficiency}",
            f"- slip_rate: {self.slip_rate}",
            f"- guess_rate: {self.guess_rate}",
            f"- learning_speed: {self.learning_speed}",
            f"- technological_familiarity: {self.technological_familiarity}",
            f"- logical_ability: {self.logical_ability}",
            f"- text_interpretation: {self.text_interpretation}"
        ]
        return ', '.join(attrs)
    