from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

def get_traffic_data():
    api_key = '534c54647767756e36395944535144'  # 주어진 API 키
    url = f'http://openapi.seoul.go.kr:8088/{api_key}/json/TrafficInfo/1/10/?TYPE=xml'  # TYPE 파라미터를 xml로 설정
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data from API: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")
    
    # Print the actual response content for debugging
    print("API response text:", response.text)  # API 응답 데이터를 출력

    if response.text.strip() == "":
        print("Empty response from API")
        raise HTTPException(status_code=500, detail="Empty response from API")
    
    try:
        return response.json()
    except ValueError as e:
        print("Error parsing JSON:", str(e))
        raise HTTPException(status_code=500, detail="Invalid JSON response from API")

def parse_traffic_data(data):
    traffic_info = []
    if 'TrafficInfo' in data and 'row' in data['TrafficInfo']:
        for item in data['TrafficInfo']['row']:
            info = {
                'road_name': item.get('ROAD_NM', 'N/A'),
                'congestion': item.get('CONGEST_LVL', 'N/A'),
                'speed': item.get('ROAD_SPD', 'N/A')
            }
            traffic_info.append(info)
    else:
        print("Unexpected data format:", data)  # 데이터 형식이 예상과 다를 경우
        raise HTTPException(status_code=500, detail="Unexpected data format")
    
    return traffic_info

@app.get("/traffic")
async def read_traffic():
    try:
        data = get_traffic_data()
        traffic_data = parse_traffic_data(data)
        return {"traffic_data": traffic_data}
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080, log_level="debug")