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

for i in items:
  try:
    ret = i[1]["retorno"]
  except:
    ret = 0

  try:
    excl = i[1]["exclusao"]
  except:
    excl = 0

  try:
    alter = i[1]["alteracao"]
  except:
    alter = 0

  try:
    acr = i[1]["acrescimo"]
  except:
    acr = 0

  data.append([alter,ret,excl,acr])

import cairoplot

colors = [ (1,0.2,0), (1,0.7,0), (1,1,0), (0,0,1) ]
cairoplot.vertical_bar_plot ( '../dados/graficos/propostas_barras.png', data, 2000, 1500, border = 0, display_values = False, grid = True, rounded_corners = False, stack = True, colors = colors )

