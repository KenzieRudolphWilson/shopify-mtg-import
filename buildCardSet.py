# -*- coding: utf-8 -*-
import json
import sys
import codecs


#simple script to parse the mtgJSON data and build a JSON array of unique card names for other code to consume
#run once, then forget about it until there are new sets in the MTGJSON

def loadCardJSON():
	jsonData = open('AllSetsArray.json')
	data = json.load(jsonData)
	jsonData.close()
	return data


#python witchery to get stdout to print UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 

data = loadCardJSON()

cardCounter = 0
nameSet = set()
for cardSet in data:
  for cards in cardSet.get("cards"):
    cardCounter += 1
    cardname = unicode(cards.get("name"))
    cardname.encode('utf-8')
    nameSet.add(cardname)


#print str(nameSet)
namesFile = codecs.open("cardNameSet.json", "w", "utf-8")

cardsJSON =  json.dumps(sorted(list(nameSet)), sort_keys=True,indent=4, separators=(',', ': '))
namesFile.write(cardsJSON)
namesFile.close()

#print 'cardinality of generated set: ' + str(len(nameSet)) 
#print 'total cardsnames found in JSON: ' + str(cardCounter)
