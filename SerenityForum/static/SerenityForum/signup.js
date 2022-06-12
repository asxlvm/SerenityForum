const regFormSubmit = event => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formJSON = Object.fromEntries(formData.entries());
    console.log(formJSON);
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/register/");
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            const resJSON = JSON.parse(xhr.responseText);
            const errElem = document.getElementById("errorDiv");
            if (resJSON.status != "SUCCESS") {
                if (resJSON.status == "RESERVED_USERNAME") {
                    const reserveRow = document.getElementById("reservationRow");
                    reserveRow.style = "display:block";
                };
                errElem.firstElementChild.className = "collection-item active red darken-1";
                errElem.style = "display:block;text-align:center";
                errElem.firstElementChild.innerText = resJSON.message + "\nStatus code: " + resJSON.status;
            } else if (resJSON.status == "SUCCESS") {
                errElem.firstElementChild.className = "collection-item active green darken-1";
                errElem.style = "display:block;text-align:center";
                errElem.firstElementChild.innerText = resJSON.message;
            };
        }};
    xhr.send(JSON.stringify(formJSON));
}

$(document).ready(function(){
    var bindEvent = function(element, type, handler) {
        if (element.addEventListener) {
            element.addEventListener(type, handler, false);
        } else {
            element.attachEvent('on' + type, handler);
        }
    };
    bindEvent(document.getElementById("regForm"), "submit", regFormSubmit);
    console.log("Bound event.");
});