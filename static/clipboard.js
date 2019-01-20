//remember to clear cache

function copyToClipboard(){
    let outputLink = document.getElementById("outputField");
    outputLink.select();
    document.execCommand("copy");
}

let clipboardButton = document.getElementById("copyButton");

clipboardButton.addEventListener("click", copyToClipboard);
