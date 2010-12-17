# -*- Coding: utf-8; Mode: Python -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from elixir import metadata, setup_all, create_all, Entity, Field, Unicode, \
     DateTime, Integer, OneToMany, ManyToMany, ManyToOne

class Tag(Entity):
    nome = Field(Unicode(256))
    comentarios = ManyToMany('Comentario')

class Paragrafo(Entity):
    id = Field(Unicode(64), primary_key=True)
    conteudo = Field(Unicode)
    comentario = OneToMany('Comentario')

class Comentario(Entity):
    data = Field(DateTime)
    autor = Field(Unicode)
    autor_url = Field(Unicode)
    instituicao = Field(Unicode)
    contribuicao = Field(Unicode)
    justificativa = Field(Unicode)
    opiniao = Field(Unicode)
    proposta = Field(Unicode)
    tags = ManyToMany(Tag, inverse='comentarios')
    paragrafo = ManyToOne(Paragrafo)

metadata.bind = "sqlite:///db"
metadata.bind.echo = True
setup_all()

if __name__ == '__main__':
    create_all()
