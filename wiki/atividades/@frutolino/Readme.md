
![Seu Frutolino](cover.png)

## A feira do Seu Frutolino

Ocê já ouviu falar do Seu Frutolino? Ele é um cabra bom danado que tem uma feira cheia de frutas bunitas e com nomes daqueles que fazem a gente morrer de tanto rir. Ele tá ficando cada vez mais famoso por causa da precisão doida com que ele controla as frutas e os preços delas. Pra manter tudo direitinho, ele precisa da ajuda dos cabras bons de programação pra criar uma função arretada que transforme as informações das frutas numa coisa bem organizadinha.

O Seu Frutolino guarda as informações das frutas dele em umas cordas, assim ó: "nome; valor; quantidade". Por exemplo, se a corda disser "banana; 4.50; 120", isso quer dizer que ele tem uma fruta chamada "banana", que custa 4.50 e tem 120 unidades por lá.

Ele precisa que vocês, jovens programadores, criem uma função do balacobaco em C que transforme essa corda numa "coisinha" com uns campos assim:

- **nome**: o nome da fruta (string)
- **valor**: o valor da fruta (float)
- **quantidade**: a quantidade de frutas (int)

Vamo lá ajudar o Seu Frutolino a botar ordem nessa feira, bando de minino réi bão!


### Entrada

- Uma string com o nome da fruta, o valor e a quantidade, separados por ponto e vírgula.

### Saída

- O nome, o valor e a quantidade da fruta, separados por linha.

### Observação

- Use `sscanf()` para parsear a fruta
- `"%[^;];"` irá ler o nome sem pegar o ponto e vírgula.

## Exemplos

```
>>>>>>>> banana
banana; 4.50; 120
========
nome: banana
valor: 4.50
quantidade: 120
<<<<<<<<

>>>>>>>> laranja
laranja; 3.25; 80
========
nome: laranja
valor: 3.25
quantidade: 80
<<<<<<<<

>>>>>>>> abacaxi
abacaxi; 2.75; 150
========
nome: abacaxi
valor: 2.75
quantidade: 150
<<<<<<<<

>>>>>>>> melancia
melancia; 6.80; 50
========
nome: melancia
valor: 6.80
quantidade: 50
<<<<<<<<

>>>>>>>> uva
uva; 5.00; 300
========
nome: uva
valor: 5.00
quantidade: 300
<<<<<<<<

>>>>>>>> pera
pera; 3.00; 200
========
nome: pera
valor: 3.00
quantidade: 200
<<<<<<<<
```