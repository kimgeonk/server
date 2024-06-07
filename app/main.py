from fastapi import FastAPI
import requests

app = FastAPI()

# API로부터 교통 데이터를 가져오는 함수
def get_traffic_data():
    api_key = '534c54647767756e36395944535144'  # 자신의 API 키를 사용하세요
    url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/TrafficInfo/1/10/'
    response = requests.get(url)
    return response.json()

# 받은 데이터를 가공하는 함수
def parse_traffic_data(data):
    traffic_info = []
    for item in data['TrafficInfo']['row']:
        info = {
            'road_name': item['ROAD_NM'],
            'congestion': item['CONGEST_LVL'],
            'speed': item['ROAD_SPD']
        }
        traffic_info.append(info)
    return traffic_info

@app.get("/traffic")
async def read_traffic():
    data = get_traffic_data()
    traffic_data = parse_traffic_data(data)
    return {"traffic_data": traffic_data}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000, reload=True)