// ==UserScript==
// @name         Stake2 - Send message with enter on Wattpad
// @namespace    http://github.com/stake2/wattpad-script/
// @version      1.0
// @description  Send message with enter on Wattpad
// @author       You
// @match        https://*.wattpad.com/inbox
// @match        https://*.wattpad.com/inbox/*
// @icon         https://icons.duckduckgo.com/ip2/wattpad.com.ico
// @grant        none
// ==/UserScript==

function xpath(path) {
	return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function xpaths(xpath, parent) {
	let results = [];
	let query = document.evaluate(xpath, parent || document,
	null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

	for (let i = 0, length = query.snapshotLength; i < length; ++i) {
		results.push(query.snapshotItem(i));
	}

	return results;
}

var wattpad_url = "https://www.wattpad.com";
var wattpad_inbox_url = wattpad_url + "/inbox";
var link = window.location.href;

var stake2_profile_link = "https://img.wattpad.com/useravatar/stake2.128.501615.jpg";

function Detect_Message_Box() {
	xpath("/html/body/div[4]/div/div/div/div/div[1]").remove();
	xpath("/html/body/div[4]/div/div/div/div/div[2]").remove();
	var main_content = xpath("/html/body/div[4]/div/div/div/div/div").style.maxWidth = "900px";
	var message_box_parent = xpath("/html/body/div[4]/div/div/div/div/div/form/div[1]");

	var old_message_box = xpath("/html/body/div[4]/div/div/div/div/div/form/div[1]/textarea");
	var message_border = xpath("/html/body/div[4]/div/div/div/div/div/form/div[1]");
	xpath("/html/body/div[4]/div/div/div/div/div/form/div[1]/div").remove();

	var app_container = document.querySelector('#app-container');

	var style_element = document.head.appendChild(document.createElement("style"));
	style_element.innerHTML = "#app-container:after {content: none;display: none;}#inbox .conversation-container .main .conversations {height: unset;min-height: unset;padding-bottom: unset;overflow-y: unset;}";

	var conversation_form = xpath("/html/body/div[4]/div/div/div/div/div/form");
	conversation_form.style.position = "none";
	conversation_form.style.borderTop = "none";

	var conversations = xpath("/html/body/div[4]/div/div/div/div/div/div[2]");
	conversations.style.height = "none";
	conversations.style.minHeight = "none";

	var column_main = xpath("/html/body/div[4]/div/div/div/div/div");
	column_main.style.display = "block";

	var send_button = xpath("/html/body/div[4]/div/div/div/div/div/form/div[2]/button");

	var textarea = xpath("/html/body/div[4]/div/div/div/div/div/form/div[1]/textarea");
	textarea.style.fontSize = "unset";
	textarea.style.padding = "13px 15px";

	send_button.style.display = "none";

	old_message_box.style.color = "#000";
	message_border.style.border = "1px solid #000";
	message_border.style.height = "130px";
	message_border.style.borderRadius = "3%";
	message_border.style.background = "none";
	old_message_box.setAttribute("placeholder", "Escreva uma mensagem...");
	old_message_box.removeAttribute("spellcheck");

	document.body.style.color = "black";

	NodeList.prototype.forEach = Array.prototype.forEach

	var person_name = xpath("/html/body/div[4]/div/div/div/div/div/div[1]/h2").textContent;

	var check_username = function(item, index) {
		var a_element = item.children[0];
		var image_element = a_element.children[0];
		var image_src = image_element.getAttribute("src");

		if (image_src != stake2_profile_link && image_src != null) {
			image_element.setAttribute("alt", person_name + "\n\n");
		}

		if (image_src == stake2_profile_link && image_src != null) {
			image_element.setAttribute("alt", "stake2\n\n");
		}
	};

	var children = conversations.childNodes;
	var check = setInterval(function(){
		children.forEach(check_username)
	}, 100);

	old_message_box.addEventListener("keyup", function(event) {
		// Number 13 is the "Enter" key on the keyboard
		if (event.keyCode === 13 && event.shiftKey === false) {
			// Cancel the default action, if needed
			event.preventDefault();
			// Trigger the button element with a click
			send_button.click();
		}
	});
}

function Set_Event_Listener(element) {
	var a_element = element.children[0].children[2];

	a_element.setAttribute('href', wattpad_url + a_element.getAttribute("href"));
	a_element.setAttribute("target", "_blank");
}

function hashHandler() {
	this.oldHash = window.location.href;
	this.Check;

	var that = this;
	var detect = function() {
	if (window.location.href != wattpad_inbox_url && that.oldHash != window.location.href) {
		console.log("Link changed: " + window.location.href);
		that.oldHash = window.location.href;

		setTimeout(function() {
			Detect_Message_Box();
		}, 650);
	}
	};

	this.Check = setInterval(function(){ detect() }, 100);
}

document.getElementById("footer-container").remove();

if (link == wattpad_inbox_url) {
	setTimeout(function() {
		xpaths("/html/body/div[4]/div/div/div/div/div[2]").forEach(Set_Event_Listener);
	}, 2000);

	var hashDetection = new hashHandler();
}

else {
	setTimeout(function() {
		Detect_Message_Box();
	}, 1300);
}