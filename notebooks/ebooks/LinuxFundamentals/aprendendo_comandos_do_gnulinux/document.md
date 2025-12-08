![](0.png)

## 24

## Aprendendo Comandos do GNU/Linux

Comandos são instruções passadas ao computador para executar uma determinada tarefa. No mundo NIX (GNU/Linux,Unix) , o conceito de comandos é diferente do padrão MS-DOS . Um comando é qualquer arquivo executável, que pode ser ou não criado pelo usuário.

Uma das tantas vantagens do GNU/Linux é a variedade de comandos que ele oferece, afinal, para quem conhece comandos, a administração do sistema acaba se tornando um processo mais rápido.

O Shell é o responsável pela interação entre o usuário e o sistema operacional, interpretando os comandos.

É no Shell que os comandos são executados.

## Extraindo mais do comando ls

O comando ls possui muitos parâmetros, veremos aqui as opções mais utilizadas. A primeira delas é o -l que lista os arquivos ou diretórios de uma forma bem detalhada (quem criou, data de criação, tamanho, dono e grupo ao qual cada um pertence):

ls -l /

```
crw-r--r-1 root root 10, 235 Mar 3 11:54 autofs drwxr-xr-x 2 root root 140 Mar 3 11:54 block lrwxrwxrwx 1 root root 3 Mar 3 11:54 cdrom -> sr0 brw-rw---1 root disk 8, 0 Mar 3 11:54 sda -rw-r--r-1 root root 501 Aug 6 2019 updatedb.conf
```

Veja que a saída desse comando é bem detalhada. Falando sobre os campos, para o primeiro caractere temos algumas opções:

```
d --> Indica que se trata de um diretório. l --> Indica que se trata de um **link** ( como se fosse um atalho também vamos falar sobre ele depois). - --> Hífen, indica que se trata de um arquivo regular. c --> Indica que o arquivo é um dispositivo de caractere (sem buffer). b --> Indica que o arquivo é um dispositivo de bloco (com buffer). u --> "Sinônimo para o tipo c" indica que o arquivo é um dispositivo de caractere (sem buffer). s --> Indica que o arquivo é um socket. p -> Indica que o arquivo é um fifo, named pipe.
```

FIFO - Sigla para First In, First Out , que em inglês significa primeiro a entrar, primeiro a sair. São amplamente utilizados para implementar filas de espera. Os elementos vão sendo colocados no final da fila e retirados por ordem de chegada. Pipes | são um exemplo de implementação de FIFO.

Buffer - É uma região de memória temporária, usada para escrita e leitura de dados. Normalmente, os buffers são utilizados quando existe uma diferença entre a taxa em que os dados são recebidos e a taxa em que eles podem ser processados.

Socket - É um meio de comunicação por software entre um computador e outro. É uma combinação de um endereço IP, um protocolo e um número de porta do protocolo.

O campo rw-r-rlista as permissões, enquanto os campos root indicam quem é o usuário e grupo dono desse diretório que, no nosso caso, é o administrador do sistema, o usuário root . O número antes do dono indica o número de hard links , um assunto abordado apenas em cursos mais avançados.

O campo 501 indica o tamanho do arquivo, e o campo Mar 3 11:54 informa a data e hora em que o diretório foi criado. Finalmente, no último campo temos o nome do arquivo ou diretório listado, que, no nosso exemplo, é o updatedb.conf .

Com relação aos diretórios, é importante ressaltar que o tamanho mostrado não corresponde ao espaço ocupado pelo diretório e seus arquivos e subdiretórios. Esse espaço é aquele ocupado pela entrada no sistema de arquivos que corresponde ao diretório. A opção -a lista todos

arquivos, inclusive os ocultos:

```
ls -a / root .. aptitude . bashrc . profile
```

Veja que, da saída do comando anterior, alguns arquivos são iniciados por . (ponto) . Esses arquivos são ocultos. No Linux, arquivos e diretórios ocultos são iniciados por um . (ponto) . Listar arquivos de forma recursiva, ou seja, listar também os subdiretórios que estão dentro do diretório / :

```
ls -R /
```

