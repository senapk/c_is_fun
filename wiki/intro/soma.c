#include <stdio.h> // inclui a biblioteca padrão de entrada e saída

int main() {
    int num1 = 0; //cria um lugar
    puts("Digite o primeiro número"); //imprime uma mensagem
    scanf("%d", &num1); //lê o número e guarda no lugar num1

    int num2 = 0;
    puts("Digite o segundo número");
    scanf("%d", &num2);

    int soma = num1 + num2; //soma e guarda na variável soma
    printf("A soma de %d e %d é %d\n", num1, num2, soma); //imprime a soma
    return 0;
}