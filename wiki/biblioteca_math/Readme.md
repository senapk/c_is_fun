## A biblioteca `math.h` em C

<!-- toc -->
- [Introdução](#introdução)
- [Principais funções](#principais-funções)
  - [Função `pow`](#função-pow)
  - [Função `sqrt`](#função-sqrt)
  - [Função `abs`](#função-abs)
  - [Funções `floor`, `ceil` e `round`](#funções-floor-ceil-e-round)
- [Outras funções](#outras-funções)
<!-- toc -->

## Introdução

Neste texto, vamos explorar a biblioteca `math.h` em C, que é uma biblioteca padrão do C que fornece funções matemáticas comuns. A biblioteca `math.h` contém um conjunto de funções que permitem realizar cálculos matemáticos avançados, como potenciação, raiz quadrada, valor absoluto e arredondamentos.

## Principais funções

### Função `pow`

A função `pow` é usada para calcular a potência de um número. Ela aceita dois argumentos: a base e o expoente, e retorna a base elevada ao expoente. A função `pow` trabalha com números em ponto flutuante.

```c
#include <stdio.h>
#include <math.h>    //pow

int main() {
    printf("Dois ao cubo: %.2f\n", pow(2, 3));          // 8.00
    printf("2.5 elevado a 3.1: %.2f\n", pow(2.5, 3.1)); // 17.12
    return 0;
}
```

### Função `sqrt`

A função `sqrt` é utilizada para calcular a raiz quadrada de um número. Ela aceita um único argumento, que é o número do qual queremos calcular a raiz quadrada, e retorna o resultado. A função `sqrt` também trabalha com números em ponto flutuante.

```c
#include <stdio.h>
#include <math.h> //sqrt

int main() {
    printf("Raiz de 25: %.2f\n", sqrt(25));   // 5.00
    printf("Raiz de 1.5: %.2f\n", sqrt(1.5)); // 1.22
    return 0;
}
```

### Função `abs`

A função `abs` é utilizada para calcular o valor absoluto de um número, ou seja, ignorando o sinal dele. Ela aceita um único argumento, que é o número do qual queremos o valor absoluto, e retorna o resultado.

Para valores em ponto flutuante utilize o `fabs`.

```c
#include <stdio.h>
#include <math.h> //abs

int main() {
    printf("Valor absoluto de -2: %d\n", abs(-2));     // 2
    printf("Valor absoluto de 2: %d\n", abs(2));       // 2
    printf("Valor absoluto de -1.5: %.2f\n", fabs(-1.5)); // 1.50
    printf("Valor absoluto de 1.5: %.2f\n", fabs(1.5));   // 1.50
    return 0;
}
```

### Funções `floor`, `ceil` e `round`

Essas funções servem para calcular o arredondamento de números reais, cada uma utilizando um critério específico:

- `floor`: Arredonda um número para baixo, por exemplo 2.9 seria arrendado para 2.0 mesmo estando mais próximo do 3.0.
- `ceil`: Arredonda um número para cima, por exemplo 2.1 seria arrendado para 3.0 mesmo estando mais próximo do 2.0.
- `round`: Arrendonda um número baseado no valor da casa decimal, por exemplo, 2.2 seria arredondado para 2.0 e 2.7 seria arredondado para 3.0.

```c
#include <stdio.h>
#include <math.h> //floor, ceil, round

int main() {
    printf("floor de 2.1: %.2f\n", floor(2.1)); // 2.00
    printf("ceil de 2.1: %.2f\n", ceil(2.1));   // 3.00
    printf("round de 2.1: %.2f\n", round(2.1)); // 2.00

    printf("floor de 2.7: %.2f\n", floor(2.7)); // 2.00
    printf("ceil de 2.7: %.2f\n", ceil(2.7));   // 3.00
    printf("round de 2.7: %.2f\n", round(2.7)); // 3.00
    return 0;
}
```

É importante observar que, para utilizar as funções da biblioteca `math.h`, é necessário incluir a biblioteca `<math.h>` no início do programa.

## Outras funções

A biblioteca `math.h` possui várias outras funções que podem ser interessantes dependendo do seu problema, como cálculo de logaritmos, funções trigonométricas e funções hiperbólicas.

Você pode visualizar a lista completa [aqui](https://en.cppreference.com/w/c/numeric/math).