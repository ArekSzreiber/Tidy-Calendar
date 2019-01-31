let downloadButton = document.getElementById("downloadButton");
let usernameSelect = document.getElementById("usernameSelect");

function activateButton(){
    console.log(downloadButton.disabled);
    downloadButton.disabled = false;
    console.log(downloadButton);
    console.log(downloadButton.disabled);
    console.log("###");
}

usernameSelect.addEventListener("change", activateButton);
console.log("event added");