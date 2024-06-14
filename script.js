document.addEventListener('DOMContentLoaded', function() {
    // 서버에서 데이터를 가져오는 함수
    function fetchData() {
        fetch('http://127.0.0.1:8080/traffic')
            .then(response => response.json())
            .then(data => {
                displayTrafficData(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    // 데이터를 화면에 표시하는 함수
    function displayTrafficData(trafficData) {
        const trafficList = document.getElementById('trafficList');
        trafficList.innerHTML = ''; // 기존 데이터 초기화

        // 데이터 배열을 순회하며 각 아이템을 화면에 추가
        trafficData.forEach(item => {
            const statusClass = getStatusClass(item['상태']);
            const statusText = getStatusText(item['상태']);

            const trafficItem = document.createElement('div');
            trafficItem.classList.add('traffic-item');
            trafficItem.innerHTML = `
                <p><strong>도로명:</strong> ${item['도로명']}</p>
                <p><strong>날짜:</strong> ${item['날짜']}</p>
                <p><strong>시간:</strong> ${item['시간']}</p>
                <p><strong>차량 수:</strong> ${item['차량의 수']}</p>
                <p><strong>상태:</strong> <span class="status ${statusClass}"></span> ${statusText}</p>
            `;

            trafficList.appendChild(trafficItem);
        });
    }

    // 상태에 따라 적절한 클래스를 반환하는 함수
    function getStatusClass(status) {
        if (status === '원할') {
            return 'green';
        } else if (status === '보통') {
            return 'yellow';
        } else if (status === '혼잡') {
            return 'red';
        }
    }

    // 상태에 따라 적절한 텍스트를 반환하는 함수
    function getStatusText(status) {
        if (status === '원할') {
            return '원할';
        } else if (status === '보통') {
            return '보통';
        } else if (status === '혼잡') {
            return '혼잡';
        }
    }

    // 페이지 로드 시 데이터를 가져와서 표시
    fetchData();
});