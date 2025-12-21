from typing import List, Optional
from pydantic import BaseModel

from SINKT.models import Concept, Relation
from SINKT.agents.question import QuestionResponse

class KnowledgeGraphModel(BaseModel):
    concepts: List[Concept]   
    relations: List[Relation]
    questions: Optional[List[QuestionResponse]]
    