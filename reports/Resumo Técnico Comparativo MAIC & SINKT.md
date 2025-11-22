# LAMIA

**Resumo Técnico Comparativo MAIC & SINKT**

**Eduardo Prasniewski**
18 de novembro de 2025

---

## 1. Anotações

### 1.1 MAIC

MAIC (Massive AI-empowered Course) é um novo paradigma para a educação online proposto para evoluir além do modelo estático "um vídeo para N alunos" dos MOOCs tradicionais. O objetivo principal do MAIC é equilibrar escalabilidade (servir muitos alunos) com adaptabilidade (fornecer uma experiência de aprendizagem personalizada). Ele atinge isso construindo uma sala de aula dinâmica "N agentes para 1 aluno", onde um único aluno interage com uma equipe de agentes conduzidos por IA.

#### Arquitetura de Duas Fases

A estrutura MAIC é implementada combinando dois sistemas distintos: **Slide2Lecture** para preparação de curso offline e **SimClass** para entrega de curso em tempo real.

O núcleo do SimClass é o seu **Controlador de Sessão**, um meta-agente que dirige o fluxo da aula. Ele instrui o Agente Professor de IA a entregar o roteiro, enquanto também gerencia um conjunto de Agentes Colegas de Classe (como o Pensador Profundo ou Mente Inquisitiva) para simular uma discussão colaborativa e ao vivo. Quando o aluno interage, o Controlador de Sessão gerencia dinamicamente a conversação, misturando perfeitamente o roteiro pré-planejado com o diálogo adaptativo em tempo real.

#### 1.1.1 Fluxo de Trabalho de Ensino

**Fase de Leitura (Read Stage)**
O processo começa com os slides do curso, $\mathcal{P}$, definidos como um conjunto de páginas individuais:

$$
\mathcal{P}=\{P_{i}\}_{1\le i\le|\mathcal{P}|} \tag{1}
$$

Estes são processados em recursos de aprendizagem inteligentes estruturados, $\hat{\mathcal{P}}$:

$$
\hat{\mathcal{P}}=\{\langle P_{i},D_{i},K_{j}\rangle\}_{1\le j\le|\hat{P}|}^{1\le i\le|\hat{P}|} \tag{2}
$$

**Fase 1 - Pipeline de Ensino Offline (Slide2Lecture):**
Este é o motor de criação do curso. Em vez de um humano gastar semanas gravando um vídeo, a estrutura Slide2Lecture atua como um pipeline de pré-processamento. Um professor fornece seus slides de aula brutos (por exemplo, um arquivo PowerPoint). O Slide2Lecture então usa LLMs multimodais para analisar este conteúdo (tanto texto quanto visual) e gera automaticamente um "roteiro de curso" completo e estruturado. Este roteiro é uma lista sequencial de ações de ensino, incluindo não apenas o conteúdo da aula (*ReadScript*), mas também quando mudar de slide (*ShowFile*) e quando questionar o aluno (*AskQuestion*).

**1.1 Extração de Conteúdo do Slide**
Uma função $f_{T}^{1}$ extrai o conteúdo textual $(P_{i}^{t})$ e visual $(P_{i}^{v})$ de cada página $P_{i}$.

$$
f_{T}^{1}:P_{i}\rightarrow\langle P_{i}^{t},P_{i}^{v}\rangle \tag{3}
$$

**1.2 Extração de Estrutura**
Uma segunda função $f_{T}^{2}$ gera uma descrição abrangente $D_{i}$ a partir do conteúdo extraído.

$$
f_{T}^{2}:\langle P_{i}^{t},P_{i}^{v}\rangle\rightarrow D_{i} \tag{4}
$$

**Fase de Planejamento (Plan Stage)**
Esta fase define as ações de ensino, $\mathcal{T}$, como uma tupla de tipo e valor.

$$
\tau = (\text{tipo, valor}) \tag{5}
$$

O tipo de ação é selecionado a partir de um conjunto predefinido:

