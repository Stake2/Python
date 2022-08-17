// ==UserScript==
// @name         Stake2 - Hide message list of social networks
// @namespace    http://github.com/stake2/hide-message-list-userscript/
// @version      1.0
// @description  Hide message list of social networks
// @author       You

// @match        https://discord.com/library
// @match        https://discord.com/channels/@me
// @match        https://discord.com/channels/@me/*
// @match        https://discord.com/store
// @icon         https://icons.duckduckgo.com/ip2/discord.com.ico

// @grant        none
// ==/UserScript==

function print(text) {
	console.log(text);
}

function xpath(path) {
	return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function insertAfter(newNode, referenceNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
	print("Really added element.");
}

function Language_Item_Definer(item_english, item_portuguese) {
	if (language.includes("en-")) {
		return item_english;
	}

	if (language.includes("pt-")) {
		return item_portuguese;
	}
}

print("Starting script...");

var website_link = String(window.location.href);

var language = navigator.language;

var activate_button, original_display, message_list, message_list_xpath, element_to_append_to, element_to_append_to_xpath, show_text, hide_text, button_style;

function Hide_Message_List() {
	message_list.style.display = "none";

	activate_button.textContent = show_text;
	activate_button.setAttribute("onclick", "Show_Message_List();");
	print("Hiding message list.");
}

function Show_Message_List() {
	message_list.style.display = original_display;

	activate_button.textContent = hide_text;
	activate_button.setAttribute("onclick", "Hide_Message_List();");
	print("Showing message list.");
}

// Defines the variables for the Discord social network
if (website_link.includes("discord.com")) {
	original_display = "flex";

	message_list_xpath = "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div[1]";
	element_to_append_to_xpath = "/html/body/div[1]/div[2]/div/div[2]/div/div[1]/nav/ul/div[2]/div[3]";

	show_text = Language_Item_Definer("Show DMs", "Mostrar MDs");
	hide_text = Language_Item_Definer("Hide DMs", "Esconder MDs");
	button_style = `.hide_message_list_style:hover {
		background-color: #FFFFFF!important;
		color: #36393f!important;
	}`;
}

// Creates the CSS class
var style = document.createElement("style");
style.innerHTML = button_style;
var body = document.getElementsByTagName("body")[0];
body.appendChild(style);

// Creates the button and adds the text
activate_button = document.createElement("button");
activate_button.innerHTML = hide_text;

// Adds the onclick and class attributes
activate_button.setAttribute("onclick", "Hide_Message_List();");
activate_button.setAttribute("class", "hide_message_list_style");

if (website_link.includes("discord")) {
	activate_button.style.borderRadius = "56px";
	activate_button.style.color = "#FFFFFF";
	activate_button.style.backgroundColor = "#36393f";
	activate_button.style.fontSize = "14px";
	activate_button.style.lineHeight = "20px";
	activate_button.style.fontWeight = "600";
	activate_button.style.fontFamily = 'Arial,sans-serif';
	activate_button.style.marginBottom = "15%";
	activate_button.style.marginLeft = "17%";
	activate_button.style.width = "48px";
	activate_button.style.height = "48px";
}

var interval = setInterval(function() {
	message_list = xpath(message_list_xpath);
	element_to_append_to = xpath(element_to_append_to_xpath);
	print(message_list)

	if (message_list != null) {
		// Inserts the button into the page
		print(activate_button);
		print(element_to_append_to);

		if (element_to_append_to != null) {
			insertAfter(activate_button, element_to_append_to);
			print("Added element.");
		}

		window.clearInterval(interval);
		Hide_Message_List();
	}
}, 200);