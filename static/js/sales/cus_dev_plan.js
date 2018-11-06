// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 格式化开发状态
function formatter_devResult(value) {
    if ('0' == value)
        return '未开发';

    if ('1' == value)
        return '开发中';

    if ('2' == value)
        return '开完完成';

    if ('3' == value)
        return '开发失败';

    return value;
}

// 操作
function handler(value, row, index) {
    if (0 == row.devResult || 1 == row.devResult) {
        return '<a href="javascript:develop(' + row.id + ');">开发客户</a>'
    } else {
        return '<a href="javascript:detail(' + row.id + ');">查看详情</a>'
    }
}

// 开发客户
function develop(sale_chance_id) {
    // 打开一个新窗口
    window.parent.openTab('开发客户', '/sales/select_sale_chance_by_id_for_page/' + sale_chance_id + '/?flag=1', 'icon-khkfjh');
}

// 查看详情
function detail(sale_chance_id) {
    // 打开一个新窗口
    window.parent.openTab('查看详情', '/sales/select_sale_chance_by_id_for_page/' + sale_chance_id + '/?flag=0', 'icon-khkfjh');
}

// 按条件查询营销机会
function select_params_sela_chance() {
    // 获取参数
    var customerName = $('#customerName').val().trim();
    var overview = $('#overview').val().trim();
    var devResult = $('#devResult').combobox('getValue');

    $('#dg').datagrid('reload', {
        customerName: customerName,
        overview: overview,
        devResult: devResult
    });
}

// 切换开发状态立即查询
$("#devResult").combobox({
    onChange: function () {
        select_params_sela_chance();
    }
});