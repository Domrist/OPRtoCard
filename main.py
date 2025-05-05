import json
from contants import *
from CardGenerator import *


with open('Data (1).json','r') as heroData:
    data=heroData.read()

obj = json.loads(data)

pdf.add_page()
pdf.set_font("Arial", size=14)

# генерация основных рамок для карточек
for i in range(5):
    xxx = 40 * i
    pdf.rect(xxx, 0, 40, 50)


initHerCardData(obj)



pdf.output("simple_demo.pdf")
