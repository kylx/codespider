var isDay = { day: 'numeric' };
var isDayWeek = { weekday: 'long' };
var isMonthYear = { month: 'long', year: 'numeric' };

var dt = new Date();
document.getElementById("theDay").innerHTML = dt.toLocaleDateString("en-US", isDay);
document.getElementById("theDayWeek").innerHTML = dt.toLocaleDateString("en-US", isDayWeek);
document.getElementById("theMonthYear").innerHTML = dt.toLocaleDateString("en-US", isMonthYear);