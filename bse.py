import requests

url = "https://real-time-finance-data.p.rapidapi.com/stock-quote"

querystring = {"symbol":"irfc","language":"en"}

headers = {
	"x-rapidapi-key": "724e260ffbmshb6d90a80f8609d1p1dc298jsndca2afd27ea2",
	"x-rapidapi-host": "real-time-finance-data.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