Como listar os arquivos que terminam com a palavra .conf dentro do diretório /etc ?

```
ls /etc/*.conf
```

Como buscar no diretório raiz / todos os diretórios que terminem com a letra n ?

ls -ld /*n

## Criar arquivo

Para criar um arquivo, podemos simplesmente abrir um editor de texto e salvá-lo. Mas existem outras formas. Uma das formas mais simples é usando o comando touch :

```
cd /tmp touch procedimentos.txt touch contas.pdf contas2.pdf contas3.pdf contas4.pdf
```

## Curingas

O significado da palavra curinga no dicionário é o seguinte: carta de baralho, que em certos jogos, muda de valor e colocação na sequência. No sistema GNU/Linux é bem parecida a utilização desse recurso. Os curingas são utilizados para especificar um ou mais arquivos ou

diretórios.

Eles podem substituir uma palavra completa ou somente uma letra, seja para listar, copiar, apagar, etc. São usados cinco tipos de curingas no GNU/Linux :

| Campo      | Significado                                                                                   |
|------------|-----------------------------------------------------------------------------------------------|
| *          | Utilizado para um nome completo ou restante de um arquivo/diretório;                          |
| ?          | Esse curinga pode substituir uma ou mais letras em determinada posição;                       |
| !          | exclui da operação;                                                                           |
| [padrão]   | É utilizado para referência a uma faixa de caracteres de um arquivo /diretório.               |
| [a-z][0-9] | Usado para trabalhar com caracteres de a at é z seguidos de um caractere de 0 at é 9.         |
| [a,z][1,0] | Usado para trabalhar com os caracteres a e z seguidos de um caractere 1 ou 0 naquela posição. |
| [a-z,1,0]  | Faz referência do intervalo de caracteres de a at é z ou 1 ou 0 naquela posição.              |
| [ˆ abc]    | Faz referência a qualquer caracter exceto a, b e c.                                           |
| {padrão}   | Expande e gera strings para pesquisa de padrões de um arquivo /diretório.                     |
| X{ab,01}   | Faz referência a sequência de caracteres Xab ou X01.                                          |
| X{a-e,10}  | Faz referência a sequência de caracteres Xa Xb Xc Xd Xe X10.                                  |

A barra invertida serve para escapar um caracter especial, ela é conhecida também como backslash .

A diferença do método de expansão dos demais, é que a existência do arquivo ou diretório é opcional para resultado final. Isto é útil para a criação de diretórios.

Os 5 tipos de curingas mais utilizados **( *, ?, [ ], , ! )** podem ser usados juntos.

Vejamos alguns exemplos:

Vamos criar 5 arquivos no diretório /srv utilizando o método de expansã

```
cd /srv touch curriculo{1,2,3}.txt curriculo{4,5}.new
```

Podemos listá-los assim:

```
ls curriculo1.txt curriculo2.txt curriculo3.txt curriculo4.new curriculo5.new
```

Vamos listar todos os arquivos do diretório /srv . Podemos usar o curinga '*' para visualizar todos os arquivos do diretório:

```
ls * curriculo1.txt curriculo2.txt curriculo3.txt curriculo4.new curriculo5.new
```

Para listarmos todos os arquivos do diretório /srv que tenham new no nome:

```
ls *new* curriculo4.new curriculo5.new
```

Listar todos os arquivos que começam com qualquer nome e terminam com .txt :

```
ls *.txt curriculo1.txt curriculo2.txt curriculo3.txt procedimentos.txt
```

Listar todos os arquivos que começam com o nome curriculo , tenham qualquer caractere no lugar do curinga, e terminem com .txt :

```
ls curriculo?.txt curriculo1.txt curriculo2.txt curriculo3.txt
```

Para listar todos os arquivos que começam com o nome curriculo , tenham qualquer caractere entre o número 1-3 no lugar da 4ł letra e terminem com .txt . Neste caso, se obtém uma filtragem mais exata, pois o curinga especifica qualquer caractere naquela posição e [ ] especifica um intervalo de números ou letras que será usado:

```
ls curriculo[1-3].txt curriculo1.txt curriculo2.txt curriculo3.txt
```

Para listar todos .txt exceto o curriculo2.txt :

```
ls curriculo[!2].txt curriculo1.txt curriculo3.txt
```

Para listar os arquivos curriculo4.new e curriculo5.new podemos usar os seguintes métodos:

```
ls *.new ls *new* ls curriculo?.new ls curriculo[4,5].* ls curriculo[4,5].new
```

Existem muitas outras sintaxes possíveis para obter o mesmo resultado. A mais indicada será sempre aquela que atender à necessidade com o menor esforço possível.

A criatividade nesse momento conta muito. No exemplo anterior, a última forma resulta na busca mais específica. O que pretendemos é mostrar como visualizar mais de um arquivo de uma só vez. O uso de curingas é muito útil e pode ser utilizado em todas as ações do sistema operacional referentes aos arquivos e diretórios: copiar ,apagar, mover e renomear.

## Criando diretórios

O comando mkdir é utilizado para criar um diretório no sistema. Um diretório é uma pasta onde você guarda seus arquivos. Exemplo:

Criar o diretório Suporte :

```
cd /srv mkdir Suporte
```

Criar o diretório Financeiro e o subdiretório Contas a Pagar :

```
mkdir -p Financeiro/Contas\ a\ Pagar
```

A opção -p permite a criação de diretórios de forma recursiva. Para que um subdiretório exista, o seu diretório diretamente superior tem que existir. Portanto a criação de uma estrutura como Rh/Processos/Cv's exigiria a execução de três comandos mkdir .

Algo como:

```
mkdir Rh mkdir Rh/Processos mkdir Rh/Processos/Cv'\s
```

A opção -p permite que toda essa estrutura seja criada em uma única linha. Assim:

```
mkdir -p Rh/Processos/Cv'\s
```

## Removendo arquivos/diretórios

O comando rm é utilizado para apagar arquivos, diretórios e susiretórios estejam eles vazios ou não.

Exemplos:

Remover os arquivos com extensão txt :

```
cd /srv ls rm curriculo?.txt ls
```

Remover o arquivo curriculo4.new pedindo confirmação:

```
rm -i curriculo4.news rm: remover arquivo comum vazio 'curriculo4.'new?
```

A opção -i força a confirmação para remover o arquivo curriculo4.new .

Remover o diretório Rh :

```
rm -r Rh
```

A opção -r ou -R indica recursividade, ou seja, a remoção deverá ser do diretório Rh e de todo o seu conteúdo.

```
Observação: Muita atenção ao usar o comando rm ! Uma vez que os arquivos e diretórios removidos não podem mais ser recuperados!
```

O comando rmdir é utilizado para remover diretórios vazios.

Exemplos:

Remover o diretório Suporte :

```
rmdir Suporte
```

## Copiar arquivos/diretórios

O comando cp serve para fazer cópias de arquivos e diretórios. Perceba que para lidar com diretórios a opção -r ou -R tem que ser usada:

```
cp arquivo-origem arquivo-destino cp arquivo-origem caminho/diretório-destino/ cp -R diretório-origem nome-destino cp -R diretório-origem caminho/diretório-destino/
```

Uma opção do comando cp muito útil em nosso dia-a-dia é a opção -p , que faz com que a cópia mantenha os meta-dados dos arquivos, ou seja, não modifica a data e hora de criação, seus donos e nem suas permissões. Utilizar como root :

```
su - aluno $ touch teste $ ls -l $ exit cd / home / aluno cp -p teste teste2 cp teste teste3 ls -l teste2 teste3
```

## Mover ou renomear arquivos/diretórios

O comando mv serve tanto para renomear um arquivo quanto para movê-lo:

```
mv arquivo caminho/diretório-destino/ mv arquivo novo-nome mv diretório novo-nome mv diretório caminho/diretório-destino/
```

A movimentação de um arquivo é uma ação de cópia seguida de uma remoção.

Renomeando arquivo:

mv teste teste4

Movendo arquivo:

```
mv teste4 /tmp
```

Renomeando diretório:

cd /srv mv Financeiro financeiro

Movendo diretório:

mv financeiro /srv/Rh/