$$
\text{tipo} \in \{\text{ShowFile, ReadScript, AskQuestion}\} \tag{6}
$$

Cada ação $\mathcal{T}_{n}$ está associada a um conteúdo específico $\hat{P}_{\mathcal{T}}$:

$$
\langle\mathcal{T}_{n},\hat{P}_{\mathcal{T}}\rangle \tag{7}
$$

#### 1.1.2 Fluxo de Trabalho de Aprendizagem

**Papéis da Turma e Conteúdo**
O ambiente de aprendizagem é definido por um conjunto de papéis da turma $\hat{\mathcal{R}}$ (por exemplo, TI, EC, CM) e o roteiro instrucional sequenciado $C$.

$$
\mathcal{R} = \{r\} \tag{8}
$$

$$
C=\{c_{1},...,c_{t}\} \tag{9}
$$

**Fase 2 - Ambiente de Aprendizagem Online (SimClass):**
Esta é a "sala de aula interativa" que o aluno experimenta. A estrutura SimClass toma o "roteiro de curso estruturado" gerado pelo Slide2Lecture como sua entrada. Em seguida, ela executa uma simulação multiagente em tempo real.

**Controlador de Sessão**
O Controlador de Sessão gerencia o ambiente de aprendizagem em tempo real.

**Receptor de Estado da Turma**
O histórico de diálogo $H_{t}$ é a união de todas as falas $u_{i}$ de todos os agentes $a_{j}$ até o tempo $t$.

$$
H_{t}=\bigcup(u_{i}^{a_{j}})^{t} \tag{10}
$$

O estado geral da turma $S_{t}$ é uma função dos materiais ensinados $P_{t}$, do histórico $H_{t}$ e dos papéis ativos $\hat{\mathcal{R}}$:

$$
S_{t}=\{P_{t},H_{t}|\hat{\mathcal{R}}\}, \text{ onde } P_{t}\subseteq\mathcal{P} \tag{11}
$$

**Função do Agente Gerenciador**
A lógica central do controlador é uma função $f_{L}$ que pega o estado atual $S_{t}$ e seleciona o próximo agente $a_{t}$ e a ação de ensino $\mathcal{T}$ a ser executada.

$$
f_{L}(S_{t}) \rightarrow (a, \mathcal{T}), \quad a \in \mathcal{A}, \mathcal{T} \in \mathcal{T} \tag{12}
$$

---

### 1.2 SINKT

O artigo apresenta o SINKT, um modelo inovador para Rastreamento de Conhecimento (*Knowledge Tracing - KT*), que é a tarefa de prever se um aluno responderá corretamente à próxima pergunta com base em seu desempenho anterior. O SINKT busca resolver os problemas de *cold-start* (partida a frio), escassez de dados (*data sparsity*) e falta de estrutura dos modelos tradicionais de KT.

#### 1.2.1 Definição do problema

Consideramos um conjunto de alunos $\mathcal{S}$, um conjunto de perguntas $\mathcal{Q}$ e um conjunto de conceitos $\mathcal{C}$. O histórico de aprendizagem de um aluno $s \in \mathcal{S}$ é registrado como uma sequência:

$$
R_s = \{(q_1, r_1), (q_2, r_2), ..., (q_T, r_T)\}
$$

Onde $q_{t} \in \mathcal{Q}$ é a pergunta respondida na etapa de tempo $t$, e $r_{t} \in \{0,1\}$ é a correção da resposta (1 para correto, 0 para incorreto).

Dado o histórico de aprendizagem $R_{s}$ de um aluno e uma nova pergunta $q_{T+1}$, o objetivo da tarefa de Rastreamento de Conhecimento (KT) é prever a probabilidade de o aluno responder corretamente à nova pergunta. Isso é denotado como:

$$
p(r_{T+1}=1|R_{s},q_{T+1}) \tag{13}
$$

Na tarefa de KT tradicional (transdutiva), o conjunto de perguntas nos dados de treinamento e nos dados de teste são os mesmos ($Q_{trein}=Q_{teste}$). Este trabalho também aborda a tarefa de KT indutiva, onde o modelo deve fazer previsões para novas perguntas não vistas durante o treinamento ($Q_{trein} \neq Q_{teste}$).

