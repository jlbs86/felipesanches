# Esse script gera um relatório ordenado por número total de comentários por usuário.
# Neste relatório, é possivel notar como alguns usuários fizeram qunatidades
# gigantescas de comentários em intervalos de tempo extremamente curtos. 
# Dentre os 5 usuários mais ativos em número de comentários, há um usuário que 
# fez 119 comentários no sistema em pouco menos de 2 horas entre o primeiro
# e o último comentário.

# Além disso, pode-se notar uma altíssima concentração de comentários com autoria 
# de apenas alguns poucos usuários. Cerca de 11% de toda a consulta pública consiste 
# em 650 comentários feitos pelos 5 usuários que mais comentaram. Enquanto os demais
# 89% são a contribuição dos outros 690 usuários.   


from model import *
setup_all()

comentarios = Comentario.query.all()
f = open("../dados/relatorio_opiniao.txt", "w")
f.write(str(len(comentarios)) + " comentarios\n")

autores = {}
for c in comentarios:
    try:
        autores[c.autor]["comments"] += 1
    except:
        autores[c.autor] = {"comments": 1, "opiniao": {}, "datamin": None, "datamax": None}

    try:
        autores[c.autor]["opiniao"][c.opiniao] += 1
    except:
        autores[c.autor]["opiniao"][c.opiniao] = 1

    try:
        if (c.data < autores[c.autor]["datamin"]):
          autores[c.autor]["datamin"] = c.data
        if (c.data > autores[c.autor]["datamax"]):
          autores[c.autor]["datamax"] = c.data
    except:
        autores[c.autor]["datamin"] = c.data
        autores[c.autor]["datamax"] = c.data


items = [ [x[1]["comments"],x[0],x[1]["opiniao"], x[1]["datamin"], x[1]["datamax"]] for x in autores.items()]
items.sort()
items.reverse()

f.write(str(len(items)) + " usuarios comentaram\n\n")

import math
for i in items:
  f.write(str(i[0]) + " (" + str(math.floor(float(1000000*i[0])/len(comentarios))/10000) + "%) ["+str(i[3])+"] " + i[1].encode('utf-8') + "\t")

  for o in i[2].keys():
    f.write(o+"("+str(i[2][o])+") ")

  if (i[0]>1):
    f.write("tempo: " + str(i[4]-i[3]))

  f.write("\n")

f.close()

