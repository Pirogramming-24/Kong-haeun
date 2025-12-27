// 게임 상태 변수
let answer = []; // 정답 숫자 3개
let attempts = 9; // 시도 가능 횟수

// DOM으로 요소 가져오기
const input1=document.getElementById("number1");
const input2=document.getElementById("number2");
const input3=document.getElementById("number3");

const attemptsSpan=document.getElementById("attempts");
const results=document.getElementById("results");
const resultImg=document.getElementById("game-result-img");
const submitBtn=document.querySelector(".submit-button");

// 게임 초기화
// 입력칸 초기화
function resetInputs(){
    input1.value="";
    input2.value="";
    input3.value="";
    input1.focus();
}
// 중복 없는 랜덤 숫자 3개 생성
function generateAnswer(){
    answer=[];
    while (answer.length<3) {
        const num=Math.floor(Math.random()*10);
        if (!answer.includes(num))
            answer.push(num);
    }
}
// 게임 전체 초기화
function initGame(){
    attempts=9;
    attemptsSpan.textContent=attempts;
    results.innerHTML="";
    resultImg.src="";
    submitBtn.disabled=false;

    resetInputs();
    generateAnswer();
}

// 시작
initGame();

// 숫자 확인
function check_numbers() {
    const userNums = [
        input1.value, input2.value, input3.value
    ]

    // 입력 유효성 검사
    if (userNums.includes("")){
        resetInputs();
        return;
    }

    const guess = userNums.map(Number);
    let strike = 0;
    let ball = 0;

    // 숫자 비교
    for (let i=0;i<3;i++){
        if (guess[i]===answer[i])
            strike++;
        else if (answer.includes(guess[i]))
            ball++;
    }

    // 결과 출력
    displayResult(guess,strike,ball);

    // 시도 횟수 감소
    attempts--;
    attemptsSpan.textContent=attempts;

    // 게임 종료 체크
    if (strike===3){
        resultImg.src="success.png";
        submitBtn.disabled=true;
    }
    else if (attempts===0){
        resultImg.src="fail.png";
        submitBtn.disabled=true;
    }

    // 입력칸 초기화
    resetInputs();
}

// 결과 출력
function displayResult(guess,strike,ball){
    // 한 줄 (결과 하나당 한 줄의 컨테이너)
    const row=document.createElement("div");
    row.classList.add("check-result");
    // 입력 숫자(왼쪽)
    const left=document.createElement("div");
    left.classList.add("left");
    left.textContent=guess.join(" ");
    // 결과(오른쪽)
    const right=document.createElement("div");
    right.classList.add("right");

    // 아웃 처리
    if (strike===0 && ball===0){
        const out=document.createElement("span");
        out.classList.add("num-result","out");
        out.textContent="O";
        right.appendChild(out);
    }
    // 스트라이크, 볼 처리
    else {
        // 스트라이크 숫자
        const strikeNum=document.createTextNode(`${strike}`);
        right.appendChild(strikeNum);
        right.appendChild(document.createTextNode(" ")); // 공백
        // S
        const s=document.createElement("span");
        s.classList.add("num-result","strike");
        s.textContent="S";
        right.appendChild(s);
        right.appendChild(document.createTextNode(" "));
        // 볼 숫자
        const ballNum=document.createTextNode(`${ball}`);
        right.appendChild(ballNum);
        right.appendChild(document.createTextNode(" "));
        // B
        const b=document.createElement("span");
        b.classList.add("num-result","ball");
        b.textContent="B";
        right.appendChild(b);
    }

    row.appendChild(left);
    row.appendChild(right);
    results.appendChild(row);
}