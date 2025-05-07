from contants import *

### DONE
def getFirstPageWeaponData(a_weaponData):

	weaponName = a_weaponData["name"]
	tmpArr = []

	if a_weaponData["range"] != 0:
		tmpArr.append(("{0}\"").format(a_weaponData["range"]))

	if a_weaponData["attacks"] != 0:
		tmpArr.append(("A{0}").format(a_weaponData["attacks"]))

	for specialRule in a_weaponData["specialRules"]:
		tmpArr.append(specialRule["label"])

	triplets = fromCollectionToStringifyTriplets(tmpArr)

	return { "weaponName" : weaponName, "trinkets" : triplets }



### DONE - WITHOUT POINTS
def getGainData(a_gainObject):

	tmpArr = []
	name = a_gainObject["name"]

	if "content" in a_gainObject:
		if len(a_gainObject["content"]) != 0:
			contents = []
			for content in a_gainObject["content"]:
				contentName = content["name"]
				if "rating" in content:
					contentName = ("{0}({1})").format(contentName, content["rating"])
				tmpArr.append(contentName)

	if "range" in a_gainObject:
		if a_gainObject["range"] != 0:
			tmpArr.append(("{0}\"").format(a_gainObject["range"]))
	if "attacks" in a_gainObject:
		if a_gainObject["attacks"] != 0:
			tmpArr.append(("A{0}").format(a_gainObject["attacks"]))
	if "specialRules" in a_gainObject:
		if len(a_gainObject["specialRules"]) != 0:
			for specRule in a_gainObject["specialRules"]:
				if "rating" in specRule:
					tmpSpecRuleString = specRule["name"] + "(" + str(specRule["rating"]) + ")"
				else:
					tmpSpecRuleString = specRule["name"]
				tmpArr.append(tmpSpecRuleString)


	#triplets = fromCollectionToStringifyTriplets(tmpArr)
	triplets = tmpArr

	return { "gainName" : name, "gainSpecRule" : triplets }



### DONE
def getFirstPageData(a_unit):

	rulesCollection = []

	for rule in a_unit["rules"]:
		rulesCollection.append(rule["label"])
	finalRules = fromCollectionToStringifyTriplets(rulesCollection)

	quaDefString = ("Qua +{0} Def +{1}").format(a_unit["quality"], a_unit["defense"])

	weaponsData = []

	for weaponData in a_unit["weapons"]:
		weaponsData.append(getFirstPageWeaponData(weaponData))

	return { "name" : a_unit["name"], "unitTrinkets" : finalRules, "quaDef" : quaDefString, "weaponsData" : weaponsData }



### DONE - WITHOUT POINTS
def getUnitUpgrades(a_unit, a_totalUpgrades):

	upgradesList = []

	for unitUpgrade in a_unit["upgrades"]:	# just some ids from users
		for upgradePack in a_totalUpgrades:
			if upgradePack["uid"] != unitUpgrade:
				continue

			upgradeSections = upgradePack["sections"]
			for upgradeSection in upgradeSections:

				upgrade = {}
				upgrade["upgradeName"] = upgradeSection["label"]

				gains = []

				for option in upgradeSection["options"]:
					for gain in option["gains"]:
						gainData = getGainData(gain)
						gains.append({"gainName":gainData["gainName"],"gainSpecRule":gainData["gainSpecRule"]})

				upgrade["gains"] = gains
				upgradesList.append(upgrade)

	return upgradesList
