$.ajax({  
  url: "/word_cloud/",  
  type: "GET",  
  dataType: "json",  
  success: function(arg) {   
      js = JSON.parse(arg);

      var i, list;
      for(i in js){
        if(js[i]instanceof Object){
          list = list + js[i].item + " ";
        }
      }

      const text = list,
        lines = text.replace(/[():'?0-9]+/g, '').split(/[\、\,\. ]+/g),
        data = lines.reduce((arr, word) => {
          let obj = Highcharts.find(arr, obj => obj.name === word);
          if (obj) {
            obj.weight += 1;
          } else {
            obj = {
              name: word,
              weight: 1
            };
            arr.push(obj);
          }
          return arr;
        }, []);

      Highcharts.chart('container', {
        accessibility: {
          screenReaderSection: {
            beforeChartFormat: '<h5>{chartTitle}</h5>' +
              '<div>{chartSubtitle}</div>' +
              '<div>{chartLongdesc}</div>' +
              '<div>{viewTableButton}</div>'
          }
        },
        series: [{
          type: 'wordcloud',
          data,
          name: 'Occurrences'
        }],
        title: {
          text: '職缺所需熱門科系',
          align: 'center'
        },
        tooltip: {
          headerFormat: '<span style="font-size: 16px"><b>{point.key}</b></span><br>'
        }
      });
  }
});