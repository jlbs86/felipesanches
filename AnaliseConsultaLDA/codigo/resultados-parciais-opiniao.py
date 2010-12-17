# Este script gera um gráfico que representa a cada faixa vertical, os resultados 
# do perfil de opinioes da consulta da lda caso se desprezem as contribuições mais 
# volumosas. É possível notar a desvio do perfil de opiniões em função da 
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
        autores[c.autor] = {"comments": 1, "opiniao": {}}

    try:
        autores[c.autor]["opiniao"][c.opiniao] += 1
    except:
        autores[c.autor]["opiniao"][c.opiniao] = 1

items = [ [x[1]["comments"], x[1]["opiniao"]] for x in autores.items()]
items.sort()
#items.reverse()

data = []
counter = 0
num = len(items)/200

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

#  counter = (counter+1)%num
#  if counter==0:
#    total = conc+nconc+ress
#    data.append([float(conc)/total,float(ress)/total,float(nconc)/total])

  total = conc+nconc+ress
  if total>0:
    data.append([float(conc)/total,float(ress)/total,float(nconc)/total])

#data.reverse()

import cairoplot

cor_conc = (0,1,0) #verde
cor_ress = (1,1,0) #amarelo
cor_nconc = (1,0,0) #vermelho

colors = [ cor_conc, cor_ress, cor_nconc]
cairoplot.vertical_bar_plot ( '../dados/graficos/resultados_parciais_opiniao.png', data, 2000, 1500, border = 50, display_values = False, grid = True, rounded_corners = True, stack = True, colors = colors )

