import os
import json

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
target_folder_path = os.path.join(current_dir, "resources/")
dir = target_folder_path + "items.json"

def shopItemMSG(itemName=None, itemDesc=None, itemPrice=None, itemRarity=None, currency=None):
    return f"""
--=[ -{itemName}- ]=--
Описание: {itemDesc}
Редкость: {itemRarity}
"""
# Цена: {itemPrice} {currency}

ShopList = {}
with open(dir, 'r', encoding='utf-8') as f:
    cont = f.read().strip()
    ShopList = cont
d = ShopList
ShopList = json.loads(d)
def GetShop():
    ShopL = {}
    for item in ShopList:
        name = item
        desc = ShopList[item]["description"]
        price = ShopList[item]["price"]
        rarity = ShopList[item]["rarity"]
        stars = ShopList[item]["currency"]
        Sale = ShopList[item]["sale"]
        ShopL[name] = {
            "desc": desc,
            "price": price,
            "rarity": rarity,
            "currency": stars,
            "sale": Sale,
            "msg": shopItemMSG(name, desc, price, rarity, stars)
        }

    return ShopL
def BuyItem(itemName=None, userBalance=None):
    if itemName is None:
        return False
    if userBalance is None:
        return False
    Item = ShopList[itemName]
    if userBalance >= int(Item["price"]):
        return True
    else:
        return False
    