from flask import Flask, render_template, request
import csv
import math   
import datetime


lb_names = []
light_bulbs = []
with open('static/databases/light_bulbs.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        light_bulbs.append(row)
        lb_names.append(row["name"])

countries_co2  = {}
countries = []
countries_codes =  {}
with open('tmp/co2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not row["Country"] in countries:
            countries.append(row["Country"])
            countries_codes[row["Country"]] = row["Code"]
        countries_co2[row["Country"]] = float(row["CO2"])/1000
kwh_prices = {}

with open('static/databases/kWh_price.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        add = {row["Code"], row["KWH_price"]}
        kwh_prices[row["Code"]] = float(row["KWH_price"])

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')


@app.before_request
def info():
    ip = request.remote_addr
    agent = request.headers.get('User-Agent')
    path = request.path
    time = datetime.datetime.now()
    dict = {"ip": ip,"agent": agent,"path": path,"time": time}
    with open('static/databases/visitors.csv', 'a', newline='') as csvfile:
        w = csv.DictWriter(csvfile, dict.keys())
        w.writerow(dict)


@app.route('/calc', methods=['POST', 'GET'])
def calc():
    if request.method == "GET":
        return render_template("calc.html", types=lb_names, countries=countries)
    
    if request.method == "POST":
        # Check if all fields are filled
        variables = ["price0", "price1", "watts0", "watts1", "amount", "average", "type0", "type1", "country"]
        if not all(request.form.get(field) for field in variables):
            return render_template("error.html", error="Please fill out all the fields.")
        # Def variables
        s = "s" # If its one year or more years
        country = request.form.get("country")
        try:
            kwh_price = kwh_prices[countries_codes[country]]
        except KeyError:
            kwh_price = 0.15
        average = int(request.form.get("average"))
        amount = int(request.form.get("amount"))
        watts = []
        price = []
        type = []
        # Read values from input
        for i in range(2):
            watts.append(int(request.form.get(f"watts{i}")))
            price.append(int(request.form.get(f"price{i}")))
            type.append(request.form.get(f"type{i}"))
        kwh_co2 = countries_co2[country]
        co2_manu = []
        lifetime = []
        lum = []
        avg_watts = []
        # CO2 manu for first and second lightbulb
        for j in range (2):
            for i in range (0, len(light_bulbs)):
                if light_bulbs[i]["name"] == type[j]:
                    value = float(light_bulbs[i]["co2"])
                    lifetime.append  (int(light_bulbs[i]["lifetime"]))
                    lum.append (int(light_bulbs[i]["lumens"]))
                    avg_watts.append (float(light_bulbs[i]["watts"]))
                    co2_manu.append(value)
                    break
        if price[1] == 0:
            print (price[1])
            co2_manu[1] = 0
        # Values for graph profit
        graph_limit = math.ceil(lifetime[0]/365/average)+1
        profit_values = [] 
        for i in range (graph_limit):
            value  = round((price[1]+(kwh_price*amount*average*watts[1]/1000*365*i)) - (price[0]+(kwh_price*average*amount*watts[0]/1000*365*i)),2)
            profit_values.append(value)
        try:
            
            years = round((price[0] - price[1])/(kwh_price*(watts[1] - watts[0])/1000*365*amount*average), 2)
            if years < 1:
                s = ""
        except ZeroDivisionError:
            years="∞"
        # Values for graph co2 saved
        co2 = []
        for i in range (graph_limit):
            value = round((watts[1]/1000*amount*average*365*i*kwh_co2+co2_manu[1])-(watts[0]/1000*amount*average*kwh_co2*365*i+co2_manu[0]),2)
            co2.append(value)
        # Quick facts
        qf = [] # Define variable for all quick facts
        # QF 1: Your new bulb will last qf[0] years and save a total of qf[1].
        qf.append(round(lifetime[0]/365/average, 2))
        qf.append (round((price[1]-price[0])+(kwh_price*((watts[1] - watts[0])/1000)*lifetime[0]),2))
        # QF 2: Every lightbulb will save qf[2] kg of co2
        qf.append (round((watts[1]/1000*lifetime[1]*kwh_co2+co2_manu[1])-(watts[0]/1000*kwh_co2*lifetime[1]+co2_manu[0]),2))
        # QF 3: New lightbulb will shine qf[3] % more
        x = lum[0]/avg_watts[0]*watts[0] # Lumens of new lb
        y = lum[1]/avg_watts[1]*watts[1] # Lumens for old lb
        qf.append (round((x/y-1),1)*100)
        if qf[3] > 0:
            qf[3] = str(qf[3]) + "% more" 
        elif qf[3] < 0:
            qf[3] = (round((y/x-1),1)*100)
            qf[3] = str(qf[3])
            qf[3] = qf[3] + "% less"
        elif qf[3] == 0:
            qf[3] = "same"
        return render_template("resoult.html", years=years, s=s, values=profit_values, co2=co2, qf = qf, limit=graph_limit)
        
@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/how')
def how():
    return render_template("how.html")
