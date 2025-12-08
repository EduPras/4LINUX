![](0.png)

## 12

## Caminhos de Diretorios

Como vimos, há várias boas interfaces gráficas de usuário, ou GUIs, disponíveis para tornar os usuários mais produtivos.

Mas de vez em quando você pode ter que fazer alguma coisa a partir da linha de comando do Linux, e é importante saber onde você está na estrutura de arquivos do Linux.

Linux são hierárquicos, ou seja, há um diretório de nível superior chamado Raiz , que é identificado como apenas uma barra / . A Raiz tem sub-diretórios organizados sob ele, como /home , /bin e /usr .

Os chamados 'caminhos' de diretório, são locais no sistema onde são armazenadas localizações físicas de arquivos, pastas, scripts e demais recursos do sistema e consistem em caminhos absolutos e caminhos relativos.

Caminho absoluto é o caminho completo de um arquivo ou subdiretório desde a raiz. Por exemplo: /proc/cpuinfo .

Onde, cpuinfo é um arquivo que está abaixo do diretório proc e o diretório proc está abaixo do diretório / (raiz).

É importante ressaltar que o caminho absoluto começará sempre com / . Desta forma, ao acessar um arquivo ou um diretório por meio do caminho absoluto não importa em qual diretório atual (corrente) você esteja.

Já o caminho relativo é usado quando não é indicado o diretório raiz para acessar um subdiretório ou um arquivo qualquer. Para que o caminho relativo funcione você precisa saber em qual diretório está localizado atualmente no sistema e ter uma boa noção de onde ficam localizados os principais diretórios e arquivos. Abaixo seguem alguns atalhos para acessar determinados diretórios.

Caminhos de diretórios:

```
1. . - diretório corrente 2. .. - diretório pai 3. / - diretório raiz 4. \-- diretório anterior
```

O comando pwd ( print name of current/working directory ) significa: imprima o nome do diretório corrente no qual estou trabalhando agora, e é usado para saber em qual diretório você está no momento.

```
cd /home pwd cd /tmp pwd cd ~ pwd /bin/ls
```

As linhas 1, 3 e 7 dos comandos acima são absolutas. Observe que todos estes caminhos começam com barra ( / ). O que permite você executar o comando ls sem indicar o caminho absoluto é a existência da variável de ambiente $PATH , que armazena os diretórios nos quais o sistema deve buscar os executáveis. O diretório /bin está presente na variável de ambiente $PATH de todo usuário comum.

Para visualizar o conteúdo da variável de ambiente $PATH do usuário corrente execute o comando:

```
echo $PATH /usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
```

Observe que cada diretório presente na variável de ambiente $PATH é separado por dois pontos ( : ). Por enquanto, ainda não é nosso objetivo entrar em detalhes sobre as variáveis de ambiente do sistema.

## Caminho relativo:

```
pwd /tmp cd .. pwd / cd pwd /tmp
```

As linhas 3 e 6 dos comandos acima usam caminho relativo. O resultado destes comandos dependem de qual diretório você está no momento, por isso o nome caminho relativo.

## Caminho relativo:

```
cd /bin ./ls echo "Certificação LPIC-1" echo $PATH /usr/share/sbin:/usr/local/bin:/usr/sbin:/usr/bin: /sbin:/bin
```

## Caminho relativo:

```
cd /usr/share/doc pwd /usr/share/doc cd ../../ pwd /usr
```

A linha 4 dos comandos acima usa um caminho relativo e sobe dois níveis na árvore de diretórios.

## Acessando os diretórios

Vamos aprender agora alguns comandos essenciais para a nossa movimentação dentro do sistema.

O comando cd é utilizado para mudar o diretório atual de onde o usuário está. Ir para o diretório home do usuário logado:

cd cd ~

Ir para o início da árvore de diretórios, ou seja, o diretório / :

cd /

Ir para um diretório específico:

cd /etc

Sobe um nível na árvore de diretórios:

cd ..

Retorna ao diretório anterior:

cd -

Entra em um diretório específico:

cd /usr/share/doc

Sobe 2 níveis da árvore de diretórios:

cd ../../

## Comando ls

O comando ls é utilizado para listar o conteúdo dos diretórios. Se não for especificado nenhum diretório, ele irá mostrar o conteúdo daquele onde estamos nomomento. Lista o conteúdo do

diretório atual:

```
ls
```

Para listar o conteúdo do diretório corrente com saída colorida faça:

```
ls --color
```

Para listar todo o conteúdo (inclusive os arquivos ocultados) do diretório corrente:

```
ls -a
```

O arquivos ocultados no Linux começam com um . (ponto).

O asterisco é um coringa que representa nenhum ou mais caracteres.

```
ls /dev/sd* /dev/sda /dev/sda2 /dev/sda4 /dev/sdb /dev/sdb2 /dev/sda1 /dev/sda3 /dev/sda5 /dev/sdb1
```

```
ls /etc/host* /etc/host.conf /etc/hostname /etc/hosts /etc/hosts.allow /etc/hosts.deny
```

O ponto de interrogação representa um único caractere ao contrário do asterisco. Observe a saída do comando abaixo. Temos dois pontos de interrogação que serão substituídos por dois caracteres:

```
ls /dev/s?? /dev/sda /dev/sdb /dev/sg0 /dev/sg1 /dev/sg2 /dev/sr0 /dev/shm: pulse-shm-1570592226 pulse-shm-2671603769 pulse-shm-525798260 pulse-shm-1851567380 pulse-shm-3911461625 pulse-shm-665496239 pulse-shm-252084306 pulse-shm-4228683900 pulse-shm-882637142 /dev/snd: by-path controlC0 hwC0D2 pcmC0D0c pcmC0D0p pcmC0D2p seq timer
```

O comando abaixo mostrará todos arquivos que começam com sd e terminam com a , b ou c :

```
ls /dev/sd[abc] /dev/sda /dev/sdb
```

O comando abaixo mostrará todos os arquivos que começam com sda , mas que não é seguido por 0 ou 1:

```
ls /dev/sda[!01] /dev/sda2 /dev/sda3 /dev/sda4 /dev/sda5
```

## Atalhos de teclado utilizados na linha de comando

Ao digitar comandos no shell do sistema GNU/Linux, podemos fazer uso de atalhos de teclado para agilizar tarefas, tais como apagar e copiar caracteres, mover o cursor para o local desejado, abrir uma nova linha de comando, entre outras descritas a seguir:

- HOME ou CTRL + A : leva o cursor para o início da linha de comandos.
- END ou CTRL + E : leva o cursor para o fim da linha de comandos.
- BACKSPACE : apaga o caractere à esquerda do cursor.
- CTRL + U : apaga tudo o que estiver à esquerda do cursor, porém permite colar o conteúdo apagado com o atalho CTRL + Y.
- DELETE : apaga o caractere à direita do cursor.
- CTRL + K : apaga tudo o que estiver à direita do cursor, porém permite colar o conteúdo apagado com o atalho CTRL + Y.
- CTRL + L : funciona como o comando clear , limpa a tela e joga o cursor para a primeira linha. Com o atalho SHIFT + PAGE UP , ainda é possível visualizar o conteúdo.
- CTRL + C : abre uma nova linha de comando na posição do cursor.
- CTRL + R : busca algum caractere específico no último comando digitado.
- CTRL + D : assim como o comando exit , sai do shell.