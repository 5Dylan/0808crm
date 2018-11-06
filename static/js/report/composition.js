// 准备数据
$(function () {
    var categories = [];
    var data = [];

    $.ajax({
        'type': 'GET',
        'url': '/report/select_compostion/',
        'dataType': 'json',
        'success': function (result) {
            // 获取数据进行赋值
            for (i = 0; i < result.length; i++) {
                categories.push(result[i].level);
                data.push(result[i].amount);
            }

            // 渲染报表
            highcharts(categories, data);
        }
    });
});

// 初始化报表
function highcharts(categories, data) {
    Highcharts.chart('container', {
        chart: {// 报表类型
            type: 'column'
        },
        title: {// 一级标题
            text: '客户构成分析'
        },
        xAxis: {// 报表显示数据名称
            categories: categories,
            crosshair: true
        },
        yAxis: {// 报表侧边栏标题
            min: 0,
            title: {
                text: '客户数量 (人)'
            }
        },
        tooltip: {// 报表提示工具
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:f} 人</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {// 报表的样式
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{// 报表显示数据的来源
            name: '客户',
            data: data
        }]
    });
}