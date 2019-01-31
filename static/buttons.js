let downloadButton = document.getElementById("downloadButton");
let generateButton = document.getElementById("generateButton");
let usernameSelect = document.getElementById("usernameSelect");

function activateButton(){
    downloadButton.disabled = false;
    generateButton.disabled = false;
}

usernameSelect.addEventListener("change", activateButton);
