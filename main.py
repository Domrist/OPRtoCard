import json
from CardGenerator import *
from APIJSONParser import *
import requests


pdf = FPDF(orientation='L', unit='mm', format='A4')

cardGenerator = CardGenerator(pdf)

pdf.add_page(orientation = "L", format = "a4")
page_height_page = 0
yRowPageIndex = 0



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
firstPageData = getFirstPageData(localUnit) # DONE
cardGenerator.writeFirstHeroCardData(firstPageData, 0) # DONE

### Write another pages with getUnitUpgrades
unitUpgrades = getUnitUpgrades(localUnit, upgradePackage)

position = Vector2(40, 4)

#cardGenerator.fillTest()

#'''
for unitUpgrade in unitUpgrades:
	cardGenerator.writeUpgradeHeroData(unitUpgrade, position)
#'''


pdf.output("simple_demo.pdf")
