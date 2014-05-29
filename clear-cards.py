#!/usr/bin/python

import shopify

shop_url = "https://7d2a4105a61e881f5ab17389192243f2:07989a2032025d99db86729cc1703150@card-castle-games.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

shop = shopify.Shop.current

product = shopify.Product.find()
for i in range(0, len(product)):
  product[i].destroy()