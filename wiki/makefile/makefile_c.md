# Makefile para Compilação de Código em C

<!-- toc -->
- [Estrutura do Makefile](#estrutura-do-makefile)
- [Descrição dos Alvos e Variáveis](#descrição-dos-alvos-e-variáveis)
  - [Variáveis](#variáveis)
  - [Alvos](#alvos)
- [Como Usar o Makefile](#como-usar-o-makefile)
  - [Compilação](#compilação)
  - [Limpeza](#limpeza)
  - [Execução](#execução)
- [Conclusão](#conclusão)
<!-- toc -->

Este Makefile é projetado para compilar programas em C com uma série de flags de compilação úteis, incluindo `-Wall`, `-Wextra`, entre outras. Ele também demonstra a organização de dependências e a criação de alvos para limpar arquivos gerados durante a compilação.

## Estrutura do Makefile

```makefile
# Definição do compilador
CC = gcc

# Flags de compilação
CFLAGS = -Wall -Wextra -pedantic -std=c11 -O2

# Alvo padrão
all: programa

# Alvo para o programa principal
programa: main.o utils.o
    $(CC) $(CFLAGS) -o programa main.o utils.o

# Alvo para compilar main.o
main.o: main.c
    $(CC) $(CFLAGS) -c main.c

# Alvo para compilar utils.o
utils.o: utils.c
    $(CC) $(CFLAGS) -c utils.c

# Alvo para limpeza dos arquivos compilados
clean:
    rm -f programa main.o utils.o

# Alvo para executar o programa
run: programa
    ./programa
```

## Descrição dos Alvos e Variáveis

### Variáveis

- `CC`: Define o compilador a ser utilizado. Neste caso, `gcc`.
- `CFLAGS`: Define as flags de compilação. Incluímos:
  - `-Wall`: Ativa todas as mensagens de aviso.
  - `-Wextra`: Ativa avisos extras.
  - `-pedantic`: Enforce as regras do padrão C.
  - `-std=c11`: Define o padrão da linguagem C a ser usado (C11 neste caso).
  - `-O2`: Ativa otimizações de compilação de nível 2.

### Alvos

- **all**: Alvo padrão que compila o programa principal. Depende de `programa`.
- **programa**: Compila o executável final a partir dos arquivos objeto `main.o` e `utils.o`.
- **main.o**: Compila o arquivo objeto a partir do código fonte `main.c`.
- **utils.o**: Compila o arquivo objeto a partir do código fonte `utils.c`.
- **clean**: Remove os arquivos gerados durante a compilação (`programa`, `*.o`).
- **run**: Compila o programa (se necessário) e o executa.

## Como Usar o Makefile

### Compilação

Para compilar o programa, basta rodar o comando:

```sh
make
```

Isso irá compilar todos os arquivos necessários e gerar o executável `programa`.

### Limpeza

Para limpar os arquivos compilados, utilize:

```sh
make clean
```

Isso removerá o executável e os arquivos objeto (`*.o`).

### Execução

Para compilar (se necessário) e executar o programa, utilize:

```sh
make run
```

Isso garantirá que o programa está atualizado e o executará em seguida.

## Conclusão

Este Makefile fornece uma base sólida para a compilação de programas em C, incluindo várias flags de compilação que ajudam a detectar problemas no código e a otimizar o desempenho. Com a adição de alvos úteis como `clean` e `run`, ele torna o processo de desenvolvimento mais eficiente e organizado.
