from fastapi import FastAPI, HTTPException, Response
import requests
import xml.etree.ElementTree as ET

app = FastAPI()

def get_traffic_data():
    url = 'http://openapi.seoul.go.kr:8088/534c54647767756e36395944535144/xml/SpotInfo/1/50/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data from API: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")

    root = ET.fromstring(response.content)
    return root

def parse_traffic_data(data):
    traffic_info = []
    for row in data.iter('row'):
        info = {
            'road_name': row.findtext('ROAD_NM', 'N/A'),
            'congestion': row.findtext('CONGEST_LVL', 'N/A'),
            'speed': row.findtext('ROAD_SPD', 'N/A')
        }
        traffic_info.append(info)
    return traffic_info

@app.get("/traffic")
async def read_traffic():
    try:
        data = get_traffic_data()
        traffic_data = parse_traffic_data(data)
        if not traffic_data:
            return Response(content="No traffic data available", status_code=200)
        else:
            print("실시간 도로 소통 정보:")
            for info in traffic_data:
                print(f"도로명: {info['road_name']}, 혼잡도: {info['congestion']}")
            return Response(content=str(traffic_data), media_type="application/json", status_code=200)
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080, log_level="debug")