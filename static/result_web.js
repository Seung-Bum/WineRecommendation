document
  .getElementById('shareButton')
  .addEventListener('click', function () {
    document.getElementById('popupOverlay').style.display = 'block';
    document.getElementById('sharePopup').style.display = 'block';

    // 현재 URL 설정
    document.getElementById('shareUrl').value = window.location.href;
  });

function closePopup() {
  document.getElementById('popupOverlay').style.display = 'none';
  document.getElementById('sharePopup').style.display = 'none';
}

function copyUrl() {
  var copyText = document.getElementById('shareUrl');
  copyText.select();
  document.execCommand('copy');
  alert('URL이 복사되었습니다!');
}

// 카카오톡 공유 버튼 설정
Kakao.init('f917da4d87bab4b5f0df798f944b872c'); // 🔹 여기에 카카오 API 키 입력 (https://developers.kakao.com/)
document
  .getElementById('kakaoShareButton')
  .addEventListener('click', function () {
    Kakao.Share.sendDefault({
      objectType: 'feed',
      content: {
        title: '내가 선택한 와인 🍷',
        description:
          document.getElementById('wine-name').innerText +
          '\n' +
          document.getElementById('wine-description').innerText,
        imageUrl: document.getElementById('wine-image').src,
        link: {
          mobileWebUrl: window.location.href,
          webUrl: window.location.href,
        },
      },
    });
  });


// 서버에서 개발 환경에 맞는 url 반환
async function getApiBaseUrl() {
    const response = await fetch('/config'); // Flask 서버에서 API URL 가져옴
    const data = await response.json(); // JSON 데이터 파싱
    return data.api_base_url; // API URL 반환
}

document.getElementById('replayButton').addEventListener('click', async () => {
    const API_BASE_URL = await getApiBaseUrl(); // 실행 환경에 따른 API URL 가져오기
    const url = API_BASE_URL; // URL 생성

    sessionStorage.clear(); // 세션 스토리지 초기화
    window.location.href = url;
});