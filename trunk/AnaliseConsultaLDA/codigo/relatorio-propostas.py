#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Esse script gera um relatório de perfil de propostas por usuário 
# ordenado por número total de comentários por usuário.

from model import *
setup_all()

comentarios = Comentario.query.all()
f = open("../dados/relatorio_propostas.txt", "w")
f.write(str(len(comentarios)) + " comentarios\n")

autores = {}
for c in comentarios:

    try:
        autores[c.autor]["comments"] += 1
    except:
        autores[c.autor] = {"comments": 1, "proposta": {}, "url":c.autor_url}

    try:
        autores[c.autor]["proposta"][c.proposta] += 1
    except:
        autores[c.autor]["proposta"][c.proposta] = 1

items = [ [x[1]["comments"], x[0], x[1]["url"], x[1]["proposta"]] for x in autores.items()]
items.sort()
items.reverse()

f.write(str(len(items)) + " usuarios comentaram\n\n")

import math
counter =0
soma=0
for i in items:
#  counter +=1
#  soma += i[0]
#  if soma>(len(comentarios)/2):
#    print math.floor(soma)/len(comentarios) 
#    print counter
#    print math.floor(counter)/len(items)
#    break

#  if counter == 35:
#    print math.floor(soma)/len(comentarios) 
#    break

  #porcentagem do total de comentarios
  f.write("(" + str(math.floor(float(1000000*i[0])/len(comentarios))/10000) + "%)")

  #nome do autor
  f.write("\t" + i[1].encode('utf-8'))

  #url do autor
  f.write(" " + i[2].encode('utf-8'))

  f.write("\t")

  #proposta
  for o in i[3].keys():
    f.write(o+"("+str(i[3][o])+") ")

  f.write("\n")

f.close()

