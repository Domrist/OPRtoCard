from fpdf import FPDF
from contants import *

pdf = FPDF(orientation='L', unit='mm', format='A4')

def writeText(x,y,text,sizee=10):
    pdf.set_font(family = "Arial", size = sizee)
    textLength = pdf.get_string_width(text)
    textLength = textLength/2
    pdf.set_xy(x,y)
    pdf.write(0,text)



def writeCenteredText(x,y,text,sizee=10):
    if x < 0:
        #abort()
        print("LESS")
    pdf.set_font(family = "Arial", size = sizee)
    textLength = pdf.get_string_width(text)/2
    x -= textLength
    pdf.set_xy(x,y)
    pdf.write(0,text)



def writeWeaponData(weaponObjects):
    localHeight = 30
    for weaponData in weaponObjects:
        weaponString = ""
        weaponSpecs = ""
        weaponName = weaponData["weaponName"]
        keyIterator = iter(weaponData)
        for key,valu in weaponData.items():
            if key == "weaponName":
                continue
            elif valu == "-":
                continue
            weaponSpecs += valu + ","
        writeText(0, localHeight, weaponName)
        localHeight += STEP_LINE_GLOBAL
        writeText(0, localHeight, "|-" + weaponSpecs)
        localHeight += STEP_LINE_GLOBAL



def getUpgradeRowCount(upgradeObject):
    res = 0
    updgradePageHeader = upgradeObject["key"]
    #print(updgradePageHeader)
    # сперва отработает длинное разделение всего и вся
    if AND_STRING in updgradePageHeader:
        splittedUpgradeHeader = updgradePageHeader.split(AND_STRING)

        for splittedUpgradeHdr in splittedUpgradeHeader:
            localUpradeLineObject = getSplittedUpgradesListPos(splittedUpgradeHdr)
            for item in localUpradeLineObject:
                res += 1    # for upgradeName
                tripleObject = splitStringToTriples(item["upgradeSpecs"])
                res += len(tripleObject)

        for upgradeLine in upgradeObject["value"]:
            tmpUpgradeLine = [var for var in upgradeLine.split("\n") if var]
            upgradeName = tmpUpgradeLine[0]
            upgradeCost = tmpUpgradeLine[1]
            upgradeLineCollection = getSplittedUpgradesListPos(upgradeName)

            for upgrade in upgradeLineCollection:
                tmpUpgradeName = upgrade["upgradeName"]
                tmpUpgradeSpecs = upgrade["upgradeSpecs"]
                tmpUpgradeSpecs = deleteFirstLastStaples(tmpUpgradeSpecs)

                res += 1
                if len(tmpUpgradeSpecs) != 0:
                    res += 1
    else:
        pass

    #print("FINAL RES FOR HEADER => ", res)
    return res



def getHeaderWriteData(a_incomingStr):
    res = []
    updgradePageHeader = a_incomingStr
    if AND_STRING in updgradePageHeader:
        splittedUpgradeHeader = updgradePageHeader.split(AND_STRING)
        for splittedUpgradeHdr in splittedUpgradeHeader:
            #print(splittedUpgradeHdr) # Replace Plague Hammer (A1, Blast(3), Poison)
            localUpradeLineObject = getSplittedUpgradesListPos(splittedUpgradeHdr)
            #print(localUpradeLineObject) # [{'upgradeName': 'Replace Plague Hammer', 'upgradeSpecs': '(A1, Blast(3), Poison)'}]
            for item in localUpradeLineObject:
                res.append(item['upgradeName'])
                print(item['upgradeSpecs'])
                for triplet in splitStringToTriples(item['upgradeSpecs']):
                    res.append(triplet)
        return res



def writeUpdgrade(xPagePos, yPagePos, upgradeObject):
    getUpgradeRowCount(upgradeObject)

    updgradePageHeader = upgradeObject["key"]
    for headerString in getHeaderWriteData(updgradePageHeader):
        writeText(xPagePos,yPagePos,headerString, 10)
        yPagePos += STEP_LINE_GLOBAL

    for upgradeLine in upgradeObject["value"]:
        tmpUpgradeLine = [var for var in upgradeLine.split("\n") if var]
        upgradeName = tmpUpgradeLine[0]
        upgradeCost = tmpUpgradeLine[1]
        upgradeLineCollection = getSplittedUpgradesListPos(upgradeName)

        for upgrade in upgradeLineCollection:
            tmpUpgradeName = upgrade["upgradeName"]
            tmpUpgradeSpecs = upgrade["upgradeSpecs"]
            tmpUpgradeSpecs = deleteFirstLastStaples(tmpUpgradeSpecs)

            writeText(xPagePos,yPagePos, tmpUpgradeName, 8)
            yPagePos += STEP_LINE_GLOBAL
            if len(tmpUpgradeSpecs) != 0:
                writeText(xPagePos,yPagePos, tmpUpgradeSpecs, 8)
                yPagePos += STEP_LINE_GLOBAL
        pdf.line(xPagePos,yPagePos-2,xPagePos+40,yPagePos-2)



def writeFillTest():
    heightShift = 4
    for i in range(12):
        #writeText(40, heightShift, "Some nights expired",10)
        writeText(40, heightShift, "Some nights expired",10)
        heightShift += STEP_LINE_GLOBAL

def initHerCardData(obj):

    writeText(0,5,obj["unitName"])
    writeCenteredText(20, 12,obj["quadef"],14)

    pdf.line(0,15,40,15)

    # генерация кейвордов
    pdf.set_font("Arial", size=8)
    keywordsLength = int(len(obj["keywords"].split(','))/3) # разбиваем кейворды на тройки
    remainingPartOfKeywords = len(obj["keywords"].split(',')) % 3
    splittedKeywords = obj["keywords"].split(',')
    # проходимся по основным тройкам
    counter = 0
    shiftLen = pdf.get_string_width(",")
    heightShift = 20
    for index in range(keywordsLength):
        finalString = ""
        for j in range(3):  # собираем тройки по группам
            finalString += splittedKeywords[counter] + ", "
            counter += 1
        writeCenteredText(20, heightShift, finalString)
        heightShift += STEP_LINE_GLOBAL
    # проходимся по оставшимся элементам (не может быть больше 3 элементов в строке)
    remaingString = ""
    for i in range(remainingPartOfKeywords):
        remaingString += splittedKeywords[counter] + ", "
        counter += 1
    writeCenteredText(20, heightShift, splittedKeywords[3])

    heightShift += STEP_LINE_GLOBAL

    # блок вывода текущего оружия
    writeWeaponData(obj["weapon"])

    # блок вывода первой странички улучшений
    #writeFillTest()
    writeUpdgrade(40,4,obj["upgrades"][0])
    #writeUpdgrade(40,54,obj["upgrades"][1])
    #writeUpdgrade(40,104,obj["upgrades"][2])
    #writeUpdgrade(40,154,obj["upgrades"][3])
