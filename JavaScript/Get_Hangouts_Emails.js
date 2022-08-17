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

function Stringfy_Array(array) {
	var text = "";
	var item;

	i = 0;
	while (i <= array.length - 1) {
		item = array[i];

		text += item;

		if (item != array[array.length - 1]) {
			text += "\n";
		}

		i += 1;
	}

	return text;
}

function Make_Email_Array(item) {
	emails.push(item);
	console.log("Email: " + item);
}

var emails = [];

var chat_div = xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div[2]/div/div/div/ul");
var chat_div_children = chat_div.childNodes;

var current_email = "";

var i = 0;
while (i <= chat_div_children.length - 1) {
	current_email = chat_div_children[i].children[0].children[0].children[0].children[0].children[0].getAttribute("title").replace(")", "");

	if (current_email.includes("@") && current_email.includes(".")) {
		current_email = current_email.replace(")", "").split(/ \(/)[current_email.replace(")", "").split(/ \(/).length - 1];

		if (current_email.includes(",")) {
			var text = "";
			var c = 0;
			for (var email in current_email.split(",")) {
				email = current_email.split(",")[c];
				text += email;

				if (c == 0) {
					text += "\n";
				}

				c += 1;
			}

			current_email = text;
		}

		Make_Email_Array(current_email);
	}

	i += 1;
}

console.log(Stringfy_Array(emails));