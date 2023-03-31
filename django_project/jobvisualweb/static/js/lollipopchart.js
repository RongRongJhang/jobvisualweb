$.ajax({  
    url: "/lollipop_chart/",  
    type: "GET",  
    dataType: "json",  
    success: function(arg) {   
        data = JSON.parse(arg);
        Highcharts.chart('container', {
            chart: {
            type: 'lollipop'
            },
            accessibility: {
            point: {
                valueDescriptionFormat: '{index}. {xDescription}, {point.y}.'
            }
            },
            legend: {
            enabled: false
            },
            title: {
            text: '職缺數量分布'
            },
            tooltip: {
            shared: true
            },
            xAxis: {
            type: '新竹地區'
            },
            yAxis: {
            title: {
                text: '職缺數'
            }
            },
            series: [{
            name: '職缺數',
            data:data
            }]
        });
    }
});

