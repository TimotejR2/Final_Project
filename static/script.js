var clicked = 0;
function show_info() {
if (clicked === 0){
        document.getElementById("1").innerHTML = "Daily average (h): How many hours do you use lightbulb every day";
        document.getElementById("2").innerHTML = "Amount: How many lightbulbs do you want to replace";
        document.getElementById("3").innerHTML = "Country: In witch country are lightbulbs. (Datas about prices of electricity are only for countryes in EU. For other countryes is used 0.15€/kWh)";
        document.getElementById("4").innerHTML = "Price: How much lightbulb cost.";
        document.getElementById("5").innerHTML = "Watts: What is the power of lightbulb in watts.";
        document.getElementById("6").innerHTML = "Type: What type is lightbulb. (If not sure, use \"Average\")";
        clicked = 1;
    }
    else if (clicked === 1) {
        document.getElementById("1").innerHTML = "";
        document.getElementById("2").innerHTML = "";
        document.getElementById("3").innerHTML = "";
        document.getElementById("4").innerHTML = "";
        document.getElementById("5").innerHTML = "";
        document.getElementById("6").innerHTML = "";
        clicked = 0;
    }
}
/*FIXME:   
window.onload = function(){
    addEventListener('scroll', function() {
        var Y = window.scrollY;
        if (Y < 100){
            console.log(Y);
            window.scrollTo({
                top: 100,
                behavior: "instant",
            });
        }
    });
}
*/