    document.getElementById('submitButton').addEventListener('click', () => {
      // 모든 폼 데이터 수집
      const forms = document.querySelectorAll('form');
      const data = {};

      forms.forEach((form) => {
        const inputs = form.querySelectorAll('input[type="radio"]:checked');
        inputs.forEach((input) => {
          data[input.name] = input.value; // 각 폼의 이름과 선택된 값을 수집
        });
      });

    console.log('수집된 데이터:', data);

      // 서버에서 개발 환경에 맞는 url 반환
    async function getApiBaseUrl() {
        const response = await fetch('/config'); // Flask 서버에서 API URL 가져옴
        const data = await response.json(); // JSON 데이터 파싱
        return data.api_base_url; // API URL 반환
    }

    // 서버로 데이터 전송 메서드
    async function sendData(data) {
      try {
          const API_BASE_URL = await getApiBaseUrl(); // 실행 환경에 따른 API URL 가져오기
          const url = API_BASE_URL + "/receiveData"; // URL 생성
  
          const response = await fetch(url, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify(data),
          });
  
          if (response.ok) {
              //console.log(response.text);
             //window.location.href = "/result"; // 성공하면 result.html 페이지로 이동
              const responseData = await response.json();
              if (responseData.redirect) {
                  window.location.href = responseData.redirect; // wine 포함된 URL로 이동
              }
              
          } else {
              const errorData = await response.json();
              if (errorData && errorData.error) {
                  alert("Error: " + errorData.error);
              }
          }
      } catch (error) {
          console.error("Error:", error);
      }
    }

    // 데이터 전송
    sendData(data);
  });
