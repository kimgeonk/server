from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import xml.etree.ElementTree as ET
import json

app = FastAPI()

def get_traffic_data():
    url = 'http://openapi.seoul.go.kr:8088/534c54647767756e36395944535144/xml/VolInfo/1/5/A-01/20240612/01/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data from API: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from API")

    root = ET.fromstring(response.content)
    return root

def parse_traffic_data(data):
    traffic_info = []
    for row in data.iter('row'):
        info = {
            '도로명': row.findtext('spot_num', '해당 사항 없음'),
            '날짜': row.findtext('ymd', '해당 사항 없음'),
            '시간': row.findtext('hh', '해당 사항 없음'),
            '차량의 수': row.findtext('vol', '해당 사항 없음')
        }
        traffic_info.append(info)
    return traffic_info

@app.get("/traffic")
async def read_traffic():
    try:
        data = get_traffic_data()
        traffic_data = parse_traffic_data(data)
        if not traffic_data:
            return JSONResponse(content={"message": "No traffic data available"}, status_code=200)
        else:
            print("실시간 도로 소통 정보:")
            for info in traffic_data:
                print(f"도로명: {info['도로명']}, 날짜: {info['날짜']}, 시간: {info['시간']}, 차량의 수: {info['차량의 수']}")
            
            formatted_data = json.dumps(traffic_data, indent=4, ensure_ascii=False)
            return JSONResponse(content=json.loads(formatted_data), status_code=200)
    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8080, log_level="debug")