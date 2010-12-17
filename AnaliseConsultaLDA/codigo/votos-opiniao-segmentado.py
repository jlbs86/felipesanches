# Este script gera um gráfico de barras que representa o perfil de opiniões para
# cada segmento de 10% dos usuários participantes, ordenados, da esquerda à direita
# em função do volume de comentário feitos na plataforma da consulta da LDA.

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
num = len(items)/10

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
    total = conc+nconc+ress
    data.append([float(conc)/total,float(nconc)/total,float(ress)/total])
    conc=0
    nconc=0
    ress=0

data.reverse()

import cairoplot

cor_conc = (0,1,0) #verde
cor_ress = (1,1,0) #amarelo
cor_nconc = (1,0,0) #vermelho

colors = [ cor_conc, cor_nconc, cor_ress]
cairoplot.vertical_bar_plot ( '../dados/graficos/votos_opiniao_segmentado.png', data, 2000, 1500, border = 50, display_values = False, grid = True, rounded_corners = True, stack = True, colors = colors )

