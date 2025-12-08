![](0.png)

## 17

## Comando apropos

O comando apropos ajuda o usuário quando ele não se lembra do comando exato, mas conhece algumas palavras-chave relacionadas ao comando que definem seu uso ou funcionalidade. Ele pesquisa a página de manual do Linux com a ajuda da palavra-chave fornecida pelo usuário para encontrar o comando e suas funções.

## Sintaxe:

```
apropos [OPÇÃO ..] PALAVRA-CHAVE ...
```

Situacao 1: suponhamos que você não saiba como compactar um arquivo, então você poderia digitar o seguinte comando no terminal e ele mostrará todos os comandos relacionados e sua breve descrição ou funcionalidade.

```
apropos compress
```

Depois de executar o comando acima, você observará uma série de comandos listados no terminal que tratam não apenas de como compactar um arquivo, mas também de expandir um arquivo compactado, pesquisar um arquivo compactado, comparar um arquivo compactado etc.

Situacao 2: o comando apropos também suporta várias palavras-chave se fornecidas como um argumento, ou seja, também podemos fornecer mais de uma palavra-chave para uma busca melhor. Assim, se duas palavras-chave forem fornecidas, o comando apropos exibirá toda a lista do comando que contém a primeira palavra-chave em sua descrição de página de manual ou a segunda palavra-chave.

apropos email

```
Entrada 1 (com uma palavra-chave)
```

apropos email address

```
Entrada 2 (com várias palavras-chave)
```

## Opções:

- -d : esta opção é usada para emitir mensagens de depuração. Quando esta opção é usada, o terminal retorna diretórios man, caminho global, diretório do caminho, avisos, etc. de cada comando que está relacionado à palavra-chave de pesquisa.
- -v : esta opção é usada para imprimir mensagens de aviso detalhadas.
- -e , -exact : esta opção é usada para pesquisar cada palavra-chave para correspondência exata. Se nenhuma opção for usada, o comando apropos retorna a lista de todos os comandos cuja descrição na descrição da página do manual corresponde à palavra-chave ou que estão de alguma forma relacionados à palavra-chave fornecida no argumento. No entanto, quando a opção -e é usada, o apropos retorna apenas o comando cuja descrição corresponde exatamente à palavra-chave.
- -w , -wildcard : esta opção é usada quando a (s) palavra (s) -chave contém curingas. apropos irá pesquisar independentemente o nome da página e a descrição que corresponde à (s) palavra (s) -chave.
- -a , -and : esta opção é usada quando queremos que todas as palavras-chave correspondam. Ele não retorna nada se qualquer uma das palavras-chave fornecidas não tiver correspondência na página do manual ou na descrição. Na entrada abaixo, duas palavras-chave foram fornecidas e apenas dois comandos são exibidos no resultado, pois há apenas um comando que contém ambas as palavras-chave.
- -l , -long : por padrão, a saída é cortada para a largura do terminal. Esta opção é útil

quando não queremos que o resultado seja truncado.

- -C : esta opção é usada quando não queremos usar o padrão ( / manpath ), mas o arquivo de configuração do usuário.
- -L : define o local para esta pesquisa.
- -m , -systems : esta opção usa páginas de manual de outros sistemas. Esta opção é útil quando queremos pesquisar a descrição da página do manual de outro sistema operacional acessível.
- -M , -manpath : define o caminho de pesquisa das páginas de manual para PATH em vez do $MANPATH padrão .
- -s , -sections , -section : Esta opção é usada quando queremos pesquisar apenas seções particulares (separadas por dois pontos) que são fornecidas no argumento.
- -? , -Help : esta opção exibe a lista de ajuda.
- -V , -version : usado para imprimir a versão do programa.
- -r , -regex : esta opção interpreta cada palavra-chave como um regex (expressão regular). A palavra-chave será comparada independentemente com o nome e a descrição da página.

E por fim, uma forma equivalente ao apropos é usar o comando man juntamente com a opção -k man -k editor