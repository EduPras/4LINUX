# Validação dos Conceitos SINKT

Primeiramente foi extraído os dados do PDF usando a biblioteca **Docling** e depois realizado a extração, com a estratégia de **multiagentes** e **validação cruzada**. Além disso foi implementado tracing das chamadas das LLMs com **Langsmith** e a visualização dos grafos, destacando os clusters e nós com mais relações.

Outro ponto a se levantar é que nesse primeiro momento, ao contrário do que foi solicitado na tarefa, utilizei apenas a relação ``prerequisite``para que eu pudesse avaliar com mais clareza os resultados obtidos, visto que estava sendo um tanto quanto complexo a análise inicial com todas as relações solicitadas.

De acordo com as minha implementação, **multiagentes** se sobressaiu, visto que a outra abordagem raramente entra em consenso sobre quais conceitos e relações devem ser mantidas.

## Extração de dados
O SINKT já considera um dataset pronto para uso. Sendo assim essa seção busca extrair os conceitos de um ebook PDF. Primeiramente iremos transformar em Markdown, visto que é melhor utilizar texto puro ao invés de páginas de PDF. Além disso, essa proposta facilita a própria extração para o MAIC, posteriormente.


<div>

<img src="https://raw.githubusercontent.com/EduPras/4LINUX/refs/heads/master/notebooks/imgs/new_rotated.jpg" alt="Description" style="display: block; margin: 20px auto; width: 60%;" />

</div>

```py
class Concept(BaseModel):
    """Represents a single educational concept found in the text."""
    concept_name: str = Field(description="The formal name of the concept (e.g., 'Inductive Logic', 'Backpropagation').")
    chapter: List[int] = Field(description="The number of the current chapter, subchapter, etc (e.g., [1] for chapter 1, [1, 2] for subchapter 1.2, [1,2,5] for subsubchapter 1.2.5)")
    description: str = Field(description="A concise definition or summary of the concept based on the text.")

class PageExtraction(BaseModel):
    """Container for multiple concepts found on a specific page processing step."""
    concepts: List[Concept] = Field(description="List of concepts extracted from the current text window.")

class Relation(BaseModel):
    source: str = Field(description="The subject concept.")
    target: str = Field(description="The object concept.")
    # relation_type: Literal['prerequisite', 'including', 'part-of', 'property', 'definition']
    relation_type: Literal['prerequisite']
    context: Optional[str] = Field(description="Justification text.")

class ConceptList(BaseModel):
    concepts: List[Concept]

class RelationList(BaseModel):
    relations: List[Relation]
```

Primeiramente é criada a classe de conversão do PDF para markdown, utiliza-se da biblioteca Docling para realizar a conversão. Essa biblioteca permite extrair as imagens e tabelas do texto, posteriormente elas são incluídas no markdown final além de serem salvas juntas. ``EBookExtractor`` é a classe principal, encapsulando a classe criada anteriormente e servindo como uma interface de mais alto nível.

## Estratégias

Foi solicitado a execução de duas estratégias diferentes: multiagentes e validação cruzada. Segundo minha implementação e experimentos, o multiagente se sobressaiu.

### Multiagentes
Para a arquitetura de agentes foi utilizada a biblioteca **Langgraph** e **Langchain**. A ideia é gerar os conceitos e validar os mesmos na primeira fase e na segunda utilizar os conceitos criados para a geração das relações.

> Optou-se por utilizar neste momento apenas a relação ``prerequisite`` para uma melhor avaliação. Como o código está modular, foi necessário apenas uma pequena adição posteriormente para verificar o funcionamento com as outras relações propostas.

<div>

<img src="https://raw.githubusercontent.com/EduPras/4LINUX/refs/heads/master/notebooks/imgs/SINKT-graph.png" alt="Description" style="display: block; margin: 20px auto; width: 70%;" />

</div>

O **AgentState** é o estado utilizado pelos agentes como uma espécie de memória a curto prazo. Essa estrutura é atualizada conforme os agentes executam e capturam informações.

```python
class AgentState(TypedDict):
    """
    The graph state.
    We separate the 'working memory' of each agent to preserve history and context (Rule 2).
    """
    text_segment: str
    knowledge_base: KnowledgeGraph

    # Concepts
    extracted_concepts: List[Concept] # raw extraction

    # Delta logic
    new_concepts: List[Concept]
    known_concepts: List[Concept]

    concept_critiques: List[ConceptCritique]
    moderated_new_concepts: List[Concept]

    active_concepts: List[Concept]

    # Relation
    proposed_relations: List[Relation]

    # Delta logic
    new_relations: List[Relation]

    relation_critiques: List[RelationCritique]
    moderated_new_relations: List[Relation]

    # Graph
    final_graph_update: KnowledgeGraph
    workflow_trace: Annotated[List[str], operator.add] 
```
Esta estratégia é dividida em três fases:

