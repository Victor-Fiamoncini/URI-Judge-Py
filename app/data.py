# -*- coding: utf-8 -*-
from urllib.request import Request, urlopen

req = Request('https://www.urionlinejudge.com.br/judge/en/profile/372455', headers={
  'User-Agent': 'Mozilla/5.0'
})
res = urlopen(req).read()

res = ''.join(map(chr, res))

print(res)
