# Esse script gera um gráfico que descreve o perfil de propostas ("alteracao", 
#   "retorno", "exclusao", "acrescimo") para cada segmento de 10 porcento 
#   dos usuários que participaram da consulta da lda.

# A primeira coluna da esquerda representa o perfil de propostas dos 10% de usuários 
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
        autores[c.autor] = {"comments": 1, "proposta": {}}

    try:
        autores[c.autor]["proposta"][c.proposta] += 1
    except:
        autores[c.autor]["proposta"][c.proposta] = 1

items = [ [x[1]["comments"], x[1]["proposta"]] for x in autores.items()]
items.sort()
items.reverse()

data = []
counter = 0
num = len(items)/20

ret=0
excl=0
acr=0
alter=0
for i in items:
  try:
    ret += i[1]["retorno"]
  except:
    pass

  try:
    excl += i[1]["exclusao"]
  except:
    pass

  try:
    alter += i[1]["alteracao"]
  except:
    pass

  try:
    acr += i[1]["acrescimo"]
  except:
    pass

  counter = (counter+1)%num
  if counter==0:
    data.append([alter,ret,excl,acr])
    ret=0
    excl=0
    acr=0
    alter=0

data.reverse()

import cairoplot


cor_retorno = (1,0,0) #vermelho
cor_exclusao = (1,0.7,0) #laranja
cor_alteracao = (1,1,0) #amarelo
cor_acrescimo = (0,0,1) #azul

colors = [ cor_alteracao, cor_retorno, cor_exclusao, cor_acrescimo]
cairoplot.vertical_bar_plot ( '../dados/graficos/propostas_barras_segmentado.png', data, 2000, 1500, border = 50, display_values = False, grid = True, rounded_corners = True, stack = True, colors = colors )

