var isDay = { day: 'numeric' };
var isDayWeek = { weekday: 'long' };
var isMonthYear = { month: 'long', year: 'numeric' };

var datetest = new Date();
document.getElementById("theDay").innerHTML = datetest.toLocaleDateString("en-US", isDay);
document.getElementById("theDayWeek").innerHTML = datetest.toLocaleDateString("en-US", isDayWeek);
document.getElementById("theMonthYear").innerHTML = datetest.toLocaleDateString("en-US", isMonthYear);


$("#datetest").text(datetest.toDateString());

$('#decr').on('click', function() {
  datetest = new Date(Date.parse($('#datetest').text()));
  datetest.setDate(datetest.getDate() - 1);
  $('#datetest').text(datetest.toDateString());
});

$('#incr').on('click', function() {
    document.getElementById("theDay").innerHTML = datetest.setDate(datetest.getDate() + 1);
    document.getElementById("theDay").innerHTML = datetest.toLocaleDateString("en-US", isDay) ;
    document.getElementById("theDayWeek").innerHTML = datetest.toLocaleDateString("en-US", isDayWeek);
    document.getElementById("theMonthYear").innerHTML = datetest.toLocaleDateString("en-US", isMonthYear);
    // datetest = new Date(Date.parse($('#datetest').text()));
    // datetest.setDate(datetest.getDate() + 1);
    // $('#datetest').text(datetest.toDateString());
});