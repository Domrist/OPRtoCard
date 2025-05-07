import json
import os
from CardGenerator import *
from APIJSONParser import *

directory = os.getcwd() + "/JSONCollectoin/"

pdf.add_page(orientation = "L", format = "a4")
page_height_page = 0
yRowPageIndex = 0


import requests
#'https://army-forge.onepagerules.com/api/army-books/FF4UemWHh60T1VRq?gameSystem=5'
x = requests.get('https://army-forge.onepagerules.com/api/army-books/cF1dpwd4bhYsNhsf?gameSystem=5')

obj = json.loads(x.content)
units = obj["units"]

#for key,val in obj.items():
#	print(key)

upgradePackage = obj["upgradePackages"]


for i in range(7):
	pdf.rect(40 * i, 0 * DEFAULT_CARD_HEIGHT, DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT)


### Write first page
localUnit = units[0]
#firstPageData = getFirstPageData(localUnit) # DONE
#writeFirstHeroCardData(firstPageData, 0) # DONE

unitUpgrades = getUnitUpgrades(localUnit, upgradePackage)
#for unitUpgrade in unitUpgrades:
print(unitUpgrades[0])
writeUpgradeHeroData(unitUpgrades[0], 4)

pdf.output("simple_demo.pdf")
