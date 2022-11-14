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









 