Esta seção detalha a estrutura SINKT, que é composta por quatro componentes principais: um **Codificador de Informação Textual (TIEnc)**, um **Codificador de Informação Estrutural (SIEnc)**, um **Codificador de Estado do Aluno** e um **Preditor de Resposta**.

#### 1.2.2 Codificador de Informação Textual (TIEnc)

Para capturar a informação semântica de conceitos e perguntas, um Modelo de Linguagem Pré-treinado (PLM) é usado como codificador semântico. O texto puro de cada conceito $c_{i}$ e pergunta $q_{i}$ é inserido no PLM para adquirir seus respectivos vetores de representação:

$$
x_{i}^{c}=PLM_{c}(\text{TEXT}(c_{i}))\in\mathbb{R}^{d_{t}} \tag{14}
$$

$$
x_{i}^{q}=PLM_{q}(\text{TEXT}(q_{i}))\in\mathbb{R}^{d_{r}} \tag{15}
$$

Aqui, $d_{t}$ representa a dimensão de codificação do PLM. Esses vetores, $x_{i}^{c}$ e $x_{i}^{q}$, servem como as entradas semânticas iniciais para os módulos subsequentes.

#### 1.2.3 Codificador de Informação Estrutural (SIEnc)

Um codificador de grafo heterogêneo multi-camadas é projetado para capturar a informação estrutural do grafo conceito-pergunta. Este codificador processa três tipos de relacionamentos usando três Redes de Atenção Gráfica (GATs) distintas:

1.  **GAT Conceito-Pergunta (C-Q):** Funde representações de conceitos vizinhos para uma pergunta alvo.
2.  **GAT Conceito-Conceito (C-C):** Integra informações de conceitos vizinhos para um conceito alvo.
3.  **GAT Pergunta-Conceito (Q-C):** Integra informações de perguntas vizinhas para um conceito alvo.

Seja $\mathcal{N}_{c_{i}}^{q}$ o conjunto de perguntas vizinhas para o conceito $c_{i}$, $\mathcal{N}_{c_{i}}^{c}$ os conceitos vizinhos para o conceito $c_{i}$, e $\mathcal{N}_{q_{i}}^{c}$ os conceitos vizinhos para a pergunta $q_{i}$.

O mecanismo de atenção para o **GAT Conceito-Pergunta (C-Q)**, que atualiza as representações das perguntas, é definido como:

$$
\alpha_{i,j}^{cq}=\frac{\exp(\text{LeakyReLU}(a_{cq}^{T}(x_{i}^{q}\oplus x_{j}^{c})))}{\sum_{c_{k}\in \mathcal{N}_{q_{i}}^{c}}\exp(\text{LeakyReLU}(a_{cq}^{T}(x_{i}^{q}\oplus x_{k}^{c})))} \tag{16}
$$

$$
e_{i}^{cq}=\sum_{c_{j}\in\mathcal{N}_{q_{i}}^{c}}\alpha_{i,j}^{cq}\cdot(W_{cq}x_{j}^{c}) \tag{17}
$$

Onde $W_{cq}$ é a matriz de peso de agregação, $a_{cq}$ é o vetor de peso de atenção, e $\oplus$ denota concatenação.

De forma similar, os **GATs Conceito-Conceito (C-C)** e **Pergunta-Conceito (Q-C)** são definidos como:

$$
\alpha_{i,j}^{cc}=\frac{\exp(\text{LeakyReLU}(a_{cc}^{T}(x_{i}^{c}\oplus x_{j}^{c})))}{\sum_{c_{k}\in \mathcal{N}_{c_{i}}^{c}}\exp(\text{LeakyReLU}(a_{cc}^{T}(x_{i}^{c}\oplus x_{k}^{c})))} \tag{18}
$$

