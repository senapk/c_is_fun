# Trabalhando com Strings em C: `sprintf` e `sscanf`

<!-- toc -->
- [Introdução](#introdução)
- [Parte 1: Escrevendo em Strings com `sprintf`](#parte-1-escrevendo-em-strings-com-sprintf)
  - [O que é `sprintf`?](#o-que-é-sprintf)
  - [Sintaxe](#sintaxe)
  - [Exemplo de Uso](#exemplo-de-uso)
  - [Detalhes Importantes](#detalhes-importantes)
- [Parte 2: Lendo Strings com `sscanf`](#parte-2-lendo-strings-com-sscanf)
  - [O que é `sscanf`?](#o-que-é-sscanf)
  - [Sintaxe](#sintaxe)
  - [Exemplo de Uso](#exemplo-de-uso)
  - [Detalhes Importantes](#detalhes-importantes)
- [Código Completo](#código-completo)
<!-- toc -->

## Introdução

Manipular strings é uma tarefa comum em programação, especialmente em C, onde as funções `sprintf` e `sscanf` desempenham papéis cruciais. A primeira parte deste guia abordará a função `sprintf`, que é utilizada para escrever dados em uma string. A segunda parte se concentrará na função `sscanf`, usada para ler dados de uma string.

## Parte 1: Escrevendo em Strings com `sprintf`

### O que é `sprintf`?

A função `sprintf` é usada para formatar e armazenar uma série de caracteres em uma string. Sua funcionalidade é similar à função `printf`, com a diferença de que `sprintf` escreve a saída formatada em um buffer de string, em vez de exibi-la no console.

### Sintaxe

```c
int sprintf(char *str, const char *format, ...);
```

- **str**: Ponteiro para o buffer onde a string formatada será armazenada.
- **format**: String de formato que especifica como os argumentos subsequentes devem ser convertidos e armazenados.
- **...**: Lista de argumentos a serem formatados.

### Exemplo de Uso

```c
#include <stdio.h>

int main() {
    char buffer[100];
    int idade = 25;
    double altura = 1.75;

    sprintf(buffer, "Idade: %d, Altura: %.2f", idade, altura);
    printf("%s\n", buffer);

    return 0;
}
```

### Detalhes Importantes

- **Buffer Overflow**: Sempre certifique-se de que o buffer é grande o suficiente para armazenar a string formatada para evitar overflow.
- **Format Specifiers**: Use especificadores de formato corretamente (`%d`, `%f`, `%s`, etc.) para garantir que os dados sejam armazenados corretamente.

## Parte 2: Lendo Strings com `sscanf`

### O que é `sscanf`?

A função `sscanf` é utilizada para ler dados de uma string formatada. Funciona de maneira similar à função `scanf`, mas lê os dados de uma string em vez de a partir da entrada padrão.

### Sintaxe

```c
int sscanf(const char *str, const char *format, ...);
```

- **str**: String de entrada da qual os dados serão lidos.
- **format**: String de formato que especifica como os dados devem ser lidos e armazenados.
- **...**: Ponteiros para variáveis onde os dados lidos serão armazenados.

### Exemplo de Uso

```c
#include <stdio.h>

int main() {
    char buffer[] = "Idade: 25, Altura: 1.75";
    int idade;
    double altura;

    sscanf(buffer, "Idade: %d, Altura: %lf", &idade, &altura);
    printf("Idade: %d, Altura: %.2f\n", idade, altura);

    return 0;
}
```

### Detalhes Importantes

- **Correspondência Exata**: A string de formato deve corresponder exatamente à estrutura da string de entrada.
- **Tipos de Dados**: Garanta que os tipos de dados dos argumentos correspondem aos especificadores de formato.

## Código Completo

```c
#include <stdio.h>

int main() {
    // Parte 1: Usando sprintf
    char buffer[100];
    int idade = 25;
    double altura = 1.75;

    sprintf(buffer, "Idade: %d, Altura: %.2f", idade, altura);
    printf("%s\n", buffer);

    // Parte 2: Usando sscanf
    char input[] = "Idade: 25, Altura: 1.75";
    int idade_lida;
    double altura_lida;

    sscanf(input, "Idade: %d, Altura: %lf", &idade_lida, &altura_lida);
    printf("Idade: %d, Altura: %.2f\n", idade_lida, altura_lida);

    return 0;
}
```