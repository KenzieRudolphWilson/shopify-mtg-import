#!/usr/bin/python

import shopify
import json
import time

shop_url = "https://7d2a4105a61e881f5ab17389192243f2:07989a2032025d99db86729cc1703150@card-castle-games.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

shop = shopify.Shop.current

# help(shopify)

jsonData = open('SetList.json')
data = json.load(jsonData)
jsonData.close()

for i in range(0, len(data)):
  print data[i]["name"]
  newCollection = shopify.CustomCollection()
  newCollection.title = data[i]["name"]
  newCollection.image = { "image" : ""}

  success = newCollection.save()

  time.sleep(0.5)

  # if success:
  #   print ("Category Created")
