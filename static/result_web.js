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


// 인스타그램 공유하기 버튼 설정
document.getElementById("instaShareButton").addEventListener("click", function () {
  const currentPageUrl = window.location.href;
  const userAgent = navigator.userAgent.toLowerCase();

  // 클립보드 API 지원 여부 확인
  if (navigator.clipboard && window.isSecureContext) {
      // HTTPS 환경 및 클립보드 API 지원
      navigator.clipboard.writeText(currentPageUrl).then(() => {
          alert("현재 페이지 링크가 복사되었습니다! 인스타그램에 직접 붙여넣어 공유하세요.");
          openInstagram(userAgent);
      }).catch(err => {
          console.error("클립보드 복사 실패:", err);
          fallbackCopy(currentPageUrl);
      });
  } else {
      // 클립보드 API 미지원 또는 HTTP 환경
      fallbackCopy(currentPageUrl);
  }
});

function fallbackCopy(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
      const successful = document.execCommand('copy');
      if(successful){
          alert("현재 페이지 링크가 복사되었습니다! 인스타그램에 직접 붙여넣어 공유하세요.");
          openInstagram(navigator.userAgent.toLowerCase());
      } else {
          alert("직접 복사해주세요.");
      }

  } catch (err) {
      console.error('복사 실패:', err);
      alert("직접 복사해주세요.");
  }
  document.body.removeChild(textArea);
}

function openInstagram(userAgent) {
  if (/android/.test(userAgent)) {
      window.location.href = "intent://instagram.com#Intent;scheme=https;package=com.instagram.android;S.browser_fallback_url=https://play.google.com/store/apps/details?id=com.instagram.android;end;";
  } else if (/iphone|ipad|ipod/.test(userAgent)) {
      window.location.href = "instagram://app";
      setTimeout(() => {
          alert("인스타그램 앱이 설치되지 않은 것 같습니다. App Store에서 설치 후 다시 시도하세요.");
      }, 2000);
  } else {
      window.open("https://www.instagram.com/", "_blank");
  }
}


// 페이스북 공유하기 버튼 설정
document.getElementById("facebookShareButton").addEventListener("click", function () {
  const currentPageUrl = window.location.href;
  //const currentPageUrl = encodeURIComponent(window.location.href); // 현재 페이지 URL 가져오기 (인코딩)
  const userAgent = navigator.userAgent.toLowerCase(); // 사용자 환경 감지

  console.log('currentPageUrl: ' + currentPageUrl);

  if (/android|iphone|ipad|ipod/.test(userAgent)) {
      // 모바일 환경: 페이스북 앱 실행 (없으면 웹 공유 페이지로 이동)
      const fbAppUrl = `fb://facewebmodal/f?href=${currentPageUrl}`;
      window.location.href = fbAppUrl;

      setTimeout(() => {
          // 앱이 없을 경우 웹 공유 페이지로 이동
          window.location.href = `https://www.facebook.com/sharer/sharer.php?u=${currentPageUrl}`;
      }, 2000);
  } else {
      // PC 환경: 새 창에서 페이스북 공유 페이지 열기 (운영환경에서만 활용됨)
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${currentPageUrl}`, "_blank");
  }
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

document.getElementById("XShareButton").addEventListener("click", function () {
  const pageUrl = encodeURIComponent(window.location.href);
  const tweetText = encodeURIComponent("이 페이지를 확인해 보세요!\n\n"); // 줄바꿈 추가
  const hashtags = encodeURIComponent("wine,와인,와인추천");
  
  const twitterWebUrl = `https://twitter.com/intent/tweet?url=${pageUrl}&text=${tweetText}&hashtags=${hashtags}`;
  const twitterAppUrl = `intent://twitter.com/intent/tweet?url=${pageUrl}&text=${tweetText}&hashtags=${hashtags}#Intent;scheme=https;package=com.twitter.android;end;`;

  // 모바일인지 확인
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

  if (isMobile) {
      window.location.href = twitterAppUrl; // 트위터 앱에서 열기 시도
      setTimeout(() => {
          window.open(twitterWebUrl, "_blank"); // 앱이 없으면 웹으로 열기
      }, 1000);
  } else {
      window.open(twitterWebUrl, "_blank"); // PC는 웹에서 열기
  }
});