1. **Extração de Conceitos**:
    - **relation_proposer**: Propõe relações aos conceitos criados anteriormente.
    - **relation_delta_filter**: Filtro, análogo ao que foi feito para os conceitos.
    - **relation_critic**: Propõe críticas e melhorias.
    - **relation_moderator**: Avalia se a relação deve ser descartada ou aceita.
2. **Extração de relações**:
    - **relation_proposer**: Propõe relações aos conceitos criados anteriormente.
    - **relation_delta_filter**: Filtro, análogo ao que foi feito para os conceitos.
    - **relation_critic**: Propõe críticas e melhorias.
    - **relation_moderator**: Avalia se a relação deve ser descartada ou aceita.
3. **Consenso**:
    - **consensus_agent**: Avalia os conceitos e relações criadas, garantindo e revisando a qualidade dos dados.
    - **auditor_node**: Este nó não utiliza LLM, mas verifica os traces garantindo que a entrada passou por todos agentes.
<center>

![](../notebooks/imgs/multiagents-pipeline.png)

</center>

Além disso foi configurado o **Langsmith** para fins de observabilidade.

![x](https://raw.githubusercontent.com/EduPras/4LINUX/refs/heads/master/notebooks/imgs/langsmith-trace.png)

### Agentes Validação Cruzada

Para os agentes de validação cruzada foi utilizado apenas o **Langchain** com ``create_agent``. Em uma primeira tentativa com um modelo com apenas um proponente e outro validator, o grafo ficou muito estenso e complexo. Já após colocar uma validação cruzada com dois proponentes e dois validadores, acabou que poucos conceitos e quase nenhuma relações eram selecionadas (o que pode ser melhorado com prompts mais abrangentes). Como a estratégia de multiagentes funcionou melhor, decidi já parar no início para não gastar mais tokens desnecessáriamente, além do tempo que levava para cada iteração.

```python
class ValidatorAgent():
    agent_number = 1
    prompt = SystemMessage("""
        You are a Strict Quality Control Agent for an Educational Knowledge Graph.

        Your Goal: Review the <RELATIONS> and <CONCEPTS> extracted from a <TEXT>.
        Filter out noise to ensure high-quality graph nodes.

        **ACCEPTANCE CRITERIA**:
        1. **Focus**: The concepts must be strong related to what is being debated on the text, not only mentions.
        2. **Correlation**: The relations must be strong, such that someone would struggle to learn the source
        concept without understand the target
        """)

    def __init__(self, llm: BaseChatModel):

        self.agent_name = f"ValidatorAgent_{ValidatorAgent.agent_number}"

        self.validator_agent = create_agent(
            name=self.agent_name,
            model=llm,
            middleware=[],
            tools=[],
            system_prompt=ValidatorAgent.prompt,
            response_format=ValidationResult
        )

        ValidatorAgent.agent_number += 1

    def invoke(self, kg: KnowledgeGraph) -> ValidationResult:
        concepts_str = "\n- ".join([c.name for c in kg.concepts])
        relations_str = "\n- ".join([f"{rel.source}-[PREREQUISITE]->{rel.target}" for rel in kg.relations])
        # Pass a dict, not a HumanMessage
        result: ValidationResult = self.validator_agent.invoke(input={
            "messages": [HumanMessage(content=f"<CONCEPTS>:\n{concepts_str}\n\n<RELATIONS>:\n{relations_str}")]
        })
        return result['structured_response']
```

```python
class CreatorAgent():
    agent_number = 1
    prompt = SystemMessage("""
        You are a Knowledge Graph Architect. You have two tasks:
        1. Identify the core <CONCEPTS> within the <CONTENT>.
        2. Identify the <RELATION> **prerequisite** between the generated <CONCEPTS> and/or <PREVIOUSLY KNOWN CONCEPTS>.

        ### RULES:
        1. The concepts must be core ideas inside the text.
        2. Do not select sentences, but keywords instead (e.g. Integral, Linux, Kernel, English, Noun, etc).
        3. Do not re-create a concept that is alredy within <PREVIOSLY KNOW CONCEPTS>
        3. Select only the concepts that are being strongly debated on the text, do not choose one that is merely mentioned.
        4. If you are creating a prerequisite relation between current concepts, the
        target must have been taught before source.
        5. You can create relations between <CONCEPTS> or <PREVIOUSLY KNOWN CONCEPTS>

    """)
    def __init__(self, llm: BaseChatModel):
        self.agent_name = f"CreatorAgent_{CreatorAgent.agent_number}"

        self.creator_agent = create_agent(
            name=self.agent_name,
            model=llm,
            tools=[],
            system_prompt=CreatorAgent.prompt,
            response_format=KnowledgeGraph
        )

        CreatorAgent.agent_number += 1

    def invoke(self, previous_concepts_str: str, text_content: str) -> KnowledgeGraph:
        human_message = HumanMessage(
            content=f"""<PREVIOUSLY KNOWN CONCEPTS>:\n{previous_concepts_str}\n\n<CONTENT>:\n{text_content}""")
        return self.creator_agent.invoke(input={"messages": [human_message]})['structured_response']
```