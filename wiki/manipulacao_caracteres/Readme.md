# Manipulação de Caracteres em C

<!-- toc -->
- [Introdução](#introdução)
- [Convertendo Caractere para Inteiro e Vice-Versa](#convertendo-caractere-para-inteiro-e-vice-versa)
- [Funções da Biblioteca `<ctype.h>`](#funções-da-biblioteca-ctypeh)
  - [isalpha() - Verifica se é uma Letra](#isalpha---verifica-se-é-uma-letra)
  - [isdigit() - Verifica se é um Dígito](#isdigit---verifica-se-é-um-dígito)
  - [isalnum() - Verifica se é uma Letra ou um Dígito](#isalnum---verifica-se-é-uma-letra-ou-um-dígito)
  - [islower() - Verifica se é uma Letra Minúscula](#islower---verifica-se-é-uma-letra-minúscula)
  - [isupper() - Verifica se é uma Letra Maiúscula](#isupper---verifica-se-é-uma-letra-maiúscula)
  - [tolower() - Converte para Minúscula](#tolower---converte-para-minúscula)
  - [toupper() - Converte para Maiúscula](#toupper---converte-para-maiúscula)
<!-- toc -->

## Introdução

Na programação, lidar com caracteres é uma parte fundamental, seja para processar texto, verificar padrões ou converter entre letras maiúsculas e minúsculas. Nesta aula, exploraremos várias técnicas e funções para manipulação de caracteres em C.

## Convertendo Caractere para Inteiro e Vice-Versa

Em C, os caracteres são representados por valores numéricos de acordo com a tabela ASCII. Isso permite que você converta facilmente um caractere em um valor inteiro (código ASCII) e vice-versa. A conversão é feita usando a conversão de tipo (casting).

Por exemplo, para converter o caractere 'A' em um inteiro, você pode fazer o seguinte:

```c
#include <stdio.h>

int main() {
    char letra = 'A';
    int codigo_ascii = (int) letra;
    printf("%d\n", codigo_ascii); // 65
    return 0;
}
```

O contrário também é possível, ou seja, converter um inteiro em um caractere. Para isso, basta fazer o casting para o tipo `char`:

```c
#include <stdio.h>

int main() {
    int codigo_ascii = 65;
    char letra = (char) codigo_ascii;
    printf("%c\n", letra); // A
    return 0;
}
```

> **Nota:** Realizamos um casting explícito, tanto de `char` para `int` quanto de `int` para `char`. Uma conversão implícita aconteceria se não tivéssemos especificado o tipo do casting. Por exemplo:

```c
char letra = 'A';
int codigo_ascii = letra; // conversão implícita de char para int
char letra2 = codigo_ascii; // conversão implícita de int para char
```

No entanto, é uma boa prática sempre realizar um casting explícito, pois isso deixa o código mais legível e evita erros.

## Funções da Biblioteca `<ctype.h>`

A biblioteca `<ctype.h>` fornece um conjunto de funções que ajudam a verificar e manipular caracteres. Para usá-la, basta incluir a biblioteca no início do seu programa com a diretiva `#include`:

```c
#include <ctype.h>
```

### isalpha() - Verifica se é uma Letra

A função `isalpha()` verifica se um caractere é uma letra (maiúscula ou minúscula). Ou seja, se o caractere está entre 'A' e 'Z' ou entre 'a' e 'z'.

- **Parâmetros**: um caractere
- **Retorno**: `1` (verdadeiro) caso seja uma letra e `0` (falso) caso contrário

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char letra = 'A';
    if (isalpha(letra)) {
        printf("É uma letra\n");
    } else {
        printf("Não é uma letra\n");
    }
    return 0;
}
```

### isdigit() - Verifica se é um Dígito

A função `isdigit()` verifica se um caractere é um dígito. Ou seja, se o caractere está entre '0' e '9'.

- **Parâmetros**: um caractere
- **Retorno**: `1` (verdadeiro) caso seja um dígito e `0` (falso) caso contrário

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char digito = '5';
    if (isdigit(digito)) {
        printf("É um dígito\n");
    } else {
        printf("Não é um dígito\n");
    }
    return 0;
}
```

### isalnum() - Verifica se é uma Letra ou um Dígito

A função `isalnum()` verifica se um caractere é uma letra ou um dígito. Ou seja, se o caractere está entre 'A' e 'Z', entre 'a' e 'z' ou entre '0' e '9'.

- **Parâmetros**: um caractere
- **Retorno**: `1` (verdadeiro) caso seja uma letra ou um dígito e `0` (falso) caso contrário

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char caractere1 = '5';
    char caractere2 = 'A';
    if (isalnum(caractere1) && isalnum(caractere2)) {
        printf("Ambos são dígitos ou letras\n");
    } else {
        printf("Um ou ambos não são dígitos ou letras\n");
    }
    return 0;
}
```

> **Dica:** A função `isalnum()` é equivalente a usar as funções `isalpha()` e `isdigit()` em conjunto.

### islower() - Verifica se é uma Letra Minúscula

A função `islower()` verifica se um caractere é uma letra minúscula. Ou seja, se o caractere está entre 'a' e 'z'.

- **Parâmetros**: um caractere
- **Retorno**: `1` (verdadeiro) caso seja uma letra minúscula e `0` (falso) caso contrário

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char letra = 'a';
    if (islower(letra)) {
        printf("É uma letra minúscula\n");
    } else {
        printf("Não é uma letra minúscula\n");
    }
    return 0;
}
```

### isupper() - Verifica se é uma Letra Maiúscula

A função `isupper()` verifica se um caractere é uma letra maiúscula. Ou seja, se o caractere está entre 'A' e 'Z'.

- **Parâmetros**: um caractere
- **Retorno**: `1` (verdadeiro) caso seja uma letra maiúscula e `0` (falso) caso contrário

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char letra = 'A';
    if (isupper(letra)) {
        printf("É uma letra maiúscula\n");
    } else {
        printf("Não é uma letra maiúscula\n");
    }
    return 0;
}
```

### tolower() - Converte para Minúscula

A função `tolower()` converte um caractere para minúscula. Ou seja, se o caractere está entre 'A' e 'Z', ele será convertido para seu equivalente entre 'a' e 'z'. Se o caractere já for uma letra minúscula, ele não será alterado.

- **Parâmetros**: um caractere
- **Retorno**: um inteiro, o código ASCII do caractere convertido

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char letra = 'A';
    char letra_minuscula = (char) tolower(letra);
    printf("%c\n", letra_minuscula); // a
    return 0;
}
```

### toupper() - Converte para Maiúscula

A função `toupper()` converte um caractere para maiúscula. Ou seja, se o caractere está entre 'a' e 'z', ele será convertido para seu equivalente entre 'A' e 'Z'. Se o caractere já for uma letra maiúscula, ele não será alterado.

- **Parâmetros**: um caractere
- **Retorno**: um inteiro, o código ASCII do caractere convertido

```c
#include <stdio.h>
#include <ctype.h>

int main() {
    char letra = 'a';
    char letra_maiuscula = (char) toupper(letra);
    printf("%c\n", letra_maiuscula); // A
    return 0;
}
```

Este guia fornece uma visão geral da manipulação de caracteres em C, utilizando as funções da biblioteca `<ctype.h>`. Essas ferramentas são essenciais para processar e validar entradas de texto de forma eficaz e robusta.