# Introdução aos Tipos de Dados em C++

<!-- toc -->
- [Tipos de Dados Fundamentais (ou Primitivos)](#tipos-de-dados-fundamentais-ou-primitivos)
- [Tipos Integrais](#tipos-integrais)
  - [`int`](#int)
  - [`char`](#char)
- [Tipos de Ponto Flutuante](#tipos-de-ponto-flutuante)
  - [`float`](#float)
  - [`double`](#double)
- [Tipo Booleano](#tipo-booleano)
  - [`bool`](#bool)
- [Curiosidade 1 - imprecisão](#curiosidade-1---imprecisão)
- [Curiosidade 2 - `sizeof`](#curiosidade-2---sizeof)
<!-- toc -->

Em C++, os tipos de dados são fundamentais para a definição dos valores que uma variável pode armazenar e como esses valores serão tratados pelo programa. C++ possui diversos tipos de dados, cada um com características específicas. Nesta aula, vamos explorar os principais tipos de dados disponíveis na linguagem e a inferência de tipos usando o `auto`.

## Tipos de Dados Fundamentais (ou Primitivos)

Os tipos de dados fundamentais em C++ podem ser agrupados em três categorias principais:

1. **Tipos Integrais**: Armazenam valores inteiros. Exemplos: `int`, `char`, etc.

2. **Tipos de Ponto Flutuante**: Armazenam valores com casas decimais. Exemplos: `float`, `double`.

3. **Tipo Booleano**: Armazena valores `true` ou `false`. Exemplo: `bool`.

## Tipos Integrais

### `int`

- É usado para armazenar valores inteiros, como 1, 100, -50, etc;
- É um dos tipos de dados mais comuns em C++;
- A maioria das plataformas representa o tipo int usando 32 bits (4 bytes) de memória;
- Permite representar valores entre aproximadamente -2 bilhões a +2 bilhões.

Exemplo de declaração e atribuição de uma variável do tipo int:

```c
int idade = 25;
```

### `char`

- É usado para armazenar caracteres individuais, como letras, dígitos ou símbolos;
- Cada caractere `char` ocupa 1 byte de memória e é representado usando aspas simples (' ').

Exemplo de declaração e atribuição de uma variável do tipo char:

```c
char letra = 'a';
```

## Tipos de Ponto Flutuante

### `float`

- É usado para armazenar valores de ponto flutuante de precisão simples;
- Geralmente, representa 32 bits (4 bytes) de memória.

Exemplo de declaração e atribuição de uma variável do tipo float:

```c
float altura = 1.75f; //o f depois do número indica que é um float
```

### `double`

- É usado para armazenar valores de ponto flutuante de dupla precisão;
- É mais preciso que o `float`, geralmente representado usando 64 bits (8 bytes) de memória;
- É adequado para aplicações que requerem alta precisão em cálculos com números decimais.

Exemplo de declaração e atribuição de uma variável do tipo double:

```c
double pi = 3.14159265359;
```

Double é o valor padrão de ponto flutuante e, na dúvida, use sempre double.

## Tipo Booleano

### `bool`

- É usado para armazenar valores lógicos, representando true (verdadeiro) ou false (falso);
- Ocupa 1 byte de memória
- É útil para expressar condições e estados em um programa.

Exemplo de declaração e atribuição de uma variável do tipo bool:

```c
#include <stdbool.h>

bool eh_par = true;
```

- No `C` é necessária a inclusão da biblioteca `<stdbool.h>` para o uso de variáveis tipo bool e das keywords `true` e `false`.
- Os tipos booleanos também têm suas representações inteiras: 0 ou 1, com 1 sendo verdadeiro.

## Curiosidade 1 - imprecisão

Só por curiosidade, o código abaixo mostra como o número 0.1 é representado em memória usando `float` e `double`.

```c
#include <stdio.h>

int main() {
    printf("float : %.20f\n", (float)0.1);  // 0.10000000149011611938
    printf("double: %.20f\n", (double)0.1); // 0.10000000000000000555
    return 0;
}
```

O resultado é:

```txt
float : 0.10000000149011611938
double: 0.10000000000000000555
```

Dá pra ver como é a aproximação do número 0.1 em cada tipo de dado e como o tipo `double` é mais preciso.

## Curiosidade 2 - `sizeof`

A função `sizeof` pode ser utilizada para descobrir o tamanho em bytes de um tipo de dado. O código abaixo vai imprimir o tamanho em bytes de cada tipo de dado:

```c
#include <stdio.h>
#include <stdbool.h>

int main() {
  printf("int : %lu\n", sizeof(int));      // 4
  printf("char: %lu\n", sizeof(char));     // 1
  printf("float: %lu\n", sizeof(float));   // 4
  printf("double: %lu\n", sizeof(double)); // 8
  printf("bool: %lu\n", sizeof(bool));     // 1
  return 0;
}
```
