import requests, sys
from datetime import date, timedelta
from flask import Flask, flash, redirect, render_template, request

app = Flask(__name__)
app.secret_key = "toshowthemessage"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result', methods=['GET','POST'])
def result():

    symbol = request.form['symbol']
    symbol.capitalize()
    
    end_date = date.today()
    start_date = (date.today() - timedelta(days=30)).isoformat()

    url = "https://twelve-data1.p.rapidapi.com/time_series"

    #Stocks like IRCTC are not present with free api plan.
    querystring = {"symbol":{symbol},"interval":"1day","outputsize":"30", "start_date":{start_date},"end_date":{end_date},"exchange":"all","format":"json"}

    headers = {
	"X-RapidAPI-Key": "76c63719d8msh2bef18674a8a0a8p1d0713jsn2e537556494b",
	"X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()


    if 'values' not in data:
        flash("Enter valid Stock Symbol")
        return redirect('/')
        
    dates = [item["datetime"] for item in data['values']]
    prices= [item["close"] for item in data["values"]]

    dates.reverse()
    prices.reverse()

    return render_template("/result.html", dates = dates, prices= prices)




if __name__ == "__main__":
    app.run(debug=True)