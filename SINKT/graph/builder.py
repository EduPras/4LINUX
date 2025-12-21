from pathlib import Path
import xml.etree.ElementTree as ET

from .model import KnowledgeGraphModel, Concept, Relation, QuestionResponse
from SINKT.utils import prettify_xml

class GraphXMLBuilder():
    """
    Create a knowledge graph from nodes_xml_path and relations_xml_path
    """
    def __init__(self):
        pass
       
    def load(self, input_dir: Path) -> KnowledgeGraphModel:
        nodes_path = input_dir / 'nodes.xml'
        relations_path = input_dir / 'relations.xml'
        questions_path = input_dir / 'questions.xml'

        graph = KnowledgeGraphModel(concepts=[], relations=[], questions=[])
        if nodes_path and relations_path:
            # Load concepts from nodes.xml
            tree_nodes = ET.parse(nodes_path)
            for node in tree_nodes.getroot().findall("node"):
                name = node.get("name")
                description = node.get("description", "")
                graph.concepts.append(Concept(name=name, description=description))

            # Load relations from relations.xml
            tree_rels = ET.parse(relations_path)
            for rel in tree_rels.getroot().findall("relation"):
                source = rel.get("source")
                target = rel.get("target")
                rel_type = rel.get("type")
                context_elem = rel.find("context")
                context = context_elem.text if context_elem is not None else None
                graph.relations.append(
                    Relation(
                        source=source, 
                        target=target, 
                        relation_type=rel_type,
                        context=context
                ))

            tree_questions = ET.parse(questions_path)
            for q in tree_questions.getroot().findall("question"):
                text = q.get("text") 
                context = q.get("context") 
                correct_answer = q.get("answer_idx") 
                main_concept = q.get("main_concept") 
                specific_concept = q.get("specific_concept") 

                # Parse <option> child elements
                options = [opt.text for opt in q.findall("option")]

                graph.questions.append(
                    QuestionResponse(
                        text=text,
                        option=options,
                        correct_answer=correct_answer,
                        context=context,
                        main_concept_id=main_concept,
                        specific_concept_id=specific_concept,
                    )
                )
        return graph
                
    def save(self, graph: KnowledgeGraphModel, output_dir: Path) -> None:
        nodes_path = output_dir / 'nodes.xml' 
        relations_path = output_dir / 'relations.xml'
        questions_path = output_dir / 'questions.xml'

        # Build nodes.xml
        root_nodes = ET.Element("nodes")
        for idx, concept in enumerate(graph.concepts):
            node = ET.SubElement(root_nodes, "node")
            node.set("id", concept.name.replace(' ', '_').lower())
            node.set("name", concept.name)
            node.set("description", getattr(concept, 'description', ''))
            node.set("order", str(idx))

        # Build relations.xml
        root_rels = ET.Element("relations")
        for rel in graph.relations:
            rel_elem = ET.SubElement(root_rels, "relation")
            rel_elem.set("type", rel.relation_type)
            rel_elem.set("source", rel.source.replace(' ', '_').lower())
            rel_elem.set("target", rel.target.replace(' ', '_').lower())
            if rel.context:
                context_elem = ET.SubElement(rel_elem, "context")
                context_elem.text = rel.context
        
        # Build questions.xml
        root_question = ET.Element("questions")
        for q in graph.questions:
            q_elem = ET.SubElement(root_question, "question")
            q_elem.set("text", str(q.text))
            # q_elem.set("option", str(q.option))
            q_elem.set("answer_idx", str(q.correct_answer))
            q_elem.set("context", str(q.context))
            q_elem.set("main_concept", str(q.main_concept_id))
            q_elem.set("specific_concept", str(q.specific_concept_id))
            if q.option:
                for opt in q.option:
                    opt_elem = ET.SubElement(q_elem, "option")
                    if opt is not None:
                        opt_elem.text = str(opt)
                    else:
                        opt_elem.text = ""

        
        # Save pretty XML
        xml_nodes_str = prettify_xml(root_nodes)
        with open(nodes_path, "w", encoding="utf-8") as f:
            f.write(xml_nodes_str)

        xml_rels_str = prettify_xml(root_rels)
        with open(relations_path, "w", encoding="utf-8") as f:
            f.write(xml_rels_str)
            
        xml_questions_str = prettify_xml(root_question)
        with open(questions_path, "w", encoding="utf-8") as f:
            f.write(xml_questions_str)


        print(f"Graph saved in {output_dir}")
