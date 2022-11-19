# Diário Projeto DNC

## 12/11/22 Sábado

Encontrei esse projeto antigo nos meus arquivos e resolvi continua-lo pois agora minha habilidades de python estão melhores.

O projeto original foi feito uma parte em python e outro em delphi.

Quero produzir as interfaces gráficas todas em pyGTK.

Este arquivo de diário eu vou planejando os próximos passos bem como reltando o que foi desenvolvido até o momento.

Criei um repositório público no github para ir subindo o estado atual na esperança que sabe de alguém perceber o quanto esse projeto é legal e quem sabe querer ajudar. E também, para que o código fonte fique na núvem disponibilizado de forma gratuita para qualquer pessoa que quiser continuar a partir  dessas idéias e desse trabalho.  


## TODO

Acho que boa parte do código já funciona.
Preciso ver os vídeos que deixei, brincar, testar, compreender e depois tentar criar as interfaces gráficas.

criar uma pasta lab para usar de laboratorio e ir explorando novamente o codigo.
E depois quem sabe criar novos videos com a documentacao. 

## Animações

Estou explorando

https://www.geeksforgeeks.org/how-to-create-animations-in-python/

Para ver se consigo fazer uma animacao de 2 passos se distanciando.
A idéia seria gerar animações em tempo real para cada passo dado no editor.

Ficou bom!

## Matplotlib

Então.

O stpEditor é um puro editor dos steps e facilita mas não é importante.
Os stps do Zouk já estão escritos.

Quero mesmo é fazer maos uns estudos do matplotlib para estudar como plotar e visualizar os passos no ambiente 3d.

Ficou interessante também.

## Enfim gtk

Enfim vou fazer o editor então se é o que falta.
Ele vai abrir o arquivo de caminho e mostrar o caminho sendo percorrido ao lado.


## Gtk nao - Ainda nao

## Sistemas de Referencias

Pista de Dança = P

Condutor = T

Conduzido = Z


pD do Condutor = pD
pE do Condutor = pE

Um frame em cada um

Transformações de um frame para outro

Eu preciso de T que leva do Frame do pD para frame da Pista de Danca para poder plotar esses objetos de forma satisfatoria.

A parte fácil é que estamos no Plano 2D. Entao os Ts serão matrizes 2x2.

Agora vou ter que ver como fazer essas contas usando python.

## Roda Imagem

A rotação de imagens não é muito straight-forward, ou seja, precisarei de outras bibliotecas.


https://stackoverflow.com/questions/59401957/rotating-images-on-a-matplotlib-plot

https://note.nkmk.me/en/python-opencv-numpy-rotate-flip/

Acho melhor usar:

> scikit-image

https://opensource.com/article/19/3/python-image-manipulation-tools

> Pillow

https://pythontic.com/image-processing/pillow/rotate

Tem várias possibilidades mas por hj cansei.


## Então vou seguir nas classes criando a classe para o Condutor e Conduzido.

Condutor ou Conduzido sao mesmas instancias da mesma classe Dançarino, Pessoa.

O importante é ter dois pés. 

## O Editor 

Resolvi que em vez de desenvolver um novo editor do zero, vou pegar 
um que tenho pronto e editar.

E vou fazer tudo no mesmo app. Tanto o editor de caminhos quanto o editor de sequencias.

## Sem delongas

Sem delongas quero criar um comando que vai ler o arquivo de caminho
Separar a parte que está o comando
E mostrar as figuras aos lado

Vou gerar as figuras em arquivos separados e ler no programa.
 
Ficou bom!
 
## Outras coisas

Em vez de criar vários arquivos separados.
Pensei que vai simplificar criar só um arquivo chamado por exemplo:

"DNC_Zouk_V1.txt"

E lá dentro eu coloco várias linhas assim:

"DNC_Zouk_V1_Condutor" vai ser o equivalente ao Cenário

DNC_Zouk_V1_Condutor_BAS_LAT_DIR
1:2:3:pD.ABR
2:1:1:pE.FCF
3:1:2:pD.LUG

DNC_Zouk_V1_Condutor_BAS_LAT_ESQ
1:2:3:pE.ABR
2:1:1:pD.FCF
3:1:2:pE.LUG

## Várias Possibilidades

São várias possibilidades.

Ao criar somente "DNC_Zouk_V1.txt"

Lá dentro eu posso editar tudo.
E depois ele lê esse arquivo para carregar as possibilidades de opções de sequencias.
Para criar as sequencias.

## Nota sobre o django

Sobre o django.


A idéia de usar o django é para modelar o banco de dados de árvore lá.
E pq árvore?

Pq a idéia é que existem pares complementares de caminhos condutor / conduzido. Ou seja, quando um condutor executa um caminho o conduzido executa outro.
As possibilidades são inúmeras. E para mapear isso, nada melhor do que um grafo.

Um grafo hierárquico no qual os caminhos são mapeados para cada agente.
E depois um tipo diferente de associação que indica os pares de caminhos do condutor e do conduzido que são complementares.

Por fim, eu quero usar o graphviz para testar novas possibilidades de visualizar a árvore.

## Rodar Imagens

pip install opencv-python
pip install imutils


Primeiro problema. Tanto pillow quanto openCV comem os cantos quando a rotação é diferente de multiplos de 90 graus.
Entao preciso colocar as imagens dos pés dentro de bolas que ficam dentro de quadrados para que os cantos não sejam comidos.

Pronto.

Agora vou tentar implementar a rotação da imagem (pelo menos). A questão de rodar tudo eu farei testes depois.


#### Funcionou

Funcionou mas está longe do que quero.
Ele roda a imagem só.

Mas terei de fazer modificações nas Classes dos Pes para guardar a rotação absoluta deles em relação ao core.
E modificar o doStep para lá dentro realizar as rotações quando o modificador de rotação estiver presente.

A idéia é a seguinte.
Rotações precisam de 2 passos para finalizar.

O primeiro pé que roda roda, mas o pe que ficou pra tras nao roda junto.
Quando o outro pe recebe qualquer comando, sua posicao de rotacao final é calculada usando a posicao de rotacao do pe espelhado.

Ex.:

pE.FRT:ft  --> Pede pro pE ir pra frente e rodar para fora 45 graus
Ele vai lá e olha o pe direito. Se o t do pe direito é zero, entao o o seu t final sera 0 + 45
Blz

Ai depois vc faz
pD.FRT:ft

Ai ele vai olhar a projecao do pe esquerdo e perceber que a diferenca de rotacao entre pE e pD é de 45 graus ja
Entao a posicao final do pD sera 45 (inicial) + 45 (o que ft mandou fazer) e portanto 90;

E assim cada pe tera que ter um angulo theta de rotação relativo ao core.

Quando pes se movimentam, o core deve se movimentar junto (igual é feito na translacao).
Só que eu so vou rotacionar o core quando os dois pes rodam e combinam um theta final igual.

OU

Ou eu posso fazer o core rodar com os pE e pD ficando no meio do caminho do theta dos dois.

Ex.: pE tá em +180 e pE tá em 45.
Nesse momento core tá em 180+45/2.

Ex.: pE tá em +45 e pE tá em -45.
Nesse momento core tá em 0.

De qualquer forma uma plotagem nova que preciso fazer é o angulo theta de cada coisa.
Angulo theta do pD pE e do Core.

uma forma e calcular uma linha nos graficos que ja desenho de forma a mostrar tudo junto.

Outra forma e plocar graficos separados mostrando os thetas de cada coisa.

Continuo depois....


## 19/11

Então vamos às alterações pra colocar angulo de orientação em tudo.
