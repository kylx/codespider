var isDay = { day: 'numeric' };
var isDayWeek = { weekday: 'long' };
var isMonthYear = { month: 'long', year: 'numeric' };

// var datetest = new Date();
// document.getElementById("theDay").innerHTML = datetest.toLocaleDateString("en-US", isDay);
// document.getElementById("theDayWeek").innerHTML = datetest.toLocaleDateString("en-US", isDayWeek);
// document.getElementById("theMonthYear").innerHTML = datetest.toLocaleDateString("en-US", isMonthYear);


$("#datetest").text(datetest.toDateString());

$('#decr').on('click', function() {
  datetest = new Date(Date.parse($('#datetest').text()));
  datetest.setDate(datetest.getDate() - 1);
  $('#datetest').text(datetest.toDateString());
});

function myFunction() {
  if (confirm("Are you sure you want to save?")) {
    document.getElementById("theDay").innerHTML = datetest.setDate(datetest.getDate() + 1);
    document.getElementById("theDay").innerHTML = datetest.toLocaleDateString("en-US", isDay) ;
    document.getElementById("theDayWeek").innerHTML = datetest.toLocaleDateString("en-US", isDayWeek);
    document.getElementById("theMonthYear").innerHTML = datetest.toLocaleDateString("en-US", isMonthYear);
  } else {
    alert("You pressed cancel.");
  }
  document.getElementById("demo").innerHTML = txt;
}