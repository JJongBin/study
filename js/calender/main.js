const date = new Date()     // 객체 생성
const year = date.getFullYear()
const month = date.getMonth() + 1   // 달은 0부터 시작(0 = 1월)
const day = date.getDate()
const dayOfWeek = date.getDay()


// console.log(date)
// console.log(year)
// console.log(month)
// console.log(day)
// console.log(dayOfWeek)


// 시간띄우기
const clock = document.querySelector("#time");

function getClock() {
    const date = new Date();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    clock.innerText = `${hours}:${minutes}:${seconds}`;
}

getClock();
setInterval(getClock, 1000);    // 1초마다 갱신


// 달
const monthItem = document.querySelector(".container .inner .calender .calender-month .control-month .month")

function getMonthItem() {
    const year = date.getFullYear()
    const month = date.getMonth() + 1;
    monthItem.innerText = `${year}.${String(month).padStart(2, "0")}`   // 상단에 년 월 표시
}
getMonthItem();
setInterval(getMonthItem, 3600000);     // 하루 기준으로 갱신


//______________________
const prevLast = new Date(year, month-1, 0);    // 지난달 
const thisLast = new Date(year, month, 0);      // 이번달

const prevLastDate = prevLast.getDate();        // 지난달 마지막 일자
const prevLastDay = prevLast.getDay();          // 지난달 마지막 요일

const thisLastDate = thisLast.getDate();        // 이번달 마지막 일자
const thisLastDay = thisLast.getDay();          // 이번달 마지막 요일


console.log("")
console.log(prevLastDate)
console.log(prevLastDay)
console.log(thisLastDate)
console.log(thisLastDay)

const prevDates = [];       // 달력에 표시할 지난달 마지막 부분
const thisDates = [...Array(thisLastDate + 1).keys()].slice(1); // ES6부터 가능함! (1부터 n까지의 배열)
const nextDates = [];       // 달력에 표시할 다음달 첫 부분

console.log("")
console.log(thisDates)
console.log(nextDates)


if (prevLastDay !== 6) {        // 지난달의 마지막일자가 토요일이면 표시하지 않아야함
    for (let i = 0; i < prevLastDay + 1; i++) {
      prevDates.unshift(prevLastDate - i);      // 큰 수부터 배열에 삽입 / 앞에다 추가됨(unshift)  
    }
}
  
for (let i = 1; i < 7 - thisLastDay; i++) {     
    nextDates.push(i);
}



const dates = prevDates.concat(thisDates, nextDates);       // concat으로 배열을 합침

// foreach(function (callback, index, array) {내용})    인자로 배열의 요소, 인덱스, 배열이 들어갈 수 있음        
// foreach((callback, index, array) => {내용})          화살표함수도 가능
dates.forEach(function (date, i) {
  dates[i] = `<div class="date">${date}</div>`;
})

document.querySelector('.dates').innerHTML = dates.join('');    // join을 이용해서 전체 삽입