import networkx as nx
import numpy as np
from typing import List, Tuple, Dict

from SINKT.utils import normalize_id
from .model import KnowledgeGraphModel
class GraphSelector:
    def __init__(self, kg_model: KnowledgeGraphModel):
        self.kg_model = kg_model
        self.graph = nx.Graph()
        self._build_graph()
        
    def _build_graph(self):
        # nodes = concept names (normalized)
        for concept in self.kg_model.concepts:
            node_id = normalize_id(concept.name)
            self.graph.add_node(node_id, name=concept.name, description=concept.description)
            
        # edges = relations (normalized)
        for rel in self.kg_model.relations:
            src_id = normalize_id(rel.source)
            tgt_id = normalize_id(rel.target)
            
            # check if both concepts exist
            if self.graph.has_node(src_id) and self.graph.has_node(tgt_id):
                self.graph.add_edge(src_id, tgt_id)
            else:
                pass

    def get_concept_pairs(self) -> List[Tuple[str, str]]:
        """
        Get pairs: (hub_id, leaf_id)
        """
        pairs = []
        degrees = dict(self.graph.degree())
        
        if not degrees: return []
        
        sorted_degrees = sorted(degrees.values())
        threshold_hub = np.percentile(sorted_degrees, 96)
        threshold_spec = np.percentile(sorted_degrees, 50)

        # Main topics (Hubs)
        hubs = [n for n, d in degrees.items() if d >= threshold_hub]
        
        for hub in hubs:
            # Hub's neighbours
            neighbors = list(self.graph.neighbors(hub))
            # Specific nodes (not hubs)
            specifics = [n for n in neighbors if degrees[n] <= threshold_spec]
            if specifics:
                for s in specifics:
                    pairs.append((hub, s))
                # chosen_spec = random.choice(specifics)
                # pairs.append((hub, chosen_spec))
                
        return list(set(pairs))

    def get_node_info(self, node_id: str) -> Dict:
        """Return name and description of a node"""
        node = self.graph.nodes[node_id]
        return {
            "name": node.get("name", node_id),
            "description": node.get("description", "")
        }
        