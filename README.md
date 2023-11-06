# Energy Cauculator
#### Video Demo:  not done yet
#### Description:
This is web based aplication that help users to get know how much money can they save by chainging lightbulbs.

How to use:
Use url : https://energycalculator.vercel.app/ or run localy on your computer.
For running localy you need to install Python, Flask and Werkzeug. (see requirements.txt).
You can run program by opening folder with code in terminal and typeing flask run.







Data about how much co2 lightbulb save are counted per lifetime of new lightbulb. If price of old lightbulb is 0, there is 0kg co2 spend while manufactoring. 
Data about luments of lightbulbs are based on how much lumens can create 1 watt multiple by number of watts of new lightbulb. When power of new lightbulb is too low, program have big imprecision.
Data about lightbulbs are only estimated. Data about prices of energy are from year 2022 and are only aviable for most of countryes in Europe. For other states is used price 0.15€ per kWh. 