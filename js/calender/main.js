const date = new Date()
const year = date.getFullYear()
// const month = date.getMonth() + 1
const day = date.getDate()
const dayOfWeek = date.getDay()




function whatDayOfWeek (d) {
    if(d === 1){
        return "Monday"
    }
    if(d === 2){
        return "Tuseday"
    }
    if(d === 3){
        return "wednsday"
    }
    if(d === 4){
        return "Thursday"
    }
    if(d === 5){
        return "Friday"
    }
    if(d === 6){
        return "Saturday"
    }
    if(d === 7){
        return "Sunday"
    }
}
console.log(date)

console.log(year)
// console.log(month)
console.log(day)
console.log(dayOfWeek)
console.log(whatDayOfWeek(dayOfWeek))



// 시간
const clock = document.querySelector("#time");

function getClock() {
    const date = new Date();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");
    clock.innerText = `${hours}:${minutes}:${seconds}`;
}

getClock();
setInterval(getClock, 1000);


// 달
const monthItem = document.querySelector(".container .inner .calender .calender-month .control-month .month")

function getMonthItem() {
    const month = date.getMonth() + 1;
    monthItem.innerText = `${month}`
}
getMonthItem();
setInterval(getMonthItem, 3600000);