$$
e_{i}^{cc}=\sum_{c_{j}\in \mathcal{N}_{c_{i}}^{c}}\alpha_{i,j}^{cc}\cdot(W_{cc}x_{j}^{c}) \tag{19}
$$

$$
\alpha_{i,j}^{qc}=\frac{\exp(\text{LeakyReLU}(a_{qc}^{T}(x_{i}^{c}\oplus x_{j}^{q})))}{\sum_{q_{k}\in \mathcal{N}_{c_{i}}^{q}}\exp(\text{LeakyReLU}(a_{qc}^{T}(x_{i}^{c}\oplus x_{k}^{q})))} \tag{20}
$$

$$
e_{i}^{qc}=\sum_{q_{j}\in\mathcal{N}_{c_{i}}^{q}}\alpha_{i,j}^{qc}\cdot(W_{qc}x_{j}^{q}) \tag{21}
$$

Para enfatizar a informação semântica original, o SINKT introduz o **conhecimento saltitante (jumping knowledge)**. A representação do nó na $l$-ésima camada do codificador é:

$$
x_{i}^{c(l)}=\text{ReLU}(W_{c}x^{c(l-1)}+e_{i}^{cc}+e_{i}^{qc}) \tag{22}
$$

$$
x_{i}^{q(l)}=\text{ReLU}(W_{q}x^{q(l-1)}+e_{i}^{cq}) \tag{23}
$$

Onde $W_{c}$ e $W_{q}$ são matrizes de peso treináveis. A entrada na camada 0 é inicializada pela saída do TIEnc:

$$
x_{i}^{c(0)}=x_{i}^{c}, \quad x_{i}^{q(0)}=x_{i}^{q} \tag{24}
$$

Após $k$ camadas, obtemos os vetores de representação finais $\tilde{c}_{i}\in\mathbb{R}^{d}$ e $\tilde{q}_{i}\in\mathbb{R}^{d}$.

#### 1.2.4 Codificador de Estado do Aluno

Para modelar o histórico de aprendizagem do aluno, as interações são transformadas para o nível de conceito. Para uma pergunta $q_{t}$ com um conjunto de conceitos $\mathcal{C}_{q_{t}}$, a representação no nível de conceito $u_{t}$ é a média dos vetores de conceito:

$$
u_{t}=\frac{1}{|\mathcal{C}_{q_{t}}|}\sum_{c_{i}\in\mathcal{C}_{q_{t}}}\tilde{c_{i}} \tag{25}
$$

Para representar conjuntamente o item e a correção da resposta $r_{t}$, um vetor de interação $v_{t}\in\mathbb{R}^{2d}$ é introduzido:

$$
v_{t}=\begin{cases}u_{t}\oplus 0 & \text{se } r_{t}=1\\ 0\oplus u_{t} & \text{se } r_{t}=0\end{cases} \tag{26}
$$

Onde $0\in\mathbb{R}^{d}$ é um vetor nulo. Esta sequência é modelada usando uma **Unidade Recorrente com Portões (GRU)**:

$$
u_{r}=\sigma(W_{r}(v_{t}\oplus h_{t-1})+b_{r}) \tag{27}
$$

$$
u_{z}=\sigma(W_{z}(v_{t}\oplus h_{t-1})+b_{z}) \tag{28}
$$

$$
u_{h}=\tanh(W_{h}(v_{t}\oplus(u_{r}*h_{t-1}))+b_{h}) \tag{29}
$$

$$
h_{t}=(1-u_{z})*u_{h}+u_{z}*h_{t-1} \tag{30}
$$

O estado oculto $h_{t}\in\mathbb{R}^{d}$ representa o estado de conhecimento do aluno na etapa de tempo $t$.

#### 1.2.5 Predição de Resposta

A probabilidade de uma resposta correta $y_{t+1}$ para a próxima pergunta $q_{t+1}$ é prevista combinando o estado de conhecimento do aluno $h_{t}$, a representação da pergunta $\tilde{q}_{t+1}$ e a representação no nível de conceito da pergunta $u_{t+1}$:

