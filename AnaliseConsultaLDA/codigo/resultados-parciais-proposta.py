# Este script gera um gráfico que representa a cada faixa vertical, os resultados 
# do perfil de propostas da consulta da LDA caso se desprezem as contribuições mais 
# volumosas. É possível notar a desvio do perfil de propostas em função da 
# influência gerada pelos usuários que fizeram blocos massivos de comentários.    

# A correta análise de processos colaborativos de consulta requer mecanismos de 
# compensação que ajudem a minimizar o desvio causado pelas participações massivas
# e dar representatividade às demais participações. 

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

data = []
counter = 0
num = len(items)/200

ret=0
excl=0
alter=0
acr=0
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

#  counter = (counter+1)%num

  total = acr+alter+excl+ret
#  if total>0 and counter==0:
  if total>0:
    data.append([float(acr)/total,float(alter)/total,float(excl)/total,float(ret)/total])

import cairoplot

cor_retorno = (1,0,0) #vermelho
cor_exclusao = (1,0.7,0) #laranja
cor_alteracao = (1,1,0) #amarelo
cor_acrescimo = (0,0,1) #azul

colors = [cor_acrescimo, cor_alteracao, cor_exclusao, cor_retorno]
cairoplot.vertical_bar_plot ( '../dados/graficos/resultados_parciais_proposta.png', data, 2000, 1500, border = 50, display_values = False, grid = True, rounded_corners = True, stack = True, colors = colors )

