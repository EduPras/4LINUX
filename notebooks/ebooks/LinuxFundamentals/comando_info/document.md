![](0.png)

## 20

## Comando info

As info pages são como as páginas de manuais, porém são utilizadas com navegação entre as páginas. Elas são acessadas pelo comando info . Este é útil quando já sabemos o nome do comando e só queremos saber qual sua respectiva função.

A navegação nas info pages é feita através de nomes marcados com um **(*) (hipertextos) que, ao pressionarmos Enter , nos leva até a seção correspondente, e Backspace** volta à página anterior. Algo parecido com a navegação na Internet.

Podemos também navegar pelas páginas com as teclas: * n (next/próximo); * p (previous/anterior); * u (up/sobe um nível) .

Para sair do comando info , basta pressionar a tecla q .

Se for necessário exibir a lista de todos os manuais de comandos/programas disponíveis, execute o comando abaixo sem nenhum argumento. Assim:

info

Para exibir as informações somente de um determinado comando, usaremos a seguinte sintaxe:

info [comando]

Visualizar informações do comando vim:

info vim

## Alternativas para consulta

Para obter uma melhor visualização, duas ferramentas de documentação foram desenvolvidas:

- yelp -&gt; Ferramenta gráfica para visualização de manuais de aplicativos gráficos do GNOME; (fornecido pelo pacote yelp);
- xman -&gt; 'Front-end' para o comando man , que facilita a consulta das man pages ; (fornecido pelo pacote x11-apps ).