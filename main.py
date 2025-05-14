import json
from CardGenerator import *
from APIJSONParser import *
import requests
from contants import *


pdf = FPDF(orientation='L', unit='mm', format='A4')
pdf.add_page(orientation = "L", format = "a4")
cardGenerator = CardGenerator(pdf)

y = requests.get('https://army-forge.onepagerules.com/api/army-books/FF4UemWHh60T1VRq?gameSystem=5')
x = requests.get('https://army-forge.onepagerules.com/api/army-books/vJuokTQpJWj3_MrJ?gameSystem=5')

obj = json.loads(y.content)
#obj = json.loads(x.content)
units = obj["units"]


upgradePackage = obj["upgradePackages"] ### CONST

counterRow = 0

for unit in obj["units"]:

	position = Vector2(40, 4 + DEFAULT_CARD_HEIGHT * cardGenerator.yRowScalerPerPage)

	### Write first page
	firstPageData = getFirstPageData(unit) # DONE
	cardGenerator.writeFirstHeroCardData(firstPageData) # DONE
	### Write upgrades pages

	unitUpgrades = getUnitUpgrades(unit, upgradePackage)


	for unitUpgrade in unitUpgrades:
		#print("UNIT_UPGRADE =>", unitUpgrade["options"], "\n\n")
		cardGenerator.writeUpgradeHeroData(unitUpgrade, position)

	for cell in range(int(position.x / DEFAULT_CARD_WIDTH)):
		pdf.rect(DEFAULT_CARD_WIDTH * cell, DEFAULT_CARD_HEIGHT * cardGenerator.yRowScalerPerPage, DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT)

	cardGenerator.increaseRowScaler()

	counterRow += 1

	if counterRow >= 3:
		counterRow = 0
		pdf.add_page(orientation = "L", format = "a4")
		cardGenerator.resetRowScaler()


pdf.output("simple_demo.pdf")


''' OTHER DATA
#for key,val in obj.items():
#	print(key)
'''
