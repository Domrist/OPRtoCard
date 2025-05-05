import json
from contants import *
from CardGenerator import *


with open('Data.json','r') as heroData:
    data=heroData.read()

obj = json.loads(data)

pdf.add_page()

# генерация основных рамок для карточек
for i in range(7):
    xxx = 40 * i
    pdf.rect(xxx, 0, 40, 50)


initHerCardData(obj)



pdf.output("simple_demo.pdf")
