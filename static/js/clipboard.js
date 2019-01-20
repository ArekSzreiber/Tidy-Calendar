function copyToClipboard(){
    let outputField = document.getElementById("outputField");
    let outputLink = outputField.select();
    console.log("output"+outputLink);
    console.log(document.getElementById("outputField"));
    console.log("cos");
}

let outputUrlField = document.getElementById("outputField");

let clipboardButton = document.getElementById("copyButton");

clipboardButton.addEventListener("onclick", copyToClipboard);