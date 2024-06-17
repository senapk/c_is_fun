#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Definindo a Fruta
typedef struct {
    char nome[50];
    float valor;
    int quantidade;
} Fruta;

// Função que recebe uma string e retorna uma Fruta

Fruta parseFruta(char *str) {
    Fruta fruta;

    sscanf(str, "%[^;]; %f; %d", fruta.nome, &fruta.valor, &fruta.quantidade);

    return fruta;
}

int main() {
    char input[100];
    scanf("%[^\n]", input);

    Fruta fruta = parseFruta(input);

    // Exibindo as informações da struct
    printf("nome: %s\n", fruta.nome);
    printf("valor: %.2f\n", fruta.valor);
    printf("quantidade: %d\n", fruta.quantidade);

    return 0;
}