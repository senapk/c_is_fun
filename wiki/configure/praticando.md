# Praticando com as ferramentas

## 1. Abra o terminal

Dependendo do seu sistema operacional, abra o terminal.

- Windows: Pode usar o Git Bash, PowerShell, ou o terminal do Windows.
- MacOS: Use o Terminal.
- Linux: Use o Terminal.

## 2. Crie e navegue até a pasta de trabalho

Utilize os comandos `cd` e `ls` para navegar até a pasta de trabalho. Ao chegar lá, crie um diretório chamado `c_workspace`:

```bash
mkdir c_workspace
cd c_workspace
```

## 3. Abra a pasta no VSCode

```bash
code .
```

## 4. Crie um arquivo de código C básico

No VSCode, crie um arquivo chamado `hello.c` com o seguinte conteúdo:

```c
#include <stdio.h>

int main() {
    printf("Hello, World!\n");
    return 0;
}
```

Salve o arquivo.

## 5. Compile o código C

Você pode abrir o terminal no VScode. Compile o código com as flags `-Wall` para mostrar todos os avisos:

```bash
gcc -Wall hello.c -o hello
```

## 6. Execute o código compilado

```bash
./hello
```

Você verá a saída:

```txt
Hello, World!
```

### Resumo dos Comandos

```bash
mkdir c_workspace
cd c_workspace
code .
```

No VSCode, crie e salve `hello.c` com o conteúdo fornecido. Depois, no terminal:

```bash
gcc -Wall hello.c -o hello
./hello
```

Esta prática cobre a criação de uma pasta de trabalho, abertura no VSCode, escrita de um código C básico, compilação com avisos e execução no terminal.

## Passos opcionais

Após instalar o Git Bash, você pode criar um atalho para abrir o Git Bash no diretório atual. Para isso, clique com o botão direito na pasta de trabalho pelo gerenciador de arquivos, depois, selecione "Git Bash Here" e o terminal será aberto no diretório atual.

## Conclusão

Após conseguir realizar todos os passos, você pode marcar essa atividade como concluída.
