![](0.png)

## 21

## Comando whereis

O comando whereis é utilizado para mostrar a localização do binário do comando, do arquivo de configuração (caso exista), e a localização das páginas de manuais do determinado comando ou arquivo.

Se compararmos o comando whereis com o comando find , eles parecerão semelhantes entre si, pois ambos podem ser usados para os mesmos fins, mas o comando whereis produz o resultado com mais precisão, consumindo menos tempo comparativamente.

- Exemplo 1: digamos que queremos encontrar a localização do comando apropos e, em seguida, precisamos executar o seguinte comando no terminal:

whereis apropos

- Exemplo 2: para encontrar a localização do comando lshw .

whereis lshw

## Opcoes:

- -b : esta opção é usada quando queremos apenas pesquisar binários.

Exemplo: para localizar o binário de um comando do Linux, digamos gunzip .

whereis -b gunzio

- -m : esta opção é usada quando queremos apenas pesquisar por seções manuais.

Exemplo: Para localizar a página de manual do comando falso.

whereis -m false

- -s : esta opção é usada quando queremos apenas pesquisar fontes.
- -u : esta opção pesquisa entradas incomuns. Um arquivo de origem ou um arquivo binário é considerado incomum se não tiver nenhuma existência no sistema de acordo com [-bmsu] descrito junto com -u . Assim, whereis -m -u * pede os arquivos no diretório atual que possuem entradas incomuns.

Exemplo : Para exibir os arquivos do diretório atual que não possuem arquivo de documentação.

```
whereis -m -u *
```

- -B : esta opção é usada para alterar ou limitar os locais onde o whereis procura por binários.

Exemplo : para localizar o binário de lesspipe no caminho, /bin .

whereis -B /bin -f lesspipe

- -M : esta opção é usada para alterar ou limitar os locais onde o whereis procura por seções manuais.

Exemplo : para verificar a página de manual de introdução que está apenas em um local específico, ou seja, /usr/share/man/man1 .

whereis -M /usr/share/man/man1 -f intro

- -S : esta opção é usada para alterar ou de outra forma limitar os locais onde whereis procura pelas fontes.

Exemplo : Para localizar todos os arquivos em /usr/bin que não estão documentados em /usr/man/man1 com fonte em /usr/src whereis -u -M /usr/share/man/man1 -S /usr/src -f *

- -f : esta opção simplesmente termina a última lista de diretórios e sinaliza o início dos nomes dos arquivos. Deve ser usado quando qualquer uma das opções -B , -M ou -S for usada.
- -V : exibe informações sobre a versão e sai.
- -h : exibe esta ajuda e sai.