$$
y_{t+1}=\sigma(W_{p}(h_{t}\oplus\tilde{q}_{t+1}\oplus u_{t+1})+b_{p}) \tag{31}
$$

Onde $W_{p}\in\mathbb{R}^{3d}$ e $b_{p}\in\mathbb{R}$ são parâmetros treináveis. O modelo é treinado minimizando a perda de entropia cruzada entre a previsão $y_t$ e a resposta de verdade fundamental $r_{t}$:

$$
\mathcal{L}=-\sum_{t=1}^{T}(r_{t}\log y_{t}+(1-r_{t})\log(1-y_{t})) \tag{32}
$$

#### 1.2.6 Discussões

A natureza estrutural e indutiva do SINKT possibilita diversas aplicações únicas em EdTech:

* **Design Curricular:** Gera automaticamente mapas de habilidades de pré-requisito (Árvores de Habilidades) usando LLMs para inferir o fluxo lógico entre novos conceitos.
* **Diagnóstico da Causa Raiz:** Rastreia erros de volta através do grafo para identificar lacunas de conhecimento fundamental em vez de apenas o erro imediato.
* **Calibração Cold Start:** Estima instantaneamente a dificuldade e o escopo de conteúdo novo e não visto, analisando o texto da pergunta.
* **Tutoria Adaptativa:** Facilita a criação de problemas de prática diversos e únicos.

**Comparação com BKT e Integração**
* **Diferença:** O BKT é um modelo probabilístico e transdutivo que depende de dados de ID históricos, enquanto o SINKT é um modelo de deep learning indutivo que depende de vetores semânticos ricos e grafos de conceito explícitos.
* **Integração:** Eles podem ser usados em conjunto. O método ideal é executar o BKT em paralelo e alimentar sua probabilidade de domínio interpretável como um recurso de entrada adicional na camada de previsão do SINKT.

**Treinamento do Modelo e Resolução de Cold Start**
* **Componentes:** O "Modelo SINKT" consiste em codificadores PLM reutilizáveis (por exemplo, BERT) e camadas centrais treinadas sob medida (GRU/GAT).
* **Estratégia de Treinamento:** 1) Pré-treinamento Universal em dados públicos agregados; 2) Ajuste Fino Específico do Cliente (opcional).
* **Cold Start:** Para um novo curso de cliente sem histórico, o SINKT usa o TIEnc pré-treinado universalmente.

---

## 2. Simulações

### 2.1 MAIC

Esta seção detalha a aplicação do MAIC, onde o aluno repete o mesmo erro mais de uma vez.

* **Cenário:** Erro Repetido no Conceito K01 (IndexError em Python).
* **Detalhe:** Erro na tentativa 2, associado à falha em acessar corretamente um índice dentro dos limites de uma lista.
* **Gatilho do MAIC:** O sistema de agentes é acionado porque a falha é considerada de alta prioridade.

**Tabela 1: Diálogo simulado**

| Agente | Mensagem e Papel (Resposta) |
| :--- | :--- |
| **Tutor** | "Olá! Notei que você teve dificuldade na questão de indexação. Lembre-se que em Python, a contagem começa em 0 e o último item é sempre tamanho - 1. Tentar acessar um índice maior causa o erro que você viu. Vamos tentar corrigir o código juntos?" |
| **Conselho** | "Percebi que você assistiu ao vídeo, mas errou o quiz logo em seguida. Talvez a teoria ainda esteja abstrata. Sugiro que você olhe este diagrama visual sobre como os índices funcionam na memória antes de prosseguir para o próximo exercício prático. Isso vai consolidar sua base." |
| **Amigo** | "Nossa, eu sempre confundo esses índices também! É super normal errar isso no começo. O importante é que no exercício final você mandou super bem. Bora pro próximo que a gente consegue!" |

#### 2.1.2 Objetivo pedagógico e resultado esperado

