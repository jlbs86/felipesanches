#este script gera um arquivo de texto que posteriormente pode ser usado junto
# a um gerador de nuvem de tags.

from model import *
setup_all()

tags = Tag.query.all()
f = open("../dados/nuvemtags.txt", "w")
for t in tags:
  nome = ""
  for c in t.nome.encode('utf-8').lower():
    if c == ' ' or c == '-':
      pass
    else:
      nome+=c
  f.write(nome + " ")
f.close()

