import json
import os
from CardGenerator import *

print(os.getcwd())

directory = os.getcwd() + "JSONCollection"

directory2 = "C:\\Users\domri\PycharmProjects\OPRCardGenerator\OPRtoCard\JSONCollectoin"

for file in os.scandir(directory2):
    print(file)
    with open(file, 'r') as heroData:
        data = heroData.read()
        obj = json.loads(data)

        pdf.add_page()

        # генерация основных рамок для карточек
        for i in range(7):
            xxx = 40 * i
            pdf.rect(xxx, 0, 40, 50)

        initHerCardData(obj)
'''
with open('OPRtoCard\\Data.json','r') as heroData:
    data=heroData.read()

obj = json.loads(data)

pdf.add_page()

# генерация основных рамок для карточек
for i in range(7):
    xxx = 40 * i
    pdf.rect(xxx, 0, 40, 50)


initHerCardData(obj)

'''

pdf.output("simple_demo.pdf")
