![](0.png)

## 10

## Variáveis

Podemos definir variáveis como nomes que contêm algum valor e, ainda, como espaços de memória que armazenam valores. Sua função é o fornecimento de dados variáveis úteis e necessários a usuários e programas. Tais variáveis apresentam a seguinte forma:

NOME=VALOR

ou seja:

4LINUX=joatham

Esse tipo de variável que acabamos de definir é conhecida como escala e pode receber valores numéricos ou caracteres.

Para acessar o endereço de memória atribuído à variável 4LINUX , em shell , devemos utilizar o operador $ (cifrão) antes do nome da variável, ou seja, se desejarmos mostrar na tela o valor da variável 4LINUX devemos imprimir o conteúdo armazenado no endereço de memória $4LINUX :

echo $4LINUX

Interessante observar o comando echo , que por sua vez é usado para imprimir algo na tela ou direcionar para um arquivo. Isso é bastante útil para automação.

Nesse caso na linha de comando o echo é útil para inspecionar variáveis de ambiente, que são parâmetros guardados em memória e que definem o ambiente em uso.

Deixa eu te mostrar como se faz.

Para imprimir algo na tela:

echo algo

Vamos definir a variável comando com o valor igual a ls :

comando=ls

Para verificarmos o valor da variável podemos digitar:

echo $comando

Ou echo "$comando"

Para escrevermos na tela: $comando , digite:

echo ''$comando

E por fim para executarmos o valor da variável comando , digite:

echo ''$comando

Ou

echo $($comando)'

## Variáveis Locais e de Ambiente (globais)

Quando falamos em variáveis em shell temos que ter em mente a divisão entre variáveis locais e de ambiente (ou globais).

- Variáveis locais : são as variáveis disponíveis somente para o shell atual. Isso significa que sua visibilidade é restrita ao ambiente para o qual foram definidas, ou seja, elas não ficam disponíveis para o restante do sistema.
- Variáveis globais (de ambiente) : são as variáveis disponíveis tanto para o shell atual como para os subprocessos que as utilizam, de forma que sua visibilidade é aberta a outros ambientes além daqueles em que elas são definidas.

Vejamos algumas variáveis de ambiente na tabela abaixo:

| Variável   | Definição                                                                                                                       |
|------------|---------------------------------------------------------------------------------------------------------------------------------|
| HOME       | Responsável por identificar o diretório do usuário.                                                                             |
| HOSTTYPE   | Faz referência à plataforma que está sendo utilizada.                                                                           |
| SHELL      | Permite identificar o shell que está sendo utilizado.                                                                           |
| TERM       | Define o tipo de terminal que está sendo utilizado.                                                                             |
| USER       | Predefine o nome da conta como variável global.                                                                                 |
| PATH       | Determina quais diretórios devemos pesquisar e, ainda, qual sequência deverá ser seguida para encontrar um determinado comando. |
| PS1        | Representa as informações exibidas no prompt.                                                                                   |
| PS2        | Representa o prompt estendido.                                                                                                  |
| MAIL       | Esta variável informa como o correio eletrônico está definido.                                                                  |
| LOGNAME    | É um sinônimo da variável USER.                                                                                                 |
| OSTYPE     | Com a utilização desta variável, é possível definir o tipo de sistema operacional que está sendo utilizado.                     |

## Como definir variáveis

A única diferença técnica entre variáveis locais e de ambiente é a forma de sua definição.

Para definir uma variável local, basta atribuir um valor a um nome de variável.

Para definir uma variável de ambiente o procedimento adiciona o comando export antes da

definição.

Abaixo mostramos exemplos de definição de variável local e de ambiente:

```
LOCAL="sem export na frente" export GLOBAL="com export na frente"
```

Vejamos o seguinte exemplo:

```
LOCAL="Variável Local" echo $LOCAL Variável Local export GLOBAL="Variável Global" echo $GLOBAL Variável Global
```

No exemplo que acabamos de ver, foi criada uma variável local chamada LOCAL , a qual estará disponível apenas a esta seção. Para visualizar o retorno da variável, foi utilizado o comando echo . Em seguida, por meio do comando export , foi criada uma variável global, que estará disponível para todas as seções do sistema. Por fim, para verificar o retorno da variável global criada, o comando echo também foi utilizado.

Uma vez definidas as variáveis , podemos visualizá-las utilizando os comandos set e env ou printenv para variáveis locais e de ambiente, respectivamente. Com isso, se tivéssemos definido as variáveis LOCAL e GLOBAL e executássemos o comando set , veríamos as definições de ambas. Mas, se executássemos o comando env , veríamos apenas a definição da variável GLOBAL

```
magica="abracadabra" echo $magica set clear env
```

Abra um terminal filho:

```
bash
```

Não há nada na variável, pois ela não foi exportada:

```
echo $magica exit
```

Exporte a variável:

```
export magica set clear env
```

Abra um terminal filho:

bash

Agora existe um valor para a variável:

echo $magica

Utilizamos o comando unset para excluir variáveis. Sua sintaxe é a seguinte:

unset &lt;variavel&gt;

## Exclusão de variáveis

É importante lembrar que esse comando, quando usado para uma variável global, só tem efeito na sessão atual, de forma que a variável continuará acessível em outras sessões.

```
unset magica echo $magica
```

Para ficar permanente para todos e funcionar em qualquer terminal deve-se colocarem um dos arquivos:

```
/etc/profile /etc/environment
```

Para ficar permanente para o usuário e funcionar em qualquer terminal deve-se colocar em um dos arquivos:

```
~/.bashrc ~/.bash_profile ~/.bash_login4 ~/.profile
```

## Alterar o prompt de comando

Variáveis de ambiente (as globais) são muito s pois definem o comportamento da'shell' e de muitos outros programas'

Para que possamos alterar o prompt de comandos, devemos alterar os valores que estão armazenados dentro da variável PS1 .

Na tabela a seguir, serão descritos alguns valores que podem ser utilizados em conjunto com a variável PS1 :

| Valor       | Descrição                                                                                                                                                                            |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| h w W u t d | Faz referência ao nome do host. Caminho completo do diretório corrente. Refere-se ao diretório atual. Exibe o nome do usuário. Exibe a hora do sistema. Refere-se à data do sistema. |

- ** ∗ ∗ | Especificaovalor ' para usuários comuns, e o valor # para o usuário root' .

No exemplo adiante, alteramos a variável PS1 para que o prompt exiba o nome do usuário, o nome do host e a hora atual:

```
export PS1='[u@h-t]' [root@mycomputer-16:55:59]
```

Volte a configuração anterior:

| source /etc/profile   |
|-----------------------|