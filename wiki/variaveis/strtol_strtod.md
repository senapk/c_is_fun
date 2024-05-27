## Conversão de String para Inteiro e Ponto Flutuante em C

Em programação, muitas vezes é necessário converter strings em valores numéricos para realizar cálculos ou manipulações de dados. Em C, existem duas funções específicas para realizar essas conversões de forma simples e segura: `strtol()` e `strtod()`.

### strtol()

A função `strtol()` é utilizada em C para converter uma string em um valor inteiro (`long int`). Ela está disponível no cabeçalho `<stdlib.h>`.

Exemplo de uso:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    char str[] = "12345";
    char *ptr;
    long int num = strtol(str, &ptr, 10);
    printf("O número convertido é: %ld\n", num);
    return 0;
}
```

Este código converte a string `"12345"` para o longo inteiro `12345`.

### strtod()

A função `strtod()` é utilizada em C para converter uma string em um valor de ponto flutuante (`double`). Assim como `strtol()`, ela está disponível no cabeçalho `<stdlib.h>`.

Exemplo de uso:

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    char str[] = "3.14";
    char *ptr;
    double num = strtod(str, &ptr);
    printf("O número convertido é: %f\n", num);
    return 0;
}
```

Este código converte a string `"3.14"` para o número de ponto flutuante `3.14`.

Essas funções são úteis para converter strings em valores numéricos de forma simples e segura, tratando casos de erro caso a string não represente um número válido.

*Nota: As funções `strtol()` e `strtod()` também estão disponíveis em C++, mas em C++ há alternativas mais convenientes como `stoi()` para conversão para inteiro e `stod()` para conversão para ponto flutuante.*