# Estruturas de seleção

<!-- toc -->
- [Introdução](#introdução)
- [Formas de Estruturas de Seleção](#formas-de-estruturas-de-seleção)
  - [1. **Estrutura de Seleção Simples**](#1-estrutura-de-seleção-simples)
  - [2. **Estrutura de Seleção Composta**](#2-estrutura-de-seleção-composta)
- [Exemplo em C](#exemplo-em-c)
<!-- toc -->

## Introdução

As **Estruturas de Seleção**, também conhecidas como **Estruturas Condicionais**,
são elementos fundamentais da programação que permitem ao desenvolvedor controlar
o **fluxo de execução** de um programa com base em **condições lógicas**. Essas
estruturas permitem que uma parte do código seja executada **apenas se** uma
determinada condição for atendida, ou então, caso a condição **não seja satisfeita**,
o programa pode seguir por outro caminho de execução ou tomar outras decisões.

## Formas de Estruturas de Seleção

Existem duas formas principais de Estruturas de Seleção:

### 1. **Estrutura de Seleção Simples**

Também conhecida como `"if-then"` em muitas linguagens de programação, é a forma
mais **básica** de estrutura condicional. Ela avalia uma condição e executa um
bloco de código se essa condição for **verdadeira**. Caso a condição seja **falsa**,
o bloco de código não é executado e o programa continua sua execução normalmente.
Veja esses exemplo abaixo na `linguagem C`:

Exemplo 1:

```c
if (idade >= 18) {
    printf("Você é maior de idade.\n");
}
```

No código acima, a mensagem "Você é maior de idade." apenas vai ser mostrada se
a variável `idade` tiver valor maior ou igual a 18.

Exemplo 2:

```c
if (numero > 0) {
    printf("O número é positivo.\n");
}
```

No código acima, a mensagem "O número é positivo." apenas vai ser mostrada se
a variável `numero` tiver valor maior que 0.

### 2. **Estrutura de Seleção Composta**

É uma extensão da estrutura simples, na qual além de executar um bloco de código
quando uma condição é verdadeira, também pode executar outro bloco de código caso
a condição seja falsa. Veja esses exemplos abaixo na `linguagem c`:

Exemplo 1:

```c
if (idade >= 18) {
    printf("Você é maior de idade.\n");
} else {
    printf("Você é menor de idade.\n");
}
```

No código acima, a mensagem "Você é maior de idade." apenas vai ser mostrada se
a variável `idade` tiver valor maior ou igual a 18. Se a idade for menor 18, então
a mensagem "Você é menor de idade." é mostrada.

Exemplo 2:

```c
if (valor % 2 == 0) {
    printf("o valor é divisível por 2\n");
} else if (valor % 3 == 0) {
    printf("o valor é divisível por 3\n");
} else {
    printf("o valor não é divisível nem por 2 e nem por 3\n");
}
```

É de **extrema** importância perceber que ao usar uma estrutura de seleção composta,
**apenas um único bloco de código vai ser executado**. Além disso, se um valor
satisfaz mais de uma condição, apenas a **primeira ocorrência** que aparecer vai
ser executada. Por exemplo, no código anterior, para uma `valor = 6`, as condições
`(valor % 2 == 0)` e `(valor % 3 == 0)` são verdadeiras. Porém, como a condição
`(valor % 2 == 0)` vem primeiro, apenas o seu bloco vai ser executado, enquanto
as demais condições vão ser ignoradas.

Exemplo 1:

```c
if (media < 4) {
    printf("aluno reprovado\n");
} else if (media >= 4 && media < 7) {
    printf("aluno ficou de af\n");
} else {
    printf("aluno aprovado\n");
}
```

Nesse exemplo, a mensagem `aluno reprovado` será exibida apenas se a variável `media` for
menor que 4. A mensagem `aluno` ficou de af será exibida somente se a variável `media` for
maior ou igual a 4 e menor do que. Já a mensagem `aluno aprovado` será exibida apenas se
a variável `media` for maior do que 7.

## Exemplo em C

Tenha como exemplo o seguinte código abaixo:

```c
#include <stdio.h>

int main() {
    int numero;

    // Solicita ao usuário que insira um número inteiro
    printf("Digite um numero inteiro: ");
    scanf("%d", &numero);

    // Verifica se o número é positivo, negativo ou igual a zero
    if (numero > 0) {
        printf("O numero digitado é positivo.\n");
    } else if (numero < 0) {
        printf("O numero digitado é negativo.\n");
    } else {
        printf("O numero digitado é igual a zero.\n");
    }

    return 0;
}
```

Neste programa, o usuário é solicitado a digitar um número inteiro. Em seguida,
o programa utiliza a estrutura `if-else` para verificar se o número é `positivo`,
`negativo` ou igual a `zero`. Dependendo do resultado, a mensagem apropriada é exibida
na tela.  

Exemplos de execução do código:

- exemplo 1:

```c
Digite um numero inteiro: 10
O numero digitado é positivo.
```

- exemplo 2:

```c
Digite um numero inteiro: -10
O numero digitado é negativo.
```

- exemplo 3:

```c
Digite um numero inteiro: 0
O numero digitado é igual a zero.
```