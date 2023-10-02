from flask import Flask, render_template, request
import csv

devices = [
    {"name" : "Lighting"},
    {"name" : "Electronic displays including televisions"},
    {"name" : "Washing machines and washer-dryers"},
    {"name" : "Dishwashers"},
    {"name" : "Fridges and freezers"}
            ]
categories = [
    {"name" : "A"},
    {"name" : "B"},
    {"name" : "C"},
    {"name" : "D"},
    {"name" : "E"},
    {"name" : "F"},
    {"name" : "G"}
        ]
lb_names = []
light_bulbs = []
with open('light_bulbs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        light_bulbs.append(row)
        lb_names.append(row["name"])
app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/calc', methods=['POST', 'GET'])
def calc():
    if request.method == "GET":
        return render_template("calc.html", types=lb_names)
    
    if request.method == "POST":
        # Check if all fields are filled
        variables = ["price0", "price1", "watts0", "watts1", "amount", "average", "type0", "type1"]
        if not all(request.form.get(field) for field in variables):
            return render_template("error.html", error="Please fill out all the fields.")
        # Def variables
        s = "s" # If its one year or more years
        # TODO: add prices based on region
        kwh_price = 0.15 # Price for kwh
        average = int(request.form.get("average"))
        amount = int(request.form.get("amount"))
        watts = []
        price = []
        type = []

        for i in range(2):
            watts.append(int(request.form.get(f"watts{i}")))
            price.append(int(request.form.get(f"price{i}")))
            type.append(request.form.get(f"type{i}"))
        # TODO: chainge co2 based on region
        kwh_co2 = 0.5
        co2_manu = []
        for j in range (2):
            for i in range (0, len(light_bulbs)):
                if light_bulbs[i]["name"] == type[j]:

                    value = float(light_bulbs[i]["co2"])
                    co2_manu.append(value)
                    break
        # Values for graph profit
        profit_values = [] 
        for i in range (10):
            value  = round((price[1]+(kwh_price*amount*average*watts[1]/1000*365*i)) - (price[0]+(kwh_price*average*amount*watts[0]/1000*365*i)),2)
            profit_values.append(value)
        try:
            
            years = round((price[0] - price[1])/(kwh_price*(watts[1] - watts[0])/1000*365*amount*average), 2)
            if years < 1:
                s = ""
        except ZeroDivisionError:
            years="∞"
        co2 = [] # Co2 of new product
        for i in range (10):
            # TODO: co2_manu
            value = round((watts[1]/1000*amount*average*365*i+co2_manu[1]*kwh_co2)-(watts[0]/1000*amount*average*kwh_co2*365*i+co2_manu[0]),2)
            co2.append(value)
        return render_template("resoult.html", years=years, s=s, values=profit_values, co2=co2)



@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/FAQ')
def FAQ():
    return render_template("FAQ.html")

@app.route('/how')
def how():
    return render_template("how.html")
