# -*- Coding: utf-8; Mode: Python -*-

#Antes de executar esse script pela primeira vez, inicialize a base de dados
# executando create_tables.py
#
#Execute esse script para fazer um dump do site da consulta da lda.

#
# extractor.py - Entry point for the extractor
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

"""This module extracts data from a website containing posts, comments
and user info.
"""

import simplejson
import urllib
import re
from elixir import session
from model import Tag, Paragrafo, Comentario
from datetime import datetime

HARDCODED_POST_ID = 564

API_URL = \
    'http://www.cultura.gov.br/consultadireitoautoral/?dialogue_query=%s'
PAGE_TO_GET_STUFF = \
    "http://www.cultura.gov.br/consultadireitoautoral/consulta/"
GET_PARAGRAPHS_RE = \
    re.compile('name="dialogue_comment_paragraph"\n\s*value="([^\"]+)"', re.M | re.I)

def get_paragraphs():
    """Gets all paragraphs from the PAGE_TO_GET_STUFF page.
    """
    page = urllib.urlopen(PAGE_TO_GET_STUFF)
    content = page.read()
    return GET_PARAGRAPHS_RE.findall(content)

def extract_comments():
    paragraphs = get_paragraphs()
    for i in paragraphs:
        # Creating the paragraph object. It will be stored in a
        # relational database by elixir+sqlalchemy :)
        paragrafo = Paragrafo()
        paragrafo.id = i

        # Building and dispatching the request to get comment data
        query = {'method': 'get_paragraph_comments',
                 'params': [i, HARDCODED_POST_ID]}
        page = urllib.urlopen(API_URL % simplejson.dumps(query))
        json = simplejson.loads(page.read())

        for c in json:
            # Time to save collected things in the database
            comentario = Comentario()
            comentario.id = int(c['comment_ID'])
            comentario.navegador = c['comment_agent']
            comentario.autor = c['comment_author']
            comentario.autor_url = c['comment_author_url']
            comentario.instituicao = c['instituicao']
            comentario.contribuicao = c['meta']['contribuicao']
            comentario.justificativa = c['meta']['justificativa']
            comentario.opiniao = c['meta']['opiniao']
            comentario.proposta = c['meta']['proposta']
            comentario.data = datetime.strptime(
                c['comment_date'], '%Y-%m-%d %H:%M:%S')
            comentario.paragrafo = paragrafo

            # Time to add the comment tags
            for t in c['tags']:
                tag = Tag()
                tag.nome = t['name']
                comentario.tags.append(tag)
        session.commit()

def main():
    """Extracting
    """
    extract_comments()

if __name__ == '__main__':
    main()
