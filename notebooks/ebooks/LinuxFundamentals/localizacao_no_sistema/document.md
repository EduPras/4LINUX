![](0.png)

## 25

## Localização no sistema

## Comando find

O comando find procura por arquivos/diretórios no disco. Ele pode procurar arquivos pela sua data de modificação, tamanho, etc. O find , ao contrário de outros programas, usa opções longas por meio de um -.

Sintaxe do comando find :

```
find [diretório] [opções/expressão]
```

- -name [expressão] : Procura pela [expressão] definida nos nomes de arquivos e diretórios processados.
- -maxdepth[num] : Limita a recursividade de busca na árvore de diretórios. Por exemplo, limitando a 1, a busca será feita apenas no diretório especificado e não irá incluir nenhum subdiretório.

```
find /etc -name *.conf
```

```
find /etc -maxdepth 1 -name *.conf
```

- -amin[num] : Procura por arquivos que foram acessados [num] minutos atrás. Caso seja antecedido por -', procura por arquivos que foram acessados entre [num] minutos atrás e o momento atual.

find ~ -amin -5

- -atime[num] : Procura por arquivos que foram acessados [num] dias atrás. Caso seja antecedido por -, procura por arquivos que foram acessados entre [num] dias atrás e a data atual.

find ~ -atime -10

- -uid[num] : Procura por arquivos que pertençam ao usuário com o uid 1000 [num].

find / -uid 1000

- -user[nome] : Procura por arquivos que pertençam ao usuário aluno [nome].

find / -user aluno

## · -perm[modo] :

Procura por arquivos que possuem os modos de permissão [modo]. Os [modo] de permissão podem ser numérico (octal) ou literal.

find / -perm 644

- -size[num] : Procura por arquivos que tenham o tamanho [num]. O tamanho é especificado em bytes. Você pode usar os sufixos k, M ou G para representar o tamanho em Quilobytes, Megabytes ou Gigabytes, respectivamente. O valor de [num] Pode ser antecedido de + ou -para especificar um arquivo maior ou menor que [num].

find / -size +1M

- -type[tipo] : Procura por arquivos do [tipo] especificado. Os seguintes tipos são aceitos:

```
b - bloco ; c - caractere ; d - diretório ; p - pipe ; f - arquivo regular ; l - link simbólico ; s - socket .
```

```
find /dev -type b
```

## Mais alguns exemplos que podem te ajudar no seu dia-a-dia..

O comando abaixo busca todos os arquivos ou diretórios que possuem permissão 777:

```
find / -perm 777
```

O comando abaixo busca no diretório /root apenas arquivos com permissão 777:

```
find /root -type f -perm 777
```

O comando abaixo busca no diretório / apenas arquivos com tamanho maior do que 10M:

```
find / -size +10M
```

O comando abaixo busca no diretório / arquivos com permissão 600 e executa o comando ls no formato longo para obter mais detalhes sobre os arquivos:

```
find / -perm 600 -exec ls -l {} \;
```

O comando abaixo busca no diretório / arquivos com permissão 600 e executa o comando ls no formato longo para obter mais detalhes sobre os arquivos:

```
find / -perm 600 -print0 | xargs -0 ls -l
```

O comando abaixo buscará no diretório raiz apenas arquivos vazios:

```
find / -type f -empty
```

O comando abaixo buscará no diretório raiz apenas diretórios vazios:

```
find / -type d -empty
```

O comando abaixo buscará no diretório raiz todos os arquivo modificados nos 50 dias anteriores:

```
find / -mtime 50
```

O comando abaixo buscará no diretório raiz todos arquivos que foram modificados entre 50 e 100 dias atrás.

```
find / -mtime +50 -mtime -100
```

O comando abaixo buscará no diretório raiz todos arquivos que foram acessados nos últimos 50 dias:

```
find / -atime 50
```

O comando abaixo buscará no diretório corrente apenas arquivos que foram acessados no último dia (nas últimas 24 horas) e executará o comando ls no formato longo (detalhado) na possível lista de arquivos que será gerada:

```
find . -type f -atime -1 -exec ls -l {} \;
```

O comando abaixo buscará no diretório pessoal do usuário que estiver executando todos os arquivos modificados nos últimos 60 minutos (1 hora):

```
find ~ -cmin -60
```

O comando abaixo buscará no diretório raiz todos os arquivos com extensão .txt e retirará a permissão de execução de todos eles:

```
find / -name "*.txt" -exec chmod -x {} ";"
```

O comando abaixo buscará arquivos que tem todas as permissões citadas em -perm , neste caso 4000:

```
find / -perm -4000
```

O comando abaixo buscará um arquivo com o nome passwd até dois níveis (subdiretórios) abaixo da raiz:

```
find / -maxdepth 2 -name passwd
```

O comando abaixo buscará no diretório corrente (ponto ( . ) após o find ) diretórios vazios e os

removerá:

```
find . -type d -empty -exec rmdir {} \;
```

## Comando xargs

Outra forma de procurar por arquivos e/ou diretórios e executar um comando é através do comando xargs que obtém como a entrada a saída ok do comando antes do pipe e envia como stdin do próximo comando, no caso o ls -ld :

```
find / etc -type d | xargs ls -ld
```

Vamos agora listar diretórios utilizando o xargs :

```
ls / | xargs - n1 ls / | xargs - n2 ls / | xargs - n3
```

Outros testes com o xargs :

```
ls / > teste_xargs.txt cat teste_xargs.txt cat teste_xargs.txt | xargs -n 2 xargs -n 3 < teste_xargs.txt
```

Você percebeu que no primeiro comando ele listou o diretório, jogando na tela um nome de cada vez. O segundo comando fará o mesmo só que com dois nomes na mesma linha, e o terceiro com 3 nomes.

```
echo "linux:macos:freebsd:openbsd" > /tmp/teste.txt cat /tmp/teste.txt | xargs -d: -n 2 linux macos freebsd openbsd
```

## Comando locate

O comando locate é um comando rápido de busca de arquivos, porém não usa busca recursiva na sua árvore de diretórios. Ele utiliza uma base de dados que é criada pelo comando updatedb , para que a busca seja mais rápida. Por padrão, a atualização da base de dados é agendado no cron do sistema para ser executada diariamente.

Para utilizá-lo, primeiro é necessário criar a sua base de dados usando a seguinte sintaxe:

updatedb

Quando esse comando é executado pela primeira vez costuma demorar um pouco. Isso deve-se a primeira varredura do disco para a criação da primeira base de dados.

Para o comando locate , usamos a seguinte sintaxe:

locate howto

A saída do comando será algo parecido com:

```
/usr/share/doc/hashcat/extra/tab_completion/howto.txt /usr/share/doc/smartmontools/badblockhowto.html /usr/share/doc/util-linux/howto-build-sys.txt /usr/share/doc/util-linux/howto-compilation.txt /usr/share/doc/util-linux/howto-contribute.txt.gz
```