from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from flask import request


app = Flask(__name__)
api = Api(app)
from bs4 import BeautifulSoup
import requests

weather_endpoint = "https://weather.com/weather/hourbyhour/l/ROXX0040:1:RO"
print("Weather endpoint: " + weather_endpoint)


@app.route('/weather/timisoara', methods=['GET'])
def get_weather():
 response = requests.get(weather_endpoint)
 html_doc = response.text
 print("Gathered response. Now parsing it...")
 html = BeautifulSoup(html_doc, 'html.parser')
 table = html.table
 table_class = table['class']
 if table_class == "twc-table":
  print('Weather table not found')
  sys.exit(1)

 print('Iterating forecast by hours table')
 rows = table.find_all('tr')
 data = {}
 data['times'] = []
 data['desc'] = []
 data['temp'] = []
 data['feels'] = []
 data['precip'] = []
 data['humidity'] = []
 data['wind'] = []

 for row in rows:
  time_cols = row.findChildren('td', attrs={'headers':'time'})
  for time in time_cols:
   data['times'].append(time.getText())

  desc_cols = row.findChildren('td', attrs={'headers':'description'})
  for desc in desc_cols:
   data['desc'].append(desc.getText())

  temp_cols = row.findChildren('td', attrs={'headers':'temp'})
  for temp in temp_cols:
   data['temp'].append(temp.getText())

  feels_cols = row.findChildren('td', attrs={'headers':'feels'})
  for feels in feels_cols:
   data['feels'].append(feels.getText())

  precip_cols = row.findChildren('td', attrs={'headers':'precip'})
  for precip in precip_cols:
   data['precip'].append(precip.getText())

  humidity_cols = row.findChildren('td', attrs={'headers':'humidity'})
  for humidity in humidity_cols:
   data['humidity'].append(humidity.getText())

  wind_cols = row.findChildren('td', attrs={'headers':'wind'})
  for wind in wind_cols:
   data['wind'].append(wind.getText())
 
 print( dumps( data ) )
 return dumps( data ), 200

if __name__ == '__main__':
     app.run(port='8082')

