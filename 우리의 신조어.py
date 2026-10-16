import streamlit as st
st.title('신조어가 좋아요')
st.write('제발 자바는 자바스크립트가 아니라고....')

<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>요즘말 사전</title>

<style>
  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 25px 16px;
    background: #fff5f8;
    font-family: Arial, "Malgun Gothic", sans-serif;
    color: #39313a;
  }

  .app {
    max-width: 520px;
    margin: 0 auto;
    background: white;
    border-radius: 25px;
    padding: 25px 20px;
    box-shadow: 0 5px 20px #edcbd744;
  }

  .top {
    text-align: center;
    margin-bottom: 25px;
  }

  .logo {
    font-size: 35px;
  }

  h1 {
    color: #e66c98;
    margin: 8px 0;
    font-size: 28px;
  }

  .subtitle {
    color: #888;
    font-size: 14px;
  }

  .search {
    display: flex;
    gap: 8px;
    margin: 22px 0;
  }

  input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border: 2px solid #f5d5e1;
    border-radius: 13px;
    font-size: 15px;
    outline-color: #e66c98;
  }

  button {
    border: none;
    cursor: pointer;
    font-size: 15px;
    border-radius: 12px;
    padding: 12px 17px;
  }

  .search-btn {
    background: #e66c98;
    color: white;
    font-weight: bold;
  }

  h2 {
    font-size: 18px;
    margin-top: 25px;
  }

  .word-list {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
  }

  .word-btn {
    background: #fff0f5;
    color: #b64d78;
    border: 1px solid #f8d5e2;
  }

  .word-btn:hover {
    background: #f9d9e6;
  }

  .result {
    display: none;
    background: #fff6f9;
    border: 1px solid #f7dce6;
    border-radius: 18px;
    padding: 20px;
    margin-top: 22px;
  }

  .result h2 {
    color: #d95487;
    font-size: 24px;
    margin: 0 0 14px;
  }

  .tag {
    display: inline-block;
    background: #f9dce8;
    color: #a6406c;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 12px;
    margin-bottom: 12px;
  }

  .meaning {
    line-height: 1.7;
  }

  .example {
    background: white;
    padding: 13px;
    border-radius: 12px;
    line-height: 1.6;
    margin-top: 12px;
  }

  .help {
    font-size: 13px;
    color: #888;
    line-height: 1.7;
    margin-top: 25px;
    text-align: center;
  }

  .error {
    color: #c04b72;
    line-height: 1.7;
  }
</style>
</head>

<body>
<main class="app">
  <header class="top">
    <div class="logo">🌷</div>
    <h1>요즘말 사전</h1>
    <p class="subtitle">
      모르는 신조어, 이제 쉽게 알아봐요!
    </p>
  </header>

  <form class="search" id="searchForm">
    <input
      id="searchInput"
      type="search"
      placeholder="궁금한 신조어를 입력해 봐!"
      aria-label="검색할 신조어"
    >
    <button class="search-btn" type="submit">
      검색
    </button>
  </form>

  <h2>💗 신조어 바로 알아보기</h2>
  <div class="word-list" id="wordList"></div>

  <section class="result" id="result" aria-live="polite"></section>

  <p class="help">
    신조어가 낯설어도 괜찮아요!<br>
    단어를 검색하거나 목록을 눌러 뜻을 확인해 보세요. 🌸
  </p>
</main>

<script>
  // 신조어 뜻과 예시는 여기에서 수정할 수 있어요.
  const dictionary = [
    {
      word: "야르",
      meaning: "신나거나 기분이 좋을 때 사용하는 감탄사예요. 상황에 따라 장난스럽게 쓰기도 해요.",
      example: "예시: 오늘 시험 끝났다, 야르!"
    },
    {
      word: "영크크",
      meaning: "인터넷에서 사용되는 신조어예요. 사용하는 사람이나 유행하는 밈에 따라 뜻이 달라질 수 있어요.",
      example: "예시: 정확한 의미는 해당 표현이 사용된 대화를 함께 확인해 보세요."
    },
    {
      word: "L을 가져가",
      meaning: "영어의 L(loss, 패배)에서 나온 표현이에요. 패배나 실수를 받아들이라는 의미로 사용해요.",
      example: "예시: 이번 대결은 네가 졌네. L을 가져가!"
    },
    {
      word: "늙크크",
      meaning: "인터넷 밈이나 대화에서 쓰일 수 있는 표현이에요. 문맥에 따라 의미가 달라질 수 있어요.",
      example: "예시: 이 표현을 본 대화나 게시글을 함께 확인해 보세요."
    }
  ];

  const input = document.getElementById("searchInput");
  const result = document.getElementById("result");
  const wordList = document.getElementById("wordList");

  function showWord(word) {
    const found = dictionary.find(item =>
      item.word.toLowerCase() === word.trim().toLowerCase()
    );

    result.style.display = "block";

    if (!found) {
      result.innerHTML = `
        <p class="error">
          😥 해당 신조어를 찾지 못했어요.<br>
          단어를 다시 확인하거나 다른 표현을 검색해 주세요.
        </p>
      `;
      return;
    }

    result.innerHTML = `
      <span class="tag">신조어 해석</span>
      <h2>${found.word}</h2>
      <p class="meaning">
        <strong>뜻</strong><br>
        ${found.meaning}
      </p>
      <div class="example">
        <strong>💬 사용 예시</strong><br>
        ${found.example}
      </div>
    `;
  }

  // 신조어 버튼을 자동으로 만들어요.
  dictionary.forEach(item => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "word-btn";
    button.textContent = item.word;

    button.addEventListener("click", () => {
      input.value = item.word;
      showWord(item.word);
    });

    wordList.appendChild(button);
  });

  // 검색 버튼을 누르거나 Enter를 치면 실행돼요.
  document.getElementById("searchForm")
    .addEventListener("submit", event => {
      event.preventDefault();

      if (!input.value.trim()) {
        result.style.display = "block";
        result.innerHTML =
          '<p class="error">검색할 신조어를 입력해 주세요! 🌷</p>';
        return;
      }

      showWord(input.value);
    });
</script>
</body>
</html>
