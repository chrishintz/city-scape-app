$(function () {
  $.get("/pets", function(tweets){
    var scoreArray = [];
    var dayArray   = [];
    for (i = 0; i < tweets.length; i++) {
      scoreArray.push(tweets[i].total);
      dayArray.push(tweets[i]._id.dayOfMonth);
    }

  $('#petchart').highcharts({
      chart: {
          type: 'area'
      },
      title: {
          text: 'Dogs(1) vs. Cats(-1)'
      },
      subtitle: {
        text: 'Are dogs (red) or cats (blue) tweeted about more in Seattle?'
      },
      xAxis: {
          name: 'Day of Month',
          categories: dayArray
      },
      plotOptions: {
          series: {
              animation: {
                  duration: 3000
              },
          }
      },
      credits: {
          enabled: false
      },
      series: [{
          name: 'Pet Score',
          data: scoreArray,
          color: '#FF0000',
          negativeColor: '#0088FF'
      }]
    });
  });
});
