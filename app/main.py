from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import requests
import xml.etree.ElementTree as ET
import json

app = FastAPI()

def get_traffic_data():
    url = 'http://openapi.seoul.go.kr:8088/534c54647767756e36395944535144/xml/VolInfo/1/5/A-02/20240612/18/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"API에서 데이터를 가져오는 중 오류 발생: {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail="API에서 데이터를 가져오는 중 오류 발생")

    root = ET.fromstring(response.content)
    return root

def parse_traffic_data(data):
    traffic_info = []
    
    for row in data.iter('row'):
        io_type = row.findtext('io_type', '해당 사항 없음')
        io_type_str = "입구" if io_type == '1' else "출구" if io_type == '2' else "알 수 없음"
        
        vol_str = row.findtext('vol', '0')
        vol = int(vol_str) if vol_str.isdigit() else 0
        if vol >= 1000:
            status = "혼잡"
        elif vol >= 500:
            status = "보통"
        else:
            status = "원활"
        
        info = {
            '도로명': row.findtext('spot_num', '해당 사항 없음'),
            '날짜': row.findtext('ymd', '해당 사항 없음'),
            '시간': row.findtext('hh', '해당 사항 없음'),
            '차량의 수': vol,
            '입출구': io_type_str,
            '상태': status
        }
        traffic_info.append(info)
    
    return traffic_info

@app.get("/traffic")
async def read_traffic():
    try:
        data = get_traffic_data()
        traffic_data = parse_traffic_data(data)
        
        # 도로명이 A-02일 때 "사직로"로 변경
        for info in traffic_data:
            if info['도로명'] == 'A-02':
                info['도로명'] = '사직로'

        if not traffic_data:
            return JSONResponse(content={"message": "교통 데이터가 없습니다."}, status_code=200)
        else:
            print("실시간 도로 소통 정보:")
            for info in traffic_data:
                print(f"도로명: {info['도로명']}, 날짜: {info['날짜']}, 시간: {info['시간']}, 입출구: {info['입출구']}, 차량의 수: {info['차량의 수']}, 상태: {info['상태']}")
            
            formatted_data = json.dumps(traffic_data, indent=4, ensure_ascii=False)
            return JSONResponse(content=json.loads(formatted_data), status_code=200)
    
    except Exception as e:
        print("오류 발생:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8080, log_level="debug")