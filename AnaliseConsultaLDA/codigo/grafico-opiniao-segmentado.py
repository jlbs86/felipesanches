# Esse script gera um gráfico que descreve o perfil de opiniões ("concordo", 
#   "não concordo" e "concordo com ressalvas") para cada segmento de 10 porcento 
#   dos usuários que participaram da consulta da lda.

# A primeira coluna da esquerda representa o perfil de opiniões dos 10% de usuários 
# que fizeram a menor quantidade de comentarios no sistema por usuário (ou seja, 
# os 10% de usuários que participaram com menor intensidade).

# A última coluna da direita representa os 10% de usuários que contribuiram o maior 
# volume de comentários.

from model import *
setup_all()

comentarios = Comentario.query.all()

autores = {}
for c in comentarios:

    try:
        autores[c.autor]["comments"] += 1
    except:
        autores[c.autor] = {"comments": 1, "opiniao": {}}

    try:
        autores[c.autor]["opiniao"][c.opiniao] += 1
    except:
        autores[c.autor]["opiniao"][c.opiniao] = 1

items = [ [x[1]["comments"], x[1]["opiniao"]] for x in autores.items()]
items.sort()
items.reverse()

data = []
counter = 0
num = len(items)/20

conc=0
nconc=0
ress=0
for i in items:
  try:
    conc += i[1]["concordo"]
  except:
    pass

  try:
    nconc += i[1]["nao-concordo"]
  except:
    pass

  try:
    ress += i[1]["concordo-com-ressalvas"]
  except:
    pass

  counter = (counter+1)%num
  if counter==0:
    data.append([conc,nconc,ress])
    conc=0
    nconc=0
    ress=0

data.reverse()

import cairoplot

cor_conc = (0,1,0) #verde
cor_ress = (1,1,0) #amarelo
cor_nconc = (1,0,0) #vermelho

colors = [ cor_conc, cor_nconc, cor_ress]
cairoplot.vertical_bar_plot ( '../dados/graficos/opiniao_barras_segmentado.png', data, 2000, 1500, border = 50, display_values = False, grid = True, rounded_corners = True, stack = True, colors = colors )

