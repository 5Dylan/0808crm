// 初始化编辑器
$('#tt').edatagrid({
    url: '/customer/select_order_by_customer_id/' + $('#id').val() + '/',
    pagination: true,  // 显示分页工具栏
    rownumbers: true,  // 显示行号
    width: 600,
    height: 333
});

// 格式化分配时间
function formatter_datetime(value) {
    if (undefined == value || null == value)
        return '';

    return value.replace('T', ' ');
}

// 格式化状态
function formatter_state(value) {
    if ('0' == value)
        return '未回款';

    if ('1' == value)
        return '已回款';

    return value;
}

// 操作
function handler(value, row, index) {
    return '<a href="javascript:detail(' + row.id + ');">查看详情</a>'
}

// 查看详情对话框
function detail(order_id) {
    // 根据订单主键查询订单
    $.get('/customer/select_order_by_id/?order_id=' + order_id, function (result) {
        var obj = result.obj;
        // 返显数据
        $('#orderNo').val(obj.orderNo);
        $('#orderDate').val(obj.orderDate.replace('T', ' '));
        $('#address').val(obj.address);
        $('#totalPrice').val(obj.totalPrice);
        if (0 == obj.state) {
            $('#state').val('未回款');
        } else if (1 == obj.state) {
            $('#state').val('已回款');
        }
    });

    // 初始化编辑器
    $('#tt2').edatagrid({
        url: '/customer/select_order_detail_by_order_id/' + order_id + '/',
        pagination: true,  // 显示分页工具栏
        rownumbers: true,  // 显示行号
        width: 600,
        height: 333
    });

    $('#order_detail_dialog').dialog('open');
}

// 初始化查看详情对话框
$('#order_detail_dialog').dialog({
    title: '订单详情',
    width: 700,
    height: 420,
    iconCls: 'icon-lsdd',
    resizable: false,
    modal: true, // 模态
    draggable: false, // 不可移动
    closed: true, // 是否关闭
    buttons: [{
        text: '关闭',
        iconCls: 'icon-cancel',
        handler: function () {
            $('#order_detail_dialog').dialog('close');
        }
    }]
});