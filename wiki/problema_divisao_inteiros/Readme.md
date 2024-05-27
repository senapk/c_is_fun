## O problema da divisão de dois inteiros

<!-- toc -->
- [Introdução](#introdução)
- [Exemplo do problema](#exemplo-do-problema)
- [Resolvendo o problema](#resolvendo-o-problema)
<!-- toc -->

## Introdução

Neste texto, abordaremos um problema comum nas operações aritméticas em C: a divisão inteira. Mostraremos porque ela acontece e como podemos resolver.

## Exemplo do problema

```c
#include <stdio.h>

int main() {
    printf("%d\n", 5 / 2); // 2

    int a = 5;
    int b = 2;
    printf("%d\n", a / b); // 2

    return 0;
}
```

O resultado **esperado** pelo programador dessa operação é o valor 2.5, pois esse é o valor de `5 / 2`. No entanto, se você executar esse código verá que o resultado mostrado é 2.

Isso acontece por conta da forma como o C trata os tipos de dados dentro de uma operação aritmética. Observe que os dois operandos, 5 e 2, são números inteiros, dessa forma, a linguagem realizará apenas uma divisão inteira, que não resulta em casas decimais. Da mesma forma que você aprendeu quando estava na terceira série do ensino fundamental, o resultado de uma divisão inteira é o quociente da divisão, ou seja, a parte inteira do resultado.

## Resolvendo o problema

A abordagem de resolução desse problema é transformar pelo menos um dos valores em um tipo de dado de ponto flutuante, dessa forma a divisão não será inteira.

Dessa forma, precisamos realizar um cast para `double` em pelo menos um dos operandos.

```c
#include <stdio.h>

int main() {
    printf("%f\n", 5 / (double) 2); // 2.500000  fazendo cast
    printf("%f\n", 5.0 / 2);        // 2.500000  usando um literal como ponto flutuante
    
    int a = 5;
    printf("%f\n", a / 2.0);        // 2.500000
    int b = 2;
    printf("%f\n", a / (double) b); // 2.500000

    return 0;
}
```

Essas soluções garantem que a divisão não será inteira, produzindo o resultado desejado de 2.5.