$.ajax({  
    url: "/pie_chart/",  
    type: "GET",  
    dataType: "json",  
    success: function(arg) {   
        data = JSON.parse(arg);
        Highcharts.chart('container', {
            chart: {
              plotBackgroundColor: null,
              plotBorderWidth: null,
              plotShadow: false,
              type: 'pie'
            },
            title: {
              text: '職缺經歷需求',
              align: 'center'
            },
            tooltip: {
              pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            accessibility: {
              point: {
                valueSuffix: '%'
              }
            },
            plotOptions: {
              pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                  enabled: true,
                  format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
              }
            },
            series: [{
              name: 'Brands',
              colorByPoint: true,
              data:data
            }]
        });
    }
});

