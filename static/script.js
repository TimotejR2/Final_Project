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
    if (isMobile() == false){

        var Y = window.scrollY;
        addEventListener('scroll', function() {
            
            if (Y == 0){
                try {
                    window.scrollTo({ top: 100, behavior: "instant" });
                    if (window.scrollY != 100) throw "instant not supported";
                } catch {
                    window.scrollTo({ top: 100, behavior: "auto" });
                }
            }
            Y = window.scrollY;
    });
    }
}

function isMobile(){
    console.log("start")
    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ||
       (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.platform))) {
        console.log("true")
        return true;
    }
        console.log("false")
        return false;
    }
