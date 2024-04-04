import requests
import json
import csv
from tools import BaseTool

class LocationRetriever:
    def __init__(self,file_path='./access/weather_district_id.csv'):
        self.find_geocodes =self.load_file(file_path)

    def load_file(self,file_path):
        find_geocodes = {}
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                find_geocodes[row['district']] = row['district_geocode']
        return find_geocodes

    def find_postal_code(self,find_name):
        for district, postal_code in self.find_geocodes.items():
            if find_name in district or district in find_name:
                return postal_code
        return -1
class Weather(BaseTool):
    def __init__(self):
        super().__init__()
        self.name = '天气获取工具,可获取现在和未来5天的天气信息,默认地址为廊坊市广阳区'
        self.description = '通过城市或地域名获取天气'
        self.variable_description = [('location','string','需要查询天气的地名，缺省值为NULL，此时默认查询廊坊市广阳区(本地地址)')]

        self.baidu_map_api_key = 'your api key'
        self.location_retriever = LocationRetriever()


    def value(self, arguments: dict):
        location_name = arguments['location']
        location_id = 131003
        if location_name != 'NULL':
            location_id = self.location_retriever.find_postal_code(location_name)
        if location_id==-1:
            return {'error':f'所给出的地区名{location_name}可能有误'}
        url = f"https://api.map.baidu.com/weather/v1/?district_id={location_id}&data_type=all&ak={self.baidu_map_api_key}"
        data = requests.get(url).json()
        weather_data = {
            'location':data['result']['location'],
            'now':data['result']['now'],
            'today':data['result']['forecasts'][0],
            'the next day':data['result']['forecasts'][1],
            'on the third day':data['result']['forecasts'][2],
            'the fourth day':data['result']['forecasts'][3],
            'the fifth day':data['result']['forecasts'][4],
        }
        return weather_data
