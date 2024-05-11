# Hello World

Um primeiro código em C é geralmente um programa simples que visa familiarizar os iniciantes com a sintaxe e os conceitos básicos da linguagem. Vamos criar um exemplo de um programa que exibe uma mensagem na tela.

````cpp
#include <stdio.h> // Inclui a biblioteca stdio.h, que permite a entrada/saída de dados.

// Tudo que é escrito após // é um comentário e é ignorado pelo compilador.

int main() // A função main() é o ponto de partida de qualquer programa C.
{
    printf("Olá, mundo! Este é o meu primeiro programa em C.\n");
    // A função printf é usada para exibir mensagens na tela.
    // \n representa uma quebra de linha.

    return 0; // Indica que o programa foi concluído com sucesso. (opcional)
}
````

**Explicação:**

1. `#include <stdio.h>`: Esta linha inclui a biblioteca `stdio.h`, que fornece funcionalidades para entrada/saída de dados em C. Ela contém a função `printf()` para imprimir mensagens na tela.

2. `int main()`: Todo programa C precisa ter a função `main()`, que é o ponto de entrada do programa. O tipo de retorno `int` indica que a função `main()` deve retornar um valor inteiro (0 neste caso) para indicar o status de saída do programa.

3. `{}`: As chaves indicam o início e o fim do escopo da função `main()`. Todas as instruções dentro dessas chaves fazem parte do corpo da função.

4. `printf("Olá, mundo! Este é o meu primeiro programa em C.\n");`: Esta linha utiliza a função `printf()` para exibir uma mensagem na tela. A mensagem é delimitada pelas aspas duplas (`"..."`). `\n` é usado para adicionar uma quebra de linha após a mensagem.

5. `return 0;`: O comando `return` é usado para finalizar a função `main()` e retornar um valor inteiro (0) que indica que o programa foi concluído com sucesso. Valores diferentes de zero podem indicar diferentes estados de saída do programa, mas, nesse caso, 0 é usado para sucesso. No caso da main em C, esse retorno também pode ser omitido.