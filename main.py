import json
import os
from CardGenerator import *


directory = os.getcwd() + "/JSONCollectoin/"

pdf.add_page(orientation = "L", format = "a4")
page_height_page = 0
yRowPageIndex = 0


for file in os.listdir(directory):
	tmpFilePath = directory+file

	with open(tmpFilePath, 'r') as heroData:
		data = heroData.read()
		obj = json.loads(data)

		unitData = initHerCardData(obj)

		# генерация основных рамок для карточек
		for i in range(unitData.getUnitDataPageCount()):
			pdf.rect(40 * i, yRowPageIndex * DEFAULT_CARD_HEIGHT, DEFAULT_CARD_WIDTH, DEFAULT_CARD_HEIGHT)

		writeHeroCardData(unitData, yRowPageIndex)
		page_height_page += DEFAULT_CARD_HEIGHT
		yRowPageIndex += 1

		if yRowPageIndex >= 3:
			pdf.add_page(orientation = "L", format = "a4")
			page_height_page = 0
			yRowPageIndex = 0


pdf.output("simple_demo.pdf")
