# -*- coding: utf-8 -*-
import json
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 
jsonData = open('AllSetsArray.json')
data = json.load(jsonData)
jsonData.close()
i = 0
for set in data:
  for cards in set.get("cards"):
    i += 1
    cardname = unicode(cards.get("name"))
    cardname.encode('utf-8')
    print cardname

print 'hello' + str(i)