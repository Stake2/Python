// ==UserScript==
// @name         Stake2 - Remove Ad Element from FimFiction
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Remove Ad Element from FimFiction
// @author       Stake2
// @match        https://www.fimfiction.net/*
// @icon         https://icons.duckduckgo.com/ip2/fimfiction.net.ico
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

	function getElementByXpath(path) {
	  return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
	}

	var ad_element = getElementByXpath("/html/body/div[1]/div[1]/div[3]/div/div/div[3]/div[1]/div[2]");

	ad_element.remove();
})();