* **Objetivo Pedagógico Central (Scaffolding):** Garantir a correção da falha conceitual de indexação.
* **Três Focos de Intervenção:**
    1.  **Cognitivo/Conceitual:** O Tutor fornece a correção técnica imediata.
    2.  **Metacognitivo/Estratégico:** O Conselho ajusta a estratégia de estudo.
    3.  **Afetivo/Emocional:** O Amigo mantém a motivação.

### 2.2 Bayesian Knowledge Tracing (BKT)

Esta seção apresenta a simulação do rastreamento de conhecimento para o conceito K01, utilizando uma fórmula de atualização de domínio inspirada no BKT.

A fórmula de atualização aplicada é:

$$
p_{t}=p_{t-1}+\alpha\cdot\beta\cdot(r_{t}-p_{t-1})
$$

Onde $\alpha$ (taxa de aprendizado) é fixado em 0.30.

**Tabela 2: Rastreamento de Domínio do Conceito K01: Simulação BKT Simplificada**

| Tentativa (t) | Tipo de Atividade | Resposta (r) | Peso ($\beta$) | Domínio Anterior ($p_{t-1}$) | Domínio Atual ($p_{t}$) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0 | Conhecimento prévio | - | - | - | 0.50 |
| 1 | Vídeo | 1 | 0.3 | 0.50 | 0.55 |
| 2 | Quiz (Fácil) | 0 | 0.6 | 0.55 | 0.45 |
| 3 | Leitura | 1 | 0.2 | 0.45 | 0.48 |
| 4 | Quiz (Médio) | 1 | 0.8 | 0.48 | 0.60 |
| 5 | Exercício de Código | 1 | 1.0 | 0.60 | 0.72 |

**Análise dos Resultados:**
O resultado final de 0.72 (72%) para o domínio do conceito K01 indica que o aluno está progredindo, mas erros em questões básicas tiveram impacto notável.

---

## 3. Conceitos-chaves (gerado por IA)

### 3.1 MAIC

1.  **Mudança de Paradigma:** Transição do modelo "Um Vídeo para N Alunos" para "N Agentes para 1 Aluno".
2.  **Arquitetura de Sistema Duplo:** Slide2Lecture (offline) e SimClass (online).
3.  **Geração Automatizada de Conteúdo:** Pipeline Slide2Lecture usa LLMs para criar roteiros de ensino a partir de slides brutos.
4.  **Eficiência de Custo e Tempo:** Reduz semanas de produção para minutos.
5.  **Simulação de Sala de Aula Multiagente:** Simula Professor, Assistente e Colegas de Classe.
6.  **Controle Dinâmico de Sessão:** "Controlador de Sessão" gerencia o fluxo em tempo real.
7.  **Ações de Ensino Heterogêneas:** Formaliza o ensino em ações discretas (ReadScript, ShowFile, etc.).
8.  **Experiência de Aprendizagem Interativa:** Permite interrupções, perguntas e discussões.
9.  **Engajamento Comportamental:** Altos níveis de engajamento proativo.
10. **Validação no Mundo Real:** Avaliado em cursos universitários reais.

### 3.2 SINKT

1.  **Capacidade Indutiva:** Capaz de prever desempenho em novas perguntas/conceitos não vistos.
2.  **Integração de LLMs:** Usa GPT-4 para relações e PLMs para semântica.
3.  **Codificador de Informação Textual (TIEnc):** Usa PLMs em vez de IDs aleatórios.
4.  **Grafo com Consciência Estrutural:** Grafo heterogêneo com arestas C-Q, Q-C e C-C.
5.  **Codificador de Informação Estrutural (SIEnc):** Emprega Redes de Atenção Gráfica (GAT).
6.  **Conhecimento Saltitante (Jumping Knowledge):** Preserva riqueza semântica original.
7.  **Solução para Cold-Start:** Aborda eficazmente a falta de dados de interação inicial.
8.  **Robustez à Escassez de Dados:** Alto desempenho mesmo com dados limitados.
9.  **Modelagem do Estado do Aluno:** Usa GRU para rastrear evolução temporal.
10. **Desempenho de Ponta (State-of-the-Art):** Supera modelos transdutivos existentes (DKT, AKT, GKT).