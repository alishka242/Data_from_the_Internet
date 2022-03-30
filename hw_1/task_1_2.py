import requests
import time
import json

if __name__ == '__main__':
    def get_data(service, appid,city):
        while True:
            time.sleep(1)
            url = f'{service}?q={city}&appid={appid}'
            response = requests.get(url)
            if response.status_code == 200:
                print(url)
                break
        return response.json()

    appid = 'b6907d289e10d714a6e88b30761fae22'
    service = 'https://samples.openweathermap.org/data/2.5/weather'
    city = 'London'
    response = get_data(service, appid, city)

    print('Получен результат')
    print(response)

    with open('hw_1/1_2_weather.json', 'w') as f:
        json_repo = json.dump(response, f)