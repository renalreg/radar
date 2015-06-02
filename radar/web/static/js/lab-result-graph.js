function load_result_code(graph_selector, result_code) {
    $(graph_selector).html('<p><img src="/static/img/spinner.gif" /></p>');

    $.get('data.json', {'result_code': result_code}, function(data) {
        var graphData = [];

        if (data.data.length == 0) {
            $(graph_selector).html('<p>No data.</p>');
            return;
        }

        for (var i = 0; i < data.data.length; i++) {
            var row = data.data[i];
            var date = Date.parse(row[0]);
            var value = row[1];
            graphData.push([date, value]);
        }

        var options = {
            chart: {
                zoomType: 'x',
                renderTo: 'graph'
            },
            title: {
                text: data.name
            },
            xAxis: {
                type: 'datetime'
            },
            yAxis: {
                title: {
                    text: data.units
                }
            },
            series: [{
                name: data.name,
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

$(function () {
    $("#result_code").change(function() {
        var result_code = $(this).val();
        load_result_code('#graph', result_code);
    }).trigger("change");
});