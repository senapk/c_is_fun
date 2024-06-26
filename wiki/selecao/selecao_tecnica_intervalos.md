# Seleção intervalada

<!-- toc -->
- [Introdução](#introdução)
- [Como Implementar a Seleção Intervalada](#como-implementar-a-seleção-intervalada)
- [Exemplo da Classificação de Faixa Etária](#exemplo-da-classificação-de-faixa-etária)
- [Implementação em C](#implementação-em-c)
- [Código Equivalente](#código-equivalente)
- [Programa Redundante](#programa-redundante)
<!-- toc -->

## Introdução

A seleção intervalada é uma técnica usada para categorizar valores dentro de
**intervalos específicos**. Em geral, esse método envolve o uso de estruturas
condicionais como `if-else` para verificar em qual intervalo um valor se
encaixa e, em seguida, executar ações com base nessa categoria.

## Como Implementar a Seleção Intervalada

A abordagem geral para implementar a seleção intervalada envolve os seguintes
passos:

1. Definir os intervalos: Identifique os intervalos que serão utilizados para
categorizar os valores. Cada intervalo deve ser **mutuamente exclusivo** e abranger
um conjunto de valores que devem ser classificados na mesma categoria.

2. Estabelecer condições: Usando instruções condicionais, crie condições que
verifiquem em qual intervalo o valor se enquadra.

3. Realizar a seleção: Com base nas condições, classifique o valor no
intervalo apropriado e execute as ações correspondentes a essa categoria.

A seleção intervalada é amplamente utilizada para resolver **problemas de
categorização**, classificação ou tomada de decisões com base em faixas de
valores.

## Exemplo da Classificação de Faixa Etária

Neste exemplo específico, vamos usar a técnica de seleção intervalada para
classificar pessoas em faixas etárias: criança, adolescente, adulto e idoso.

Seguindo os passos de implementação citados:

1. **Definir os intervalos**:
    - **Idoso**: 60 anos ou mais
    - **Adulto**: 18 a 59 anos
    - **Adolescente**: 13 a 17 anos
    - **Criança**: 0 a 12 anos

2. **Estabelecer condições**:
    - **idade** >= 60 (Idoso)
    - **idade** < 60 e **idade** >= 18 (Adulto)
    - **idade** < 18 e **idade** >= 13 (Adolescente)
    - **idade** < 13 e **idade** >= 0 (Criança)

3. **Realizar a seleção**:

Uma maneira de implementar essas condições seria se aproveitar do fluxo da
estrutura de seleção `if-else`. Tenha como exemplo o trecho de código em
C abaixo:

```c
if (idade >= 60){
    // Idoso
} else if (idade >= 18){
    //Adulto
} else if (idade >= 13){
    //Adolescente
} else if (idade >= 0){
    //Criança
} else {
    //Idade inválida
}
```

Como idoso é um extremo da nossa classificação, ele é colocado como **condição
inicial**. Se a idade passada for maior que 60, então a classificação correta é
`idoso`. No caso de não passar na primeira condição, então podemos ter certeza
que é falso que `idade >= 60`, ou seja, `idade < 60`. O fluxo segue para a
segunda condição. Se a idade for maior que 18, como já sabemos que `idade < 60`,
então então a classificação correta é `Adulto`. A partir daqui o código segue
a mesma lógica para classificar os demais valores.

## Implementação em C

Veja abaixo uma implementação valida do problema da classificação de faixa
etária em C:

```c
#include <stdio.h>

int main() {
    int idade;

    // Solicita ao usuário que insira uma idade válida 
    printf("Digite uma idade válida: ");
    scanf("%d", &idade);
    
    // Verifica em qual grupo a idade se encaixa
    if (idade >= 60){
        printf("Idoso\n");
    } else if (idade >= 18){
        printf("Adulto\n");
    } else if (idade >= 13){
        printf("Adolescente\n");
    } else if (idade >= 0){
        printf("Criança\n");
    } else {
        // Valor negativo
        printf("Idade inválida\n");
    }

    return 0;
}
```

Neste programa, o usuário é solicitado a digitar uma idade válida. Em seguida,
o programa utiliza a técnica de seleção intervalada para verificar  em qual
categoria a idade se encaixa. Dependendo do resultado, a mensagem apropriada
é exibida na tela.

Exemplos de execução do código:

- exemplo 1

```c
Digite uma idade válida: 6
Criança
```

- exemplo 2

```c
Digite uma idade válida: 15
Adolescente
```

- exemplo 3

```c
Digite uma idade válida: 23
Adulto
```

- exemplo 4

```c
Digite uma idade válida: 72
Idoso
```

- exemplo 5

```c
Digite uma idade válida: -10
Idade inválida
```

## Código Equivalente

Esse trecho de código é equivalente ao código anterior, porém trata os intervalos de forma inversa. Neste caso, a condição inicial é `idade < 0` e a condição final é `idade >= 60`.

```c
if (idade < 0){
    printf("Inválido\n");
} else if (idade < 13){
    printf("Criança\n");
} else if (idade < 18){
    printf("Adolescente\n");
} else if (idade < 60){
    printf("Adulto\n");
} else {
    printf("Idoso\n");
}
```

## Programa Redundante

Mesmo que o código abaixo funcione, ele é redundante e não é uma boa prática de programação. A dupla verificação de `idade >= 0` é desnecessária, pois se a idade for menor que 0, o fluxo do programa não passará pela primeira condição e irá direto para a segunda condição.

```c
    if (idade < 0){
        printf("Inválido\n");
    } else if (idade >= 0 && idade < 13){
        printf("Criança\n");
    } else if (idade >=13 && idade < 18){
        printf("Adolescente\n");
    } else if (idade >=18 && idade < 60){
        printf("Adulto\n");
    } else {
        printf("Idoso\n");
    }
```