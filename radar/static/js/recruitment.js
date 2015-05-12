function load_recruitment_graph(url, id, title) {
    $.get(url, function(data) {
        var graphData = [];

        for (var i = 0; i < data.data.length; i++) {
            var row = data.data[i];
            var date = Date.parse(row.date);
            var count = row.count;
            graphData.push([date, count]);
        }

        var options = {
            chart: {
                zoomType: 'x',
                renderTo: id
            },
            title: {
                text: title
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: 'Patients'
                },
                min: 0
            },
            series: [{
                name: 'Patients',
                data: graphData
            }],
            plotOptions: {
                line: {
                    marker: {
                        enabled: true
                    }
                }
            }
        };

        var chart = new Highcharts.Chart(options);
    });
}