
# for string 'Realm Lord(Private Guard(Men-at-Arms))' recursion level is 2
###Realm Lord
###|-Private Guard
###|--Men-at-Arms
# for string 'Realm Lord(Ap(1), Atk(3))' recursion level is 1
###Realm Lord(
###|-Ap(1)
###|-Atk(3)
# for string 'Realm Lord(Ap, A4, 12") recursion level is 1


def splitStringByTopLevelBraces(a_string):
	arr = []

	counter = 0
	lowerBorder = 0
	higherBorder = 0

	for i in a_string:
		higherBorder += 1
		if i == "(":
			counter += 1
		elif i == ")":
			counter -= 1
		elif i == "," and counter == 0:
			arr.append(a_string[lowerBorder:higherBorder-1])
			lowerBorder = higherBorder

		if higherBorder == len(a_string):
			arr.append(a_string[lowerBorder:higherBorder])

	return arr



def getGetCollectionFromNestedString(a_string):

	objectToModify = {}

	objectToModify["nodeCaption"] = ""
	objectToModify["nodeChilds"] = []
	objectToModify["nodeValues"] = []

	if a_string.count("(") == 0:	# Fast/Hero/etc

		objectToModify["nodeCaption"] = a_string
		return objectToModify

	else:

		objectToModify["nodeCaption"] = a_string[:a_string.find("(")]

		nextStringParse = a_string[a_string.find("(") + 1:a_string.rfind(")")]

		for item in splitStringByTopLevelBraces(nextStringParse):
			if item.count("(") == 1 and item.count(")") == 1:

				tmpObject = {}
				tmpObject["nodeChilds"] = []
				tmpObject["nodeCaption"] = item[:item.find("(")]
				tmpObject["nodeValues"] = []
				tmpObject["nodeValues"].append(item[item.find("(")+1:item.find(")")])

				objectToModify["nodeChilds"].append(tmpObject)
			else:

				obj = getGetCollectionFromNestedString(item)
				objectToModify["nodeChilds"].append(obj)

		return objectToModify



def appendObjectFromNestedCollectionToArray(a_obj, a_arr, a_recursionLevel = 0):

	localRecursionLevel = a_recursionLevel

	appendedString = ""
	if a_recursionLevel != 0:
		appendedString = "|"

	a_arr.append(appendedString + ("-" * a_recursionLevel) + a_obj["nodeCaption"])

	if len(a_obj["nodeValues"]) == 1:
		pass
		# make additional check for text length

	for nodeValue in a_obj["nodeValues"]:
		a_arr.append(str(nodeValue))


	for child in a_obj["nodeChilds"]:
		appendObjectFromNestedCollectionToArray(child, a_arr, localRecursionLevel + 1)

	return a_arr



def printObjectArr(a_arrToPrint):
	for i in a_arrToPrint:
		print(i)





x = 'Realm Lord(Private Guard( Men-at-Arms))'
y = 'Realm Lord(Ap(1), Atk(3))'
z = 'Realm Lord(Ap, A4, 12")'

a = 'Realm Lord'

recursion = 'Realm Lord(Private Guard(Men-at-Arms(Realm Lord(Private Guard( AP(1), Men-at-Arms)))))'
recursion2 = 'Realm Lord(Private Guard(Fast,Men-at-Arms(Realm Lord(Private Guard( AP(1), Men-at-Arms))), Furious))'
recursion21 = 'Private Guard(Men-at-Arms(Realm Lord(Private Guard( AP(1), Men-at-Arms))))'
recursion22 = 'Men-at-Arms(Realm Lord(Private Guard( AP(1), Men-at-Arms)))'
recursion23 = 'Realm Lord(Private Guard( AP(1), Men-at-Arms))'
recursion24 = 'Private Guard( AP(1), Men-at-Arms)'
recursion25 = 'AP(1), Men-at-Arms'

'''

Realm Lord
(
	Private Guard
	(
		Men-at-Arms
		(
			Realm Lord
			(
				Private Guard
				(
					AP(1),
					Men-at-Arms
				)
			)
		)
	)
)

'''

z = ['Fast', 'Flying', 'Impact(2)', 'Tough(3)', 'Claws', 'Bait', 'Joust']

zz = ['Fast', 'Flying', 'Impact(2)', 'Tough(3)', 'Claws', 'Drop Rock']

ff = z

arr = ["asd","qwe","zxc", "rty","fgh","vbn"]


finalTriples = []

index = len(ff)

while len(ff) != 0:
	st = ",".join(ff[:index])

	if len(st) > 20:
		index -= 1
	else:
		finalTriples.append(st)
		ff = ff[index:]
		index = len(ff)

print(finalTriples)





#printObjectArr(tmpArr)

#getGetCollectionFromNestedString(recursion2)
