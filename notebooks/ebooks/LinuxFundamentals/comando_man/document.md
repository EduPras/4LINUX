![](0.png)

## 19

## Comando man

O comando man sem dúvidas é o comando mais usado para obtenção de documentação no Linux, ele é o responsável por trazer os manuais mais completos sobre determinado comando, arquivo de configuração, bibliotecas, entre outros nos quais estamos trabalhando.

Os manuais do sistema são divididos nos seguintes níveis:

- man 1 -&gt; Programas e executáveis disponíveis ao usuário;
- man 2 -&gt; Rotinas de sistema Unix e C;
- man 3 -&gt; Rotinas de bibliotecas da linguagem C;
- man 4 -&gt; Arquivos especiais (dispositivos em /dev );
- man 5 -&gt; Arquivos de configuração e convenções;
- man 6 -&gt; Games;
- man 7 -&gt; Diversos (macros textuais, por exemplo, regex );
- man 8 -&gt; Comandos administrativos;
- man 9 -&gt; Rotinas internas do kernel.

É comum o exame da LPI cobrar mais dos níveis 1, 5 e 8 dos manuais! Então lembre se de estudar binários, arquivos de configuração e comandos administrativos.

Sintaxe do comando man :

```
man [ comando ]
```

ou

```
man [ seção ] [ comando ]
```

Uma curiosidade: as informações sobre as seções do comando man podem ser encontradas em seu próprio manual, digitando o comando man man .

Se for necessário visualizar o manual do comando passwd , podemos fazer da seguinte forma:

```
man passwd
```

Para navegar pelo manual, o comando man abre um arquivo que está compactado na pasta /usr /share/man/man1 para o passwd . Outros níveis de manuais, dependem do comando ou arquivo. O passwd é conhecido no sistema GNU/Linux como um comando que adiciona ou modifica a senha do usuário e, também, como o arquivo de usuários do sistema /etc/passwd) .

Veremos agora o manual do arquivo de usuários passwd :

```
man 5 passwd
```

Podemos consultar quais manuais estão disponíveis dentro do próprio diretório do man :

```
ls /usr/share/man/
```

Dentro desse diretório é possível ver todas as divisões dos manuais: os níveis, os idiomas e mais. Todos os níveis de manuais possuem sua determinada introdução que pode ser vista com o comando:

```
man <nivel> intro
```

Podemos ver que para visualizar o manual do arquivo de usuário passwd precisamos informar em qual nível de manual ele se encontra, pois já existe um passwd no nível 1, que é o comando, então ele aparece primeiro quando digitamos man passwd sem indicar o nível.

Esse manual do arquivo passwd está compactado na pasta /usr/share/man/man5 .