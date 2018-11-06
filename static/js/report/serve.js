$(function () {
    var data = [];

    $.ajax({
        'type': 'GET',
        'url': '/report/select_serve/',
        'dataType': 'json',
        'success': function (result) {
            // 获取数据进行赋值
            for (i = 0; i < result.length; i++) {
                var options = {
                    name: result[i].serveType,
                    y: result[i].amount
                }

                // 如果是投诉，选中
                if ('投诉' == result[i].serveType) {
                    options.sliced = true;
                    options.selected = true;
                }

                data.push(options);
            }

            // 渲染报表
            highcharts(data);
        }
    });
});

// 初始化报表
function highcharts(data) {
    Highcharts.chart('container', {
        chart: {// 报表类型
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {// 一级标题
            text: '客户服务分析'
        },
        tooltip: {// 报表提示工具
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        plotOptions: {// 报表的样式
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                }
            }
        },
        series: [{// 报表显示数据的来源
            name: '服务',
            colorByPoint: true,
            data: data
        }]
    });
}