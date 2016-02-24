$(document).ready(function() {
  var ctx = $("#mycanvas").get(0).getContext("2d");
  var data = [
    {
      value: 270,
      color: 'cornflowerblue',
      hightlight: 'lightskyblue',
      label: "javascript",
    },
    {
      value: 50,
      color: '#EAEAEA',
      label: "HTML"
    }
  ];

  var chart = new Chart(ctx).Doughnut(data, {
    segmentStrokeColor : "blue",
    percentageInnerCutout : 70,
    animationEasing : "easeOutQuad",
    animationSteps: 200
  });
  console.log("i'm happy")
});
