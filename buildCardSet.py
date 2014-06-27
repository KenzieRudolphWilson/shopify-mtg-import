# -*- coding: utf-8 -*-
import json
import sys
import codecs




def loadCardJSON():
	jsonData = open('AllSetsArray.json')
	data = json.load(jsonData)
	jsonData.close()
	return data


#simple function to parse the mtgJSON data and build a JSON array of unique card names for other code to consume
#returns S

def generateCardMap():
	#python witchery to get stdout to print UTF-8
	#sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 
	
	data = loadCardJSON()
	
	#cardCounter = 0
	nameSet = set()
	for cardSet in data:
	  for cards in cardSet.get("cards"):
	    #cardCounter += 1
	    cardname = unicode(cards.get("name"))
	    cardname.encode('utf-8')
	    nameSet.add(cardname)
	
	
	#print str(nameSet)
	
	cardsJSON =  json.dumps(sorted(list(nameSet)), sort_keys=True,indent=4, separators=(',', ': '))
	#print 'cardinality of generated set: ' + str(len(nameSet)) 
	#print 'total cardsnames found in JSON: ' + str(cardCounter)

	return cardsJSON


def saveUTF8File(content, name):
	namesFile = codecs.open(name, "w", "utf-8")
	namesFile.write(content)
	namesFile.close()