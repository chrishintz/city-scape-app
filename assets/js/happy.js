$(document).ready(function() {

  var percentage, emptiness, image;

  $.get("/chart", function(response) {
    percentage = response.percentage;
    emptiness = response.emptiness;
    image = response.image;

    if (image == "neutral.png") {
      $("#happy").addClass("neutral-face");
    } else if (image == "happy.png") {
      $("#happy").addClass("happy-face");
    }

    var ctx = $("#mycanvas").get(0).getContext("2d");
    var data = [
      {
        value: percentage,
        color: "#FF6600",
      },
      {
        value: emptiness,
        color: "transparent",
      }
    ];

    var chart = new Chart(ctx).Doughnut(data, {
      segmentStrokeColor : "#CF5300",
      percentageInnerCutout : 70,
      animationEasing : "easeOutQuad",
      animationSteps: 200
    });
  });

});
