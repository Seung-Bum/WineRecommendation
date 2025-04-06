document.addEventListener("DOMContentLoaded", () => { // DOM(Document Object Model)이 완전히 로드되었을 때 실행할 JavaScript 코드를 정의
  const list = document.getElementById("wine-list");
  const countText = document.getElementById("wine-count");

  function getSelectedTags() {
    return Array.from(document.querySelectorAll("input[type=checkbox]:checked"))
      .map((b) => b.nextElementSibling.textContent.trim()); // 선택된 텍스트 배열
  }

  function fetchWineData(tags = []) {
    // 쿼리 문자열 구성
    const query = tags.length > 0 ? `?tags=${encodeURIComponent(tags.join(","))}` : "";

    fetch(`/getWineData${query}`)
      .then((res) => res.json())
      .then((data) => {
        const wines = Object.values(data);
        list.innerHTML = "";
        wines.forEach((wine) => {
          console.log(wine)
          const div = document.createElement("div");
          div.className = "text-center";
          div.innerHTML = `
            <img
              src="${wine.image_url}"
              class="rounded shadow mb-2 w-full w-[100px]"
            />
            <p class="text-sm">${wine.name}</p>
          `;
          list.appendChild(div);
        });

        countText.textContent = `총 ${wines.length}개의 와인이 검색되었어요!`;
      });
  }

  // 체크박스 변경 이벤트 설정
  document.querySelectorAll("input[type=checkbox]").forEach((box) => {
    box.addEventListener("change", () => {
      const selectedTags = getSelectedTags();
      fetchWineData(selectedTags); // 선택된 태그 기준으로 다시 요청
    });
  });

  // 초기 로딩 시 전체 데이터 가져오기
  fetchWineData();
});
