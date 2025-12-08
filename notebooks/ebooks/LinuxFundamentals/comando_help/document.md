![](0.png)

## 16

## Comando help

O comando help provê ajuda para comandos internos do interpretador de comandos, ou seja, o comando help fornece ajuda rápida. Ele é muito útil para saber quais opções podem ser usadas com os comandos internos do interpretador de comandos (shell). Para visualizar uma ajuda rápida para todos os comandos internos do sistema, podemos fazer da seguinte forma:

help

Caso desejemos visualizar a ajuda rápida para somente um comando interno, usamos esta outra sintaxe:

help [comando]

O comando help somente mostra a ajuda para comandos internos.

help type

O comando type mostra se cada nome de comando é um comando do UNIX, um comando interno, um alias, uma palavra-chave do shell ou uma função de shell definida.

Verifique o tipo do comando help que conheceremos a seguir:

```
help help
```

Para comandos externos, o help aparece como parâmetro. Por exemplo:

```
[comando] --help
```

Desse modo, caso desejemos visualizar uma ajuda rápida sobre um comando externo, devemos fazer da seguinte forma:

```
ls --help
```

O parâmetro --help pode ser utilizado em qualquer comando para ter uma consulta rápida dos parâmetros que ele pode nos oferecer. É importante entender que --help é na verdade um parâmetro individual de cada comando, logo se um comando não tiver esse parâmetro existem outros meios para se obter ajuda. Não se esqueça de estudar as diferenças entre comandos internos e externos.