
## Aula 1

  - [ ] ação tal

  ### Introduçao ao C

  ### Variáveis
  - Tipos
    - int
    - char
    - float
    - double
    - texto
    - bool
  - Modificadores
    - long
    - short
    - const
    - static
  - Globais, Locais

  ### Sintaxe
    - linguagens C-Like
    - {} e ;

  ### Hello World
    - exemplo dado pelo professor

## Aula 2

  ### Compilação
    - compilar no terminal com gcc
    - utilizar os parâmetros como -lm -Wall -std=c11
    - utilizar o `clang -Weverything`

    - compreender código fonte, bibliotecas externas
    - abrindo, visualizando e compilando no vscode

    - Avançado (opcional):
      - criar um makefile e compilar utilizando make
      - utilizar as tags `CC` e `CFLAGS`

  ### primeiro codigo
    - include, int main()

## Aula 3

  ### Operações
    - +, -, *, / %

  ### Operadores
    - ==, !=, >, <, >=, <=
    - &&, ||, !
    - x++, x--, ++x, --y

  ### Exercício

## Aula 4

  ### Seleção
  - condicionamento
  - if, else, else if

  ### Exercício

## Aula 5

  ### Exercícios sobre o que já foi aprendido
    - Auxílio do professor e monitores

## Aula 6

  ### Ternário
    - Alertar sobre boas práticas  

## Aula 7

  ### Funções? (preciso de opinião p ver se isso da certo)
    - Parâmetros
    - Retorno
    
## Aula 8

  ### Funções 
    - Simplificando if/else
  
## Aula 9

  ### Repetição
    - While
    - Continue
    - Break

  ### Exemplo de exercício

## Aula 10

  ### Repetição
    
    - For
    - Importância do índice
    - boas práticas

### Trabalhando com múltiplos arquivos
  - Declaração e Definição
  - Avançado: Externe e protótipo
### Debug
  


### Repetição

  
  - Do - While
  - For
  - 
### Enum

  - cast para int

### Struct

  - typedef

### Array

  - criando inline
  - acessando por indice
  - modificando
  - não valida index
  - tecnica do sizeof
  - criando por constantes
  - vet e vet_size
  - preenchimento incremental
  - tamanho e capacidade
  - Passando vetor por parametro
  - Sizeof não funciona dentro
  - 
### Sintaxe de ponteiros

  - Conceito ponteiros
  - p[0]
  - *p
  - p[n] equivale a *(p + n)
  - função swap
  - ponteiros para função
    - função sort

### Strings

  - const char *
  - char nome[]
  - funções úteis
    - strlen, strcpy, strcmp
    - fgets e remoção de \n
    - tratamento de buffer, flush
    - tratamento de erros
    - ascii e conversão de tipo
      - isdig, isalpha, tolower, toupper, isupper, islower
    - converter usando atoi, itoa, strtoll
    - fgets, __strtok_r
  - sscanf, ssprint

### Matrizes

  - mat[][]
  - passando mat por parametro
- math.h
  - pow, round, sqrt, sin, cos
- Variáveis globais, locais e static
- rand e srand
- argc e argv
- conversão tipos
- padding

 ### arquivos
  - redirect no bash usando (input) <,  (overwrite) >, (append) >>
  - envio de EOF com (unix) CTRL-D, (windows) CTRL-Z Enter
  - ler direto de arquivo com FILE *, fscanf, fprintf
  - escrever em arquivo usando FILE *
  - ler e escrever usar arquivo binário
    - dados e structs

### vetores

  - formas de inicialização de um vetor
  - cálculo automático do tamanho do vetor utilizando typedef
  - funções básicas sobre vetores
    - encontrar mínimo em intervalo
    - encontrar posição (valor ou mínimo)
    - contar ocorrências em intervalo
  - técnicas
    - ordenação
    - busca binária
    - vetor auxiliar para filtrar elementos
    - vetor auxiliar para marcação de ocorrências
    - vetor auxiliar para contagem de ocorrências
    - função sort

### Alocação dinâmica

- malloc
- free
- realloc
- calloc
