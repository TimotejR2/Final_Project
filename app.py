from flask import Flask, render_template, request
import math   
import sqlite3

# Read data from database
con = sqlite3.connect("static/data.db")
db = con.cursor()

# Read names of light bulbs to memory
db.execute("SELECT name FROM light_bulbs;")
results = db.fetchall()
lb_names = []
i = 0
for i in range(len(results) - 1):
    row = str(results[i+1])
    lb_names.append(row[2:-3])
    i = i + 1

db.execute("SELECT * FROM light_bulbs;")
results = db.fetchall()
light_bulbs = []
for i in range(len(results) - 1):
    row = str(results[i+1]) # Convert to text
    row = row[1:-3]
    row = row.split(", ") # Chainge to array
    row[0] = row [0][1:-1]
    for j in range (1,6): # Convert numeric data to float, possible to optimalise memory usage by useing int in some cases
        row[j] = float(row[j])
    dic = {"name": row[0], "lifetime": row[1], "watts": row[2], "co2": row[3], "price": row[4], "lumens": row[5]}
    light_bulbs.append(dic)

countries_co2  = {}
countries = []
countries_codes =  {}
db.execute("SELECT * FROM co2;")
results = db.fetchall()
for i in range(len(results) - 1):
    countries.append (results[i][0]) # Name of country
    countries_codes[results[i][0]] = results[i][1]
    countries_co2[results[i][0]] = results[i][3]

db.execute("SELECT * FROM price;")
kwh_prices = {}
results = db.fetchall()
for i in range(len(results) - 1):
    kwh_prices[results[i][0]] = results[i][1]

con.commit()
con.close
del con, db, results, dic, row

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
        try: # Try if country is in databases of 
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
        kwh_co2 = countries_co2[country]/1000
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
            co2_manu[1] = 0
        # Values for graph profit
        graph_limit = math.ceil(lifetime[0]/365/average)+1
        profit_values = [] 
        for i in range (graph_limit):
            value  = round((price[1]+(kwh_price*amount*average*watts[1]/1000*365*i)) - (price[0]+(kwh_price*average*amount*watts[0]/1000*365*i)),2)
            profit_values.append(value)
        if ((price[1]+(kwh_price*amount*average*watts[1]/1000*365*(lifetime[0]/365/average))) - (price[0]+(kwh_price*average*amount*watts[0]/1000*365*(lifetime[0]/365/average)))) <= 0:
            return render_template ("error.html", error = "You will not save any money")
        years = round((price[0] - price[1])/(kwh_price*(watts[1] - watts[0])/1000*365*amount*average), 2)
        if years < 1:
            s = ""
    
        # Values for graph co2 saved
        co2 = []
        co2year1 = watts[1]/1000*amount*average*365*kwh_co2
        co2year0 = watts[0]/1000*amount*average*365*kwh_co2
        for i in range (graph_limit):
            value = round(((co2year1*i+co2_manu[1]) - (co2year0*i+co2_manu[0])),2)
            co2.append(value)
        # Quick facts
        qf = [] # Define variable for all quick facts
        # QF 1: Your new bulb will last qf[0] and save a total of qf[1].
        qf.append(round(lifetime[0]/365/average, 2))
        if qf[0] == 1:
            qf[0] = "one year"
        elif qf[0] < 1:
            qf[0] = "less than one year"
        elif qf[0] > 1 and qf[0] < 2:
            qf[0] = "more than one year"
        else:
            qf[0] = str(qf[0]) + "years"
        qf.append (round((price[1]-price[0])+(kwh_price*((watts[1] - watts[0])/1000)*lifetime[0]),2))

        # QF 2: Every lightbulb will save qf[2] kg of co2
        rozdiel = (watts[1]/1000*kwh_co2*lifetime[0]+co2_manu[1]) - (watts[0]/1000*kwh_co2*lifetime[0]+co2_manu[0])
        qf.append (round( rozdiel,1))

        # QF 3: New lightbulb will shine qf[3] % more
        x = lum[0]/avg_watts[0]*watts[0] # Lumens of new lb   
        y = lum[1]/avg_watts[1]*watts[1] # Lumens for old lb 
        qf.append(".")
        if x > y:
            qf[3] = round(round((x/y-1),1)*100)
            qf[3] = str(qf[3]) + "% more" 
        elif y > x:
            
            qf[3] = round((round(((y-x)/y),2)*100),1) # Fix n.0001 bug
            i = 1
            while qf[3] == 100 or qf[3] == 0: #Fix 100% and 0% bug
                qf[3] = round(((y-x)/y),i)*100
                i = i+1
                if i > 10: # Remove chaince of creating infinite loop
                    break
            qf[3] = str(qf[3])
            qf[3] = qf[3] + "% less"
        elif x == y:
            qf[3] = "same"
        del variables,country, average, amount, watts, price, type, kwh_co2, co2_manu, lifetime, lum, avg_watts, value, co2year1, co2year0, rozdiel, x, y
        return render_template("resoult.html", years=years, s=s, values=profit_values, co2=co2, qf = qf, limit=graph_limit)
        
@app.route('/about')
def about():
    return render_template("about.html")
    
@app.route('/how')
def how():
    return render_template("how.html")
