
function parse()
{

	let dataToSave = {}

	let mainColumn = document.getElementsByClassName("MuiGrid-root MuiGrid-item MuiGrid-grid-xs-true css-6lvoxv")[2];

	let unitName = mainColumn.children[0];
	let unitPoints = mainColumn.children[0];

	for(let i = 0; i < 4;i++)
	{
		unitName = unitName.children[0];
	}

	unitPoints = unitPoints.children[0];
	unitPoints = unitPoints.children[1];
	unitPoints = unitPoints.children[0];

	console.log(unitPoints)

	dataToSave["unitName"] = unitName.innerText;
	dataToSave["unitPoints"] = unitPoints.innerText;


	let unitData = mainColumn.querySelector("#unitSelection");
	unitData = unitData.children[0];

	let defaultData = unitData.children[0];
	let additionalData = unitData.children[1]

	// START parse default data

	let quaDefContainer = defaultData.children[0];
	let keyWords = defaultData.children[1];

	dataToSave["quadef"] = quaDefContainer.innerText;
	dataToSave["keywords"] = keyWords.innerText;

	// START parse weapon table
	let weaponContainer = defaultData.children[2];
	weaponContainer = weaponContainer.firstChild;
	let weaponList = weaponContainer.children[1];

	weaponDataArray = [];

	for(let i = 0;i < weaponList.childElementCount; ++i)
	{
		let weaponData = {};
		let weapon = weaponList.children[i];

		let weaponName = weapon.children[0].innerText;
		let weaponRange = weapon.children[1].innerText;
		let weaponAtk = weapon.children[2].innerText;
		let weaponAP = weapon.children[3].innerText;
		let weaponSPE = weapon.children[4].innerText;

		weaponData["weaponName"] = weaponName;
		weaponData["weaponRange"] = weaponRange;
		weaponData["weaponAtk"] = weaponAtk;
		weaponData["weaponAP"] = weaponAP;
		weaponData["weaponSPE"] = weaponSPE;

		weaponDataArray.push(weaponData);
	}

	dataToSave["weapon"] = weaponDataArray;

	// END of parase weapon table
	// END of parse default data
	// START of parsing upgrades (additional data)

	let GLOBAL_UPGRADES = [];

	console.log(additionalData.childElementCount);

	let totalIterationCount = (additionalData.childElementCount - 1) / 2;

	for(let i = 0; i < totalIterationCount; i++)
	{

		let firstElementIndex = i * 2 + 1;
		let secondElementIndex = (i+1) * 2;
		
		let categoryString = additionalData.children[firstElementIndex]; // should go deep down inside to get final value
		let upgradeList = additionalData.children[secondElementIndex];

		let localPair = {};

		let TMP_ARRAY = [];

		for(let upgradeLineIndex = 0; upgradeLineIndex <  upgradeList.childElementCount; upgradeLineIndex++)
		{
			let upgradeLine = upgradeList.children[upgradeLineIndex];
			//console.log(upgradeLine.innerText);
			TMP_ARRAY.push(upgradeLine.innerText);
		}

		localPair["key"] = categoryString.innerText;
		localPair["value"] = TMP_ARRAY;

		GLOBAL_UPGRADES.push(localPair);
	}

	dataToSave["upgrades"] = GLOBAL_UPGRADES

}
