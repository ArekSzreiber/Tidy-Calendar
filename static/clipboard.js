//remember to clear cache

function copyToClipboard(){
    let outputLink = document.getElementById("outputField");
    outputLink.select();
    document.execCommand("copy");
}

let outputUrlField = document.getElementById("outputField");

let clipboardButton = document.getElementById("copyButton");

clipboardButton.addEventListener("click", copyToClipboard);
