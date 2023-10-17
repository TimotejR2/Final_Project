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



window.onload = function(){
var top = 1;
    addEventListener('scroll', function() {
        console.log("scroll")
        if (top == 1){
            document.getElementById("header").style.display = 'none';
            setTimeout(() => {window.scrollTo({top: 1, behavior: "smooth",});},"100");
            top = 2; //2 means header was hided right now
            setTimeout(() => {
                top = 0;
            }, "1000");
        }
        else{
            if (top == 0){
                if (0 == window.scrollY){
                    document.getElementById("header").style.display = 'block';
                    top = 1;
                }
            }
        }
    });
}