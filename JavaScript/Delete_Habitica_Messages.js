// ==UserScript==
// @name         Stake2 - Delete Habitica Messages
// @namespace    http://github.com/Stake2/habitica-script/
// @version      1.0
// @description  Delete messages on Habitica website
// @author       You
// @match        https://*.habitica.com/private-messages
// @match        https://*.habitica.com/private-messages/*
// @icon         https://icons.duckduckgo.com/ip2/habitica.com.ico
// @grant        none
// ==/UserScript==

function xpaths(xpath, parent) {
	let results = [];
	let query = document.evaluate(xpath, parent || document,
	null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

	for (let i = 0, length = query.snapshotLength; i < length; ++i) {
		results.push(query.snapshotItem(i));
	}

	return results;
}

var buttons = xpaths("//div[contains(@class, 'action d-flex align-items-center')]");

function Click_On_Remove_Buttons(button_thing) {
	var button_text = button_thing.children[1].textContent;

	if (button_text == " Deletar ") {
		button_thing.click();
	}
}

setTimeout(function() {
	buttons.forEach(Click_On_Remove_Buttons);
	console.log("Finished deleting messages.");
}, 1000);