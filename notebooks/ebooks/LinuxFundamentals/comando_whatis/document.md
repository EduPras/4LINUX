![](0.png)

## 18

## Comando whatis

O comando whatis tem basicamente a mesma função do comando apropos , porém as buscas do comando whatis são mais específicas. O apropos busca as páginas de manuais e descrições de maneira mais genérica. Se digitarmos a palavra passwd ele nos trará tudo que tiver passwd , seja como nome ou parte do nome do manual ou na descrição. Já o whatis nos trará somente o manual com nome exato da palavra pesquisada.

A sintaxe utilizada no comando whatis é a seguinte:

whatis [comando]

Você sabe que tem um programa chamado vim , mas não sabe o que ele faz?

whatis vim

Uma forma equivalente ao whatis é usar o comando man juntamente com a opção -f :

man -f vim

85

18. Comando whatis

Para localizar as man pages , o comando apropos e whatis utilizam o mesmo banco de dados construído com o comando catman ou makewhatis (executado pelo administrador do sistema, root ).

Para construir o banco de dados do comando apropos e whatis devemos executar o comando abaixo:

## Debian:

catman

## CentOS:

makewhatis -v