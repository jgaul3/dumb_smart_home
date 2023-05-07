function togglePower() {
    let powerRadioOn = document.getElementById("powerToggleOn").checked;
    if (!powerRadioOn) {
        document.getElementById("ACForm").reset();
        document.getElementById("tempDiv").style.display = "none";
    }
    document.getElementById("settingsDiv").style.display =
        powerRadioOn ? "" : "none";
}

function toggleMode() {
    let needsTemperature = ["cool", "heat"].indexOf(
        document.querySelector('input[name="mode"]:checked')["value"]
    ) > -1;
    document.getElementById("tempDiv").style.display =
        needsTemperature ? "" : "none";
}

function expandDiv(id) {
    let otherDiv = document.getElementById(id);
    otherDiv.style.display = otherDiv.style.display === "none" ? "block" : "none";
}