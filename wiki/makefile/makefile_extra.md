# Adendos ao Makefile

## Variáveis Automáticas

No Makefile, você pode utilizar variáveis automáticas para simplificar as regras. Algumas das mais comuns incluem:

- `$@`: O nome do alvo da regra.
- `$<`: O primeiro item na lista de dependências.
- `$^`: A lista de todas as dependências, sem duplicatas.

### Exemplo

```makefile
programa: main.o utils.o
    $(CC) $(CFLAGS) -o $@ $^
```

Aqui, `$@` será substituído por `programa` e `$^` por `main.o utils.o`.

## Diretivas `include`

Você pode dividir seu Makefile em vários arquivos e usar a diretiva `include` para incorporá-los. Isso é útil para projetos grandes.

### Exemplo

```makefile
include paths.mk
include flags.mk

programa: main.o utils.o
    $(CC) $(CFLAGS) -o programa main.o utils.o
```

## Regras Implícitas

Make possui regras implícitas que podem ser aproveitadas para simplificar o Makefile. Por exemplo, você não precisa definir explicitamente como compilar cada arquivo `.c` em `.o`.

### Exemplo

```makefile
# Regras implícitas
%.o: %.c
    $(CC) $(CFLAGS) -c $<

programa: main.o utils.o
    $(CC) $(CFLAGS) -o $@ $^
```

## Funções no Makefile

Makefiles suportam várias funções internas que podem ser usadas para operações de texto, manipulação de listas, etc.

### Função `wildcard`

Utilizada para obter uma lista de arquivos correspondentes a um padrão.

```makefile
SRC = $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)
```

### Função `patsubst`

Substitui um padrão em uma lista de palavras.

```makefile
SRC = src/main.c src/utils.c
OBJ = $(patsubst %.c, %.o, $(SRC))
```

## Diretivas de Condicionais

Você pode adicionar condicionais ao seu Makefile para compilar código de maneira diferente com base em certas condições.

### Exemplo

```makefile
DEBUG ?= 0
ifeq ($(DEBUG), 1)
    CFLAGS += -g
else
    CFLAGS += -O2
endif
```

## Phony Targets

Alvos fictícios (phony targets) são utilizados para definir comandos que não correspondem a arquivos reais. Isso evita conflitos se houver arquivos com os mesmos nomes dos alvos.

### Exemplo

```makefile
.PHONY: clean all

all: programa

clean:
    rm -f programa main.o utils.o
```

## Diretivas `$(shell ...)`

Você pode executar comandos do shell e capturar sua saída com a função `$(shell ...)`.

### Exemplo

```makefile
DATE := $(shell date +%Y-%m-%d)
```

## Conclusão

Esses adendos fornecem funcionalidades adicionais e técnicas avançadas para escrever Makefiles mais poderosos e flexíveis. Utilizando variáveis automáticas, regras implícitas, funções e condicionais, você pode melhorar significativamente a manutenção e a escalabilidade do seu processo de compilação.