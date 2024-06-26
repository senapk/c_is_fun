# Valores, Lugares e Casting

Em C++, o casting é uma operação que permite converter explicitamente um valor de um tipo para outro. Isso é útil quando queremos garantir que um determinado valor seja tratado como outro tipo.

<!-- toc -->
- [Conversões implícitas](#conversões-implícitas)
- [Cast Tradicional do C](#cast-tradicional-do-c)
<!-- toc -->

## Conversões implícitas

Conversões acontecem naturalmente quando utilizamos o operador de atribuição. Essas conversões são chamadas de implícitas e serão mais aprofundadas no próximo arquivo, até lá, vamos relembrar os tipos de dados padrão:

```c
5     //int
5.4   //double
3.6f  //float
'a'   //char
true  //boolean
```

Quando fazemos uma atribuição, ele vai tentar converter da melhor forma possível.

- Um ponto flutuante para inteiro vai perder a parte fracionada.

```c
int x = 5.53;   //double para int
int y = 4.123f; //float para int
printf("%d, %d", x, y); // 5, 4
```

- Um inteiro para ponto flutuante vai ser convertido sem perdas.

```c
double x = 5;
printf("%lf", x); //5.0
```

- Um inteiro para `char` vai ser convertido de acordo com a [tabela ASCII](../string/tabela_asc2.md). Definindo o tipo no printf como inteiro ou char altera o comportamento.

```c
int x = 'a';
printf("%d", x); //97

char c = 97;
printf("%c", c); //'a';
```

- Booleano `false` é qualquer valor zero. Todo o resto é convertido para `true`.

```c
#include <stdbool.h>

bool f = 3;
printf("%d", f); //true (1)

bool g = 0;
printf("%d", g); //false (0)
```

## Cast Tradicional do C

Você não precisa de uma atribuição para converter um tipo para outro, isso pode ser feito diretamente através de um cast.

A sintaxe do C-style cast é a seguinte:

```c++
(tipo) valor;
```

Onde tipo é o tipo de dados para o qual desejamos converter a expressão.

```c++
#include <iostream>
int main() {
    std::cout << (char) 97 << '\n'; //a
    std::cout << (int) 45.1235 << '\n'; //45
}
```
