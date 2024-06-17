# Strings em C: Arrays de `char`

<!-- toc -->
- [Introdução](#introdução)
- [Representação de Strings como Arrays de `char`](#representação-de-strings-como-arrays-de-char)
  - [Definição de uma String](#definição-de-uma-string)
  - [Terminador Nulo](#terminador-nulo)
  - [Acesso e Modificação de Strings](#acesso-e-modificação-de-strings)
- [Inicialização de Strings](#inicialização-de-strings)
  - [Inicialização Direta](#inicialização-direta)
  - [Inicialização com Tamanho Especificado](#inicialização-com-tamanho-especificado)
  - [Inicialização Caracter a Caracter](#inicialização-caracter-a-caracter)
- [Leitura de Strings do Teclado](#leitura-de-strings-do-teclado)
  - [Leitura com `%s`](#leitura-com-s)
  - [Leitura com `%[^\n]`](#leitura-com-n)
- [Conclusão](#conclusão)
<!-- toc -->

## Introdução
Em C, as strings não são um tipo primitivo, mas são representadas como arrays de caracteres (`char`). Isso significa que uma string em C é simplesmente uma sequência de caracteres armazenada em um array, terminada por um caractere nulo (`\0`). Este guia explicará como as strings funcionam em C, demonstrando a relação entre strings e arrays de caracteres.

## Representação de Strings como Arrays de `char`

### Definição de uma String
Uma string em C pode ser definida de várias maneiras. Aqui está um exemplo básico:

```c
char saudacao[] = "Olá, Mundo!";
```

Neste exemplo, `saudacao` é um array de caracteres que contém os caracteres 'O', 'l', 'á', ',', ' ', 'M', 'u', 'n', 'd', 'o', '!', seguidos por um terminador nulo `\0`.

### Terminador Nulo
O terminador nulo `\0` é crucial na representação de strings em C. Ele indica o fim da string, permitindo que funções da biblioteca padrão saibam onde a string termina. Sem esse terminador, funções como `printf` não saberiam onde parar ao imprimir a string.

### Acesso e Modificação de Strings
Como strings são arrays, você pode acessar e modificar os caracteres individuais usando notação de índice de array:

```c
saudacao[0] = 'H';
printf("%s\n", saudacao); // Saída: "Hlá, Mundo!"
```

## Inicialização de Strings
Existem várias maneiras de inicializar uma string em C:

### Inicialização Direta
```c
char saudacao[] = "Olá, Mundo!";
```
Aqui, o compilador calcula automaticamente o tamanho do array, incluindo o terminador nulo.

### Inicialização com Tamanho Especificado
```c
char saudacao[13] = "Olá, Mundo!";
```
Você pode especificar o tamanho do array, mas precisa garantir que ele seja grande o suficiente para armazenar todos os caracteres, incluindo o terminador nulo.

### Inicialização Caracter a Caracter
```c
char saudacao[] = {'O', 'l', 'á', ',', ' ', 'M', 'u', 'n', 'd', 'o', '!', '\0'};
```
Essa forma explicita cada caractere, incluindo o terminador nulo.

Leitura de Strings do Teclado
Leitura com %s

O especificador de formato %s é utilizado na função scanf para ler strings do teclado. Contudo, %s para de ler a entrada no primeiro espaço em branco encontrado.
Exemplo

c

#include <stdio.h>

int main() {
    char nome[50];
    printf("Digite seu nome: ");
    scanf("%s", nome);  // Lê uma string até o primeiro espaço
    printf("Olá, %s!\n", nome);
    return 0;
}

Neste exemplo, se o usuário digitar "João Silva", apenas "João" será armazenado na variável nome.
Leitura com %[^\n]

O especificador de formato %[^\n] pode ser utilizado para ler uma linha inteira, incluindo espaços, até encontrar uma nova linha (\n).
Exemplo

c

#include <stdio.h>

int main() {
    char nomeCompleto[100];
    printf("Digite seu nome completo: ");
    scanf("%[^\n]", nomeCompleto);  // Lê até a nova linha
    printf("Olá, %s!\n", nomeCompleto);
    return 0;
}

Neste exemplo, se o usuário digitar "João Silva", "João Silva" será armazenado na variável nomeCompleto.

## Conclusão
Strings em C são arrays de caracteres terminados por um caractere nulo (`\0`). Esta representação permite flexibilidade e eficiência no manuseio de strings, mas requer que o programador gerencie manualmente aspectos como o terminador nulo e o tamanho do array. A compreensão de como as strings são representadas e manipuladas é essencial para programação eficaz em C.
