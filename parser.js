let mainColumn = document.getElementsByClassName("MuiGrid-root MuiGrid-direction-xs-row")[3];

let unitData = mainColumn.querySelector("#unitSelection");
unitData = unitData.children[0];

let defaultData = unitData.children[0];
let additionalData = unitData.children[1]

// START parse default data

let quaDefContainer = defaultData.children[0];
let keyWords = defaultData.children[1];

// START parse weapon table
let weaponContainer = defaultData.children[2];
weaponContainer = weaponContainer.firstChild;
let weaponList = weaponContainer.children[1];

for(let i = 0;i < weaponList.childElementCount; i++)
{
	let weapon = weaponContainer.children[i];

	let weaponName = weapon.children[0];
	let weaponRange = weapon.children[1];
	let weaponAtk = weapon.children[2];
	let weaponAP = weapon.children[3];
	let weaponSPE = weapon.children[4];

	// LATER PUT THIS DATA TO JSON
}
// END of parase weapon table

// END of parse default data



// START of parsing upgrades (additional data)

let GLOBAL_UPGRADES = {};

let totalIterationCount = (additionalData.childElementCount - 1) / 2;

for(let i = 0; i < totalIterationCount; i++)
{

	let firstElementIndex = i * 2 + 1;
	let secondElementIndex = (i+1) * 2;
	
	let categoryString = additionalData.children[firstElementIndex]; // should go deep down inside to get final value
	let upgradeList = additionalData.children[secondElementIndex];

	//console.log(categoryString.innerText);

	let TMP_ARRAY = [];

	for(let upgradeLineIndex = 0; upgradeLineIndex <  upgradeList.childElementCount; upgradeLineIndex++)
	{
		let upgradeLine = upgradeList.children[upgradeLineIndex];
		//console.log(upgradeLine.innerText);
		TMP_ARRAY.push(upgradeLine.innerText);
	}

	GLOBAL_UPGRADES[categoryString.innerText] = TMP_ARRAY;
}


console.log(GLOBAL_UPGRADES);
