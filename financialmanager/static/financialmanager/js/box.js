
function isValidURL(str) {
    var pattern = new RegExp("/(https?:\/\/)?([\da-z\.-]+)\.([a-z]{2,6})([\/\w\.-]*)*\/?");
    return pattern.test(str)
};

$(document).ready(function () {
    $(".card-title , .mt-4 span:nth-child(2)").each(function () {
        var value = parseInt($(this).html());
        if (value < 0) {
            $(this).css('color', 'red');
        }
    });
});


function settingsFunction() {
    console.log("heeres")
    const form = document.getElementById('settingsForm')
    const url = form.elements["gateway_url"].value

    if (isValidURL(url)) { form.submit() }
    else {
        document.getElementById("errorAlert").textContent = 'فرم وارد شده اشتباه است لطفا مجددا بررسی کنید '
    }
}

window.onload = function() {

document.getElementById("box-select").onchange = function () {

    window.location.href = (document.getElementById('box-select').value)
};


}