# -*- coding: utf-8 -*-
from urllib.request import Request, urlopen

# 123123
# 372455
# 4044

req = Request('https://www.urionlinejudge.com.br/judge/en/profile/', headers={
  'User-Agent': 'Mozilla/5.0'
})
res = urlopen(req).read()
res = ''.join(map(chr, res))
res = res.split(' ')

# Name:
index = res.index('class="pb-username">\n')
index = res[index + 30]
name = index.split('>')[1]
name = name.split('<')[0]  

# Place:
index = res.index('<span>Place:</span>\n')
place = res[index + 16]

# University:
index = res.index('<span>University:</span>\n')
index = res[index + 19]
university = index.split('>')[1]
university = university.split('<')[0]

# Since:
index = res.index('<span>Since:</span>\n')
since = res[index + 16]

# Points:
index = res.index('<span>Points:</span>\n')
points = res[index + 16]

# Solved:
index = res.index('<span>Solved:</span>\n')
solved = res[index + 16]

# Tried:
index = res.index('<span>Tried:</span>\n')
tried = res[index + 16]

# Submissions:
index = res.index('<span>Submissions:</span>\n')
submissions = res[index + 16]

print(name)
