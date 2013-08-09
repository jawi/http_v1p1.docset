#!/opt/local/bin/python2.7

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag 

db = sqlite3.connect('Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

docpath = 'Resources/Documents'

page = open(os.path.join(docpath,'rfc2616.html')).read()
soup = BeautifulSoup(page)

any = re.compile('.*')
for tag in soup.find_all('a', {'href':any}):
    name = tag.text.strip()
    if len(name) > 0 and not re.compile("\[\d+\]").match(name):
        path = tag.attrs['href'].strip()
        elems = path.split('#')
        resName = elems[0]
        anchor = elems[1] if len(elems) == 2 else ""
        depth = len(anchor.split("."))
        _type = 'Section' if depth == 1 else 'Entry' if depth == 2 else 'Keyword'
        if resName not in ('index.html', 'biblio.html', 'bookindex.html'):
            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, _type, path))
            print 'name: %s, path: %s, type: %s, depth: %d' % (name, resName, _type, depth)

db.commit()
db.close()
