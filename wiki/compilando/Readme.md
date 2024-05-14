# Compilando manualmente

<!-- toc -->
- [Compilando e executando](#compilando-e-executando)
- [Explicando as flags](#explicando-as-flags)
<!-- toc -->

## Compilando e executando

Para compilar, você precisa ter o `gcc` instalado. Crie e salve o arquivo como `arquivo.c`. Navegue até a pasta onde você salvou o arquivo. Ao dar o comando `ls` dentro da pasta, você deve encontrar o arquivo que salvou. Após isso, compile e execute com os comandos. Abra o `terminal` com o `bash` e digite:

**No Windows:**

```bash
gcc -Wall -Wextra -Werror arquivo.c -o arquivo.exe
.\arquivo.exe
```

**No Linux:**

```bash
gcc -Wall -Wextra -Werror arquivo.c -o arquivo.out
./arquivo.out
```

A primeira linha compila o código-fonte `arquivo.c` para gerar o arquivo executável `arquivo.exe` (no Windows) ou `arquivo.out` (no Linux). Se houver qualquer erro ou **possível erro**, as flags `-Wall`, `-Wextra` e `-Werror` vão impedir a finalização e avisar onde você deve consertar.

O comando `.\arquivo.exe` ou `./arquivo.out` é uma instrução para executar o código gerado pela primeira linha.

## Explicando as flags

No contexto do compilador GCC (GNU Compiler Collection), as opções `-Wall`, `-Wextra` e `-Werror` são usadas para controlar a exibição de mensagens de aviso (warnings) e como esses avisos são tratados durante o processo de compilação. Aqui está uma explicação de cada uma delas:

### -Wall (Ativar todos os avisos padrão)

Por exemplo, se você tem um código com variáveis não inicializadas ou conversões implícitas, o `-Wall` pode emitir avisos relacionados a essas questões, incentivando boas práticas de programação.

### -Wextra (Ativar mais avisos além dos habilitados por -Wall)

Ao usar `-Wextra`, o compilador será mais proativo na identificação de situações suspeitas no código-fonte, como variáveis não utilizadas ou conversões que podem levar a perda de dados.

### -Werror (Tratar avisos como erros)

Avisos (warnings) indicam possíveis problemas e normalmente não impedem o processo de compilação. Com o `-Werror`, os avisos serão tratados como erros, impedindo a finalização do processo de